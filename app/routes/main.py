# Importar componentes necessários do Flask
from flask import Blueprint, render_template, redirect, url_for, request, flash
# Importar decorators e objetos do Flask-Login
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Hotel, Experiencia, Acessibilidade, Cidade, Favorito, User, Carrinho, Reserva
import re

# Criar Blueprint para rotas principais da aplicação
# Sem url_prefix, as rotas começam diretamente da raiz (/)
main_bp = Blueprint('main', __name__)


def validar_cpf(cpf):
    """
    Valida apenas o FORMATO do CPF (11 dígitos numéricos), sem checar os
    dígitos verificadores. Isso permite usar qualquer sequência de 11 números
    para testes, sem exigir um CPF real.
    """
    cpf = re.sub(r'\D', '', cpf or '')
    return len(cpf) == 11


def mascarar_cpf(cpf):
    """
    Retorna apenas os 3 últimos dígitos do CPF (formato usado para exibição
    no histórico), sem guardar nem mostrar o número completo em nenhum momento.
    """
    cpf = re.sub(r'\D', '', cpf or '')
    return cpf[-3:] if len(cpf) >= 3 else cpf


def validar_dados_cartao(numero_cartao, validade_cartao, cvv_cartao):
    """
    Faz uma validação básica dos dados do cartão de crédito informado no formulário:
    - número com 13 a 19 dígitos (padrão da maioria das bandeiras)
    - validade no formato MM/AA, com mês entre 01 e 12
    - CVV com 3 ou 4 dígitos
    Retorna True se todos os campos estiverem em um formato aceitável.
    """
    numero_limpo = re.sub(r'\D', '', numero_cartao or '')
    if not (13 <= len(numero_limpo) <= 19):
        return False

    if not re.fullmatch(r'(0[1-9]|1[0-2])/\d{2}', validade_cartao or ''):
        return False

    if not re.fullmatch(r'\d{3,4}', cvv_cartao or ''):
        return False

    return True

@main_bp.route('/')
# @login_required  # Decorator que protege a rota - requer autenticação
def index():
    """
    Página inicial do sistema (protegida).
    
    Apenas usuários autenticados podem acessar esta página.
    Se não autenticado, será redirecionado para a página de login.
    
    Returns:
        Renderiza o template index.html com dados do usuário atual
    """
    # current_user é um objeto especial do Flask-Login que representa
    # o usuário atualmente autenticado na sessão
    
    
    slides_data = [
        {
            "image": "static/images/bento/bento.jpg",
            "title": "Bento Gonçalves - RS",
            "link": "/destinos/bento", # Rota para onde o botão vai
            "button_text": "Ver mais"
        },
        {
            "image": "static/images/poa/porto-2.jpg",
            "title": "Porto Alegre - RS",
            "link": "/destinos/porto",
            "button_text": "Ver mais"
        },
        {
            "image": "static/images/gramado/gramado.jpg",
            "title": "Gramado - RS",
            "link": "/destinos/gramado",
            "button_text": "Ver mais"
        }
    ]
    
    return render_template('index.html', user=current_user, slides=slides_data)

@main_bp.route('/dashboard')
@login_required  # Esta rota também requer autenticação
def dashboard():
    """
    Página de dashboard (protegida).
    
    Exemplo de rota adicional protegida. Pode ser usada para
    exibir estatísticas, relatórios ou informações do usuário.
    
    Returns:
        Renderiza o template dashboard.html com dados do usuário
    """
    return render_template('dashboard.html', user=current_user)

from flask import redirect, url_for

@main_bp.route('/perfil')
@login_required
def perfil():
    """
    Redireciona a rota principal do perfil direto para a aba de informações
    """
    return redirect(url_for('main.perfil_informacoes'))

@main_bp.route('/botoes_lat_perf/perfil_informacoes')
def perfil_informacoes():
    # Aponta para a subpasta e respeita o nome "perfil_informacoes" do seu arquivo
    return render_template('botoes_lat_perf/perfil_informacoes.html', active_page='informacoes')

@main_bp.route('/botoes_lat_perf/perfil_carrinho')
@login_required
def perfil_carrinho():
    # 1. Busca os hotéis no carrinho
    hoteis_carrinho = Carrinho.query.filter(Carrinho.user_id == current_user.id, Carrinho.hotel_id.isnot(None)).all()

    # 2. Busca as experiências pagas no carrinho (pontos turísticos gratuitos nunca entram aqui)
    experiencias_carrinho = Carrinho.query.filter(Carrinho.user_id == current_user.id, Carrinho.experiencia_id.isnot(None)).all()

    # 3. Calcula o valor total do carrinho
    total_carrinho = sum(item.subtotal for item in hoteis_carrinho) + sum(item.subtotal for item in experiencias_carrinho)

    return render_template(
        'botoes_lat_perf/perfil_carrinho.html',
        active_page='carrinho',
        hoteis=hoteis_carrinho,
        experiencias=experiencias_carrinho,
        total_carrinho=total_carrinho
    )


@main_bp.route('/carrinho/adicionar/<string:tipo>/<int:item_id>', methods=['POST'])
@login_required
def adicionar_carrinho(tipo, item_id):
    """
    Adiciona um item ao carrinho ou soma a quantidade se ele já estiver lá.
    Apenas hotéis e experiências pagas podem ser adicionados (pontos turísticos
    gratuitos não têm valor a pagar, então não fazem sentido no carrinho).
    """
    quantidade = request.form.get('quantidade', 1, type=int)
    if quantidade is None or quantidade < 1:
        quantidade = 1

    if tipo == 'hotel':
        item_carrinho = Carrinho.query.filter_by(user_id=current_user.id, hotel_id=item_id).first()
    else:  # experiencia
        # Verificação de segurança: só permite experiências com preço > 0
        experiencia = Experiencia.query.get(item_id)
        if experiencia and experiencia.preco <= 0:
            flash('Este item é gratuito e não pode ser adicionado ao carrinho.', 'warning')
            return redirect(request.referrer or url_for('main.index'))
        item_carrinho = Carrinho.query.filter_by(user_id=current_user.id, experiencia_id=item_id).first()

    if item_carrinho:
        item_carrinho.quantidade += quantidade
        flash('Quantidade atualizada no carrinho!', 'success')
    else:
        item_carrinho = Carrinho(user_id=current_user.id, quantidade=quantidade)
        if tipo == 'hotel':
            item_carrinho.hotel_id = item_id
        else:
            item_carrinho.experiencia_id = item_id
        db.session.add(item_carrinho)
        flash('Adicionado ao carrinho com sucesso!', 'success')

    db.session.commit()
    return redirect(request.referrer or url_for('main.perfil_carrinho'))


@main_bp.route('/carrinho/atualizar/<int:carrinho_id>', methods=['POST'])
@login_required
def atualizar_carrinho(carrinho_id):
    """
    Atualiza a quantidade de um item do carrinho. Se a quantidade enviada
    for menor que 1, o item é removido.
    """
    item = Carrinho.query.filter_by(id=carrinho_id, user_id=current_user.id).first()

    if item:
        nova_quantidade = request.form.get('quantidade', 1, type=int)
        if nova_quantidade is None or nova_quantidade < 1:
            db.session.delete(item)
            flash('Item removido do carrinho.', 'info')
        else:
            item.quantidade = nova_quantidade
            flash('Quantidade atualizada!', 'success')
        db.session.commit()

    return redirect(url_for('main.perfil_carrinho'))


@main_bp.route('/carrinho/remover/<int:carrinho_id>', methods=['POST'])
@login_required
def remover_carrinho(carrinho_id):
    """
    Remove um item do carrinho, independente da quantidade.
    """
    item = Carrinho.query.filter_by(id=carrinho_id, user_id=current_user.id).first()

    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Item removido do carrinho.', 'info')

    return redirect(url_for('main.perfil_carrinho'))


@main_bp.route('/carrinho/limpar', methods=['POST'])
@login_required
def limpar_carrinho():
    """
    Remove todos os itens do carrinho do usuário de uma vez só.
    """
    Carrinho.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Carrinho esvaziado com sucesso!', 'info')
    return redirect(url_for('main.perfil_carrinho'))


@main_bp.route('/carrinho/finalizar', methods=['POST'])
@login_required
def finalizar_reserva():
    """
    Transforma todos os itens do carrinho em reservas confirmadas.
    Cada item do carrinho vira um registro de Reserva; ao final, o carrinho é esvaziado.
    """
    itens_carrinho = Carrinho.query.filter_by(user_id=current_user.id).all()

    if not itens_carrinho:
        flash('Seu carrinho está vazio.', 'warning')
        return redirect(url_for('main.perfil_carrinho'))

    # Dados gerais, válidos para todos os itens desta reserva
    nome_responsavel = request.form.get('nome_responsavel', '').strip()
    telefone_contato = request.form.get('telefone_contato', '').strip()
    cpf_responsavel = request.form.get('cpf_responsavel', '').strip()
    observacoes = request.form.get('observacoes', '').strip()

    nome_cartao = request.form.get('nome_cartao', '').strip()
    numero_cartao = request.form.get('numero_cartao', '').strip()
    validade_cartao = request.form.get('validade_cartao', '').strip()
    cvv_cartao = request.form.get('cvv_cartao', '').strip()

    if not nome_responsavel or not telefone_contato or not cpf_responsavel:
        flash('Preencha o nome do responsável, o telefone de contato e o CPF para confirmar a reserva.', 'warning')
        return redirect(url_for('main.perfil_carrinho'))

    if not validar_cpf(cpf_responsavel):
        flash('O CPF informado é inválido. Verifique os números digitados.', 'warning')
        return redirect(url_for('main.perfil_carrinho'))

    if not nome_cartao or not validar_dados_cartao(numero_cartao, validade_cartao, cvv_cartao):
        flash('Verifique os dados do cartão de crédito: número, validade (MM/AA) e CVV.', 'warning')
        return redirect(url_for('main.perfil_carrinho'))

    cpf_formatado = mascarar_cpf(cpf_responsavel)
    numero_cartao_limpo = re.sub(r'\D', '', numero_cartao)

    for item in itens_carrinho:
        nova_reserva = Reserva(
            user_id=current_user.id,
            quantidade=item.quantidade,
            valor_total=item.subtotal,
            nome_responsavel=nome_responsavel,
            telefone_contato=telefone_contato,
            cpf_responsavel=cpf_formatado,
            nome_cartao=nome_cartao,
            numero_cartao_final=numero_cartao_limpo[-4:],
            validade_cartao=validade_cartao,
            observacoes=observacoes or None
        )

        if item.hotel_id:
            # Campos específicos de hotel: data de entrada e de saída
            data_entrada_str = request.form.get(f'data_entrada_{item.id}')
            data_saida_str = request.form.get(f'data_saida_{item.id}')

            nova_reserva.hotel_id = item.hotel_id
            if data_entrada_str:
                nova_reserva.data_entrada = datetime.strptime(data_entrada_str, '%Y-%m-%d').date()
            if data_saida_str:
                nova_reserva.data_saida = datetime.strptime(data_saida_str, '%Y-%m-%d').date()
        else:
            # Campos específicos de experiência: data e horário do passeio
            data_passeio_str = request.form.get(f'data_passeio_{item.id}')
            horario_passeio_str = request.form.get(f'horario_passeio_{item.id}')

            nova_reserva.experiencia_id = item.experiencia_id
            if data_passeio_str:
                nova_reserva.data_passeio = datetime.strptime(data_passeio_str, '%Y-%m-%d').date()
            if horario_passeio_str:
                nova_reserva.horario_passeio = horario_passeio_str

        db.session.add(nova_reserva)

    # Esvazia o carrinho depois de transformar tudo em reservas
    Carrinho.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    flash('Reserva confirmada com sucesso! Você pode acompanhar tudo no seu histórico.', 'success')
    return redirect(url_for('main.perfil_historico'))

@main_bp.route('/botoes_lat_perf/perfil_preferencias')
def perfil_preferencias():
    return render_template('botoes_lat_perf/perfil_preferencias.html', active_page='preferencias')

@main_bp.route('/botoes_lat_perf/perfil_historico')
@login_required
def perfil_historico():
    hoteis_reservados = Reserva.query.filter(
        Reserva.user_id == current_user.id, Reserva.hotel_id.isnot(None)
    ).order_by(Reserva.data_criacao.desc()).all()

    experiencias_reservadas = Reserva.query.filter(
        Reserva.user_id == current_user.id, Reserva.experiencia_id.isnot(None)
    ).order_by(Reserva.data_criacao.desc()).all()

    return render_template(
        'botoes_lat_perf/perfil_historico.html',
        active_page='historico',
        hoteis=hoteis_reservados,
        experiencias=experiencias_reservadas
    )

@main_bp.route('/botoes_lat_perf/perfil_favoritos')
@login_required
def perfil_favoritos():
    # 1. Busca os hotéis favoritados
    hoteis_favoritos = Favorito.query.filter(Favorito.user_id == current_user.id, Favorito.hotel_id.isnot(None)).all()
    
    # 2. Busca todas as experiências/pontos favoritados
    todos_favoritos_exp = Favorito.query.filter(Favorito.user_id == current_user.id, Favorito.experiencia_id.isnot(None)).all()
    
    pontos_turisticos = []
    expericias_pagas = []
    
    for fav in todos_favoritos_exp:
        if fav.experiencia and fav.experiencia.categoria:
            # Transforma em minúsculo e remove espaços extras para padronizar
            categoria_limpa = fav.experiencia.categoria.lower().strip()
            
            # Verifica se contém "ponto" e "turist" (assim aceita com ou sem acento no 'í')
            if 'ponto' in categoria_limpa and 'turist' in categoria_limpa:
                pontos_turisticos.append(fav)
            else:
                expericias_pagas.append(fav)
                
    return render_template(
        'botoes_lat_perf/perfil_favoritos.html', 
        active_page='favoritos', 
        hoteis=hoteis_favoritos,
        experiencias=expericias_pagas,
        pontos_turisticos=pontos_turisticos
    )

@main_bp.route('/favoritar/<string:tipo>/<int:item_id>', methods=['POST'])
@login_required
def favoritar_item(tipo, item_id):
    if tipo == 'hotel':
        favorito = Favorito.query.filter_by(user_id=current_user.id, hotel_id=item_id).first()
    else:  # experiencia ou ponto_turistico
        favorito = Favorito.query.filter_by(user_id=current_user.id, experiencia_id=item_id).first()

    if favorito:
        db.session.delete(favorito)
        db.session.commit()
        flash('Item removido dos favoritos com sucesso!', 'info')
    else:
        novo_favorito = Favorito(user_id=current_user.id)
        if tipo == 'hotel':
            novo_favorito.hotel_id = item_id
        else:  # Salva como experiencia (independente de ser Ponto Turístico ou Experiência)
            novo_favorito.experiencia_id = item_id

        db.session.add(novo_favorito)
        db.session.commit()
        flash('Adicionado aos favoritos com sucesso!', 'success')

    return redirect(request.referrer or url_for('main.index'))


@main_bp.route('/favoritos/limpar', methods=['POST'])
@login_required
def limpar_favoritos():
    """
    Remove todos os favoritos do usuário de uma vez só.
    """
    Favorito.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Favoritos esvaziados com sucesso!', 'info')
    return redirect(url_for('main.perfil_favoritos'))

# ====================================================================================
# Alterar a rota para pasta cidades, toda acidade adicionada deve ser adicionada la;
# para isso faça /nome_da_pasta/nome_da_cidade.html dentro da def destinos
# ====================================================================================
@main_bp.route("/destinos/<destino>")
def destinos(destino):
    print(destino)
    if destino == "bento":
        return render_template("/cidades/bento.html",user=current_user )

    if destino == "porto":
        return render_template("/cidades/porto.html",user=current_user )

    if destino == "gramado":
        return render_template("/cidades/gramado.html",user=current_user )


@main_bp.route('/reserva/<string:tipo>/<int:item_id>', methods=['GET', 'POST'])
@login_required
def detalhe_reserva(tipo, item_id):
    item_nome = ""
    item_imagem = ""
    preco_item = 0.00  # Inicializa o preço zerado por padrão para segurança
    acessibilidade = None  # Inicializa como None por padrão
    lat = -29.6  # Valor padrão de segurança (evita NameError se o item não tiver coordenadas no banco)
    lng = -51.16  # Valor padrão de segurança (Serra Gaúcha/RS)
    
    # 1. MAPEAMENTO DE FALLBACK (Usado se o banco de dados falhar ou estiver vazio)
    nomes_hoteis = {
        1: "Pousada Pipas Terroir", 2: "Döra Experience", 3: "Budget Farroupilha", 4: "Hotel Bem-Te-Vi", 5: "Spa do Vinho Condomínio",
        6: "Hotel Valle D’incanto", 7: "Hotel Ritta Höppner", 8: "WoodStone Gramado Hotel", 9: "Exclusive Gramado", 10: "Buona Vitta Gramado",
        11: "Hotel Master Cosmopolitan", 12: "Hotel Continental", 13: "Plaza São Rafael", 14: "Double Tree by Hilton", 15: "Hotel Laghetto Viverone Moinhos"
    }
    
    nomes_experiencias = {
        1: "Vale del Vino", 2: "Parque da Ovelha", 3: "Parque Temático Epopeia Italiana", 4: "Pipa Pórtico", 5: "Vale do Rio das Antas",
        6: "Faça um passeio de maria fumaça!", 7: "Conheça o preparo tradicional do chimarrão", 8: "Piquenique nos vinhedos", 9: "Viva a aventura e adrenalina com voo de balão", 10: "Experiência única no Parque Caminhos da Aventura",
        11: "Lago Negro", 12: "Mini Mundo", 13: "Rua Coberta", 14: "Snowland", 15: "Museu de Cera Dreamland",
        16: "Viva o natal em gramado", 17: "Se impressione com carros antigos e classicos de Hollywood!", 18: "Experimente outro nivel de gastronomia", 19: "Parta para um dos cartões postais da Serra Gaúcha", 20: "Tire fotos na Rua Torta",
        21: "Orla do Guaíba", 22: "Casa de Cultura Mario Quintana", 23: "Memorial do Rio Grande do Sul", 24: "Praça da Matriz", 25: "Parque Moinhos de Vento",
        26: "Viva a atmosfera gremista!", 27: "Veleje pelo Guaíba", 28: "Explore a gastronomia local!", 29: "Assista a um espetáculo no histórico Theatro São Pedro", 30: "Entre na arte da cidade"
    }

    # 2. LÓGICA PARA HOSPEDAGENS (HOTEIS)
    if tipo == 'hotel':
        try:
            hotel = Hotel.query.get(item_id)
            if hotel:
                item_nome = hotel.nome
                preco_item = hotel.preco  # <-- Busca o preço mapeado no Banco
                acessibilidade = Acessibilidade.query.filter_by(hotel_id=hotel.id).first()
                # Coleta as coordenadas reais do banco se elas existirem
                if hotel.latitude and hotel.longitude:
                    lat = hotel.latitude
                    lng = hotel.longitude
            else:
                item_nome = nomes_hoteis.get(item_id, f"Hotel {item_id}")
                acessibilidade = Acessibilidade.query.filter_by(hotel_id=item_id).first()
        except Exception:
            item_nome = nomes_hoteis.get(item_id, f"Hotel {item_id}")
            acessibilidade = None
        
        # Mapeamento de Imagens dos Hotéis
        if item_id <= 5:
            item_imagem = f"images/bento/hotel{item_id}.bento.jfif"
        elif item_id >= 6 and item_id <= 10:
            mapa_gramado_ht = {6: "gram_ht01.webp", 7: "gram_ht02.jpg", 8: "gram_ht03.jpg", 9: "gram_ht04.jpg", 10: "gram_ht05.webp"}
            item_imagem = f"images/gramado/{mapa_gramado_ht[item_id]}"
        elif item_id >= 11 and item_id <= 15:
            mapa_poa_ht = {11: "hotel1.poa.jfif", 12: "hotel2.poa.jfif", 13: "hotel3.poa.jfif", 14: "hotel4.poa.jfif", 15: "hotel5.poa.jfif"}
            item_imagem = f"images/poa/{mapa_poa_ht[item_id]}"

    # 3. LÓGICA PARA PONTOS TURÍSTICOS E EXPERIÊNCIAS
    else:  # tipo == 'experiencia'
        # Pegamos o nome esperado do dicionário de fallback primeiro
        nome_esperado = nomes_experiencias.get(item_id)
        
        try:
            # 1. Tenta buscar no banco pelo ID enviado
            exp = Experiencia.query.get(item_id)
            
            # 2. Se não achar pelo ID, busca pelo Nome exato para corrigir dessincronização de ID
            if not exp and nome_esperado:
                exp = Experiencia.query.filter_by(nome=nome_esperado).first()

            if exp:
                item_nome = exp.nome
                preco_item = exp.preco
                # Busca a acessibilidade usando o ID REAL que está no banco de dados
                acessibilidade = Acessibilidade.query.filter_by(experiencia_id=exp.id).first()
                
                if exp.latitude and exp.longitude:
                    lat = exp.latitude
                    lng = exp.longitude
            else:
                # Fallback absoluto se o banco estiver completamente vazio
                item_nome = nome_esperado if nome_esperado else f"Experiência {item_id}"
                acessibilidade = Acessibilidade.query.filter_by(experiencia_id=item_id).first()
        except Exception:
            item_nome = nome_esperado if nome_esperado else f"Experiência {item_id}"
            acessibilidade = None
        
        # Mapeamento de Imagens das Experiências
        if item_id <= 5:
            item_imagem = f"images/bento/ponto{item_id}.jfif"
        elif item_id <= 10:
            item_imagem = f"images/bento/exp{item_id - 5}.jfif"
        elif item_id >= 11 and item_id <= 20:
            mapa_gramado_exp = {
                11: "pnt_tur01.webp", 12: "pnt_tur02.jpg", 13: "pnt_tur03.jpg", 14: "pnt_tur04.avif", 15: "pnt_tur05.jpg",
                16: "gramadoexp1.jfif", 17: "gramadoexp2.jfif", 18: "gramadoexp3.jfif", 19: "gramadoexp4.jfif", 20: "gramadoexp5.jfif"
            }
            item_imagem = f"images/gramado/{mapa_gramado_exp[item_id]}"
        elif item_id >= 21 and item_id <= 30:
            mapa_poa_exp = {
                21: "orla.jfif", 22: "marioquintana.jfif", 23: "memorialrs.jfif", 24: "pracamatriz.jfif", 25: "moinhos.jfif",
                26: "arena.jfif", 27: "guaiba.jfif", 28: "rdelaboca.jfif", 29: "theatro.jfif", 30: "iberec.jfif"
            }
            item_imagem = f"images/poa/{mapa_poa_exp[item_id]}"

    if tipo == 'hotel':
        is_favorited = Favorito.query.filter_by(user_id=current_user.id, hotel_id=item_id).first() is not None
    else:
        is_favorited = Favorito.query.filter_by(user_id=current_user.id, experiencia_id=item_id).first() is not None

    # 4. TRATAMENTO DO ENVIO DO FORMULÁRIO DE RESERVA DIRETA (sem passar pelo carrinho)
    if request.method == 'POST':
        nome_responsavel = request.form.get('nome_responsavel', '').strip()
        telefone_contato = request.form.get('telefone_contato', '').strip()
        cpf_responsavel = request.form.get('cpf_responsavel', '').strip()
        observacoes = request.form.get('observacoes', '').strip()

        nome_cartao = request.form.get('nome_cartao', '').strip()
        numero_cartao = request.form.get('numero_cartao', '').strip()
        validade_cartao = request.form.get('validade_cartao', '').strip()
        cvv_cartao = request.form.get('cvv_cartao', '').strip()

        quantidade = request.form.get('quantidade', 1, type=int)
        if quantidade is None or quantidade < 1:
            quantidade = 1

        if not nome_responsavel or not telefone_contato or not cpf_responsavel:
            flash('Preencha o nome do responsável, o telefone de contato e o CPF para confirmar a reserva.', 'warning')
            return redirect(url_for('main.detalhe_reserva', tipo=tipo, item_id=item_id))

        if not validar_cpf(cpf_responsavel):
            flash('O CPF informado é inválido. Verifique os números digitados.', 'warning')
            return redirect(url_for('main.detalhe_reserva', tipo=tipo, item_id=item_id))

        if not nome_cartao or not validar_dados_cartao(numero_cartao, validade_cartao, cvv_cartao):
            flash('Verifique os dados do cartão de crédito: número, validade (MM/AA) e CVV.', 'warning')
            return redirect(url_for('main.detalhe_reserva', tipo=tipo, item_id=item_id))

        numero_cartao_limpo = re.sub(r'\D', '', numero_cartao)

        nova_reserva = Reserva(
            user_id=current_user.id,
            quantidade=quantidade,
            valor_total=preco_item * quantidade,
            nome_responsavel=nome_responsavel,
            telefone_contato=telefone_contato,
            cpf_responsavel=mascarar_cpf(cpf_responsavel),
            nome_cartao=nome_cartao,
            numero_cartao_final=numero_cartao_limpo[-4:],
            validade_cartao=validade_cartao,
            observacoes=observacoes or None
        )

        if tipo == 'hotel':
            data_entrada_str = request.form.get('data_entrada')
            data_saida_str = request.form.get('data_saida')

            nova_reserva.hotel_id = item_id
            if data_entrada_str:
                nova_reserva.data_entrada = datetime.strptime(data_entrada_str, '%Y-%m-%d').date()
            if data_saida_str:
                nova_reserva.data_saida = datetime.strptime(data_saida_str, '%Y-%m-%d').date()
        else:
            data_passeio_str = request.form.get('data_passeio')
            horario_passeio_str = request.form.get('horario_passeio')

            nova_reserva.experiencia_id = item_id
            if data_passeio_str:
                nova_reserva.data_passeio = datetime.strptime(data_passeio_str, '%Y-%m-%d').date()
            if horario_passeio_str:
                nova_reserva.horario_passeio = horario_passeio_str

        db.session.add(nova_reserva)
        db.session.commit()

        flash('Reserva confirmada com sucesso! Você pode acompanhar tudo no seu histórico.', 'success')
        return redirect(url_for('main.perfil_historico'))

    # 5. RENDERIZAÇÃO DO TEMPLATE (Variável preco_item adicionada ao retorno)
    return render_template('reserva.html', 
                           user=current_user, 
                           tipo=tipo, 
                           item_id=item_id, 
                           nome=item_nome,
                           imagem=item_imagem,
                           acessibilidade=acessibilidade,
                           preco_item=preco_item,
                           lat=lat,        # <-- Enviado com sucesso ao Jinja
                           lng=lng,
                           is_favorited=is_favorited)        # <-- Enviado com sucesso ao Jinja