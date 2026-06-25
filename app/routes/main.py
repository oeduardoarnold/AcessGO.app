# Importar componentes necessários do Flask
from flask import Blueprint, render_template
# Importar decorators e objetos do Flask-Login
from flask_login import login_required, current_user
from app.models.hotel import Hotel 
from app.models.experiencia import Experiencia

# Criar Blueprint para rotas principais da aplicação
# Sem url_prefix, as rotas começam diretamente da raiz (/)
main_bp = Blueprint('main', __name__)

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

@main_bp.route('/perfil')
@login_required
def perfil():
    """
    Pagina de perfil limitada a quem ja tem login na plaraforma
    """
    return render_template('perfil.html',user=current_user)

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
    
    # 1. MAPEAMENTO DE NOMES (Bento: 1-10 | Gramado: 11-20 | Porto Alegre: 21-30)
    nomes_hoteis = {
        # Bento Gonçalves
        1: "Pousada Pipas Terroir", 2: "Döra Experience", 3: "Budget Farroupilha", 4: "Hotel Bem-Te-Vi", 5: "Spa do Vinho Condomínio",
        # Gramado
        6: "Hotel Valle D’incanto", 7: "Hotel Ritta Höppner", 8: "WoodStone Gramado Hotel", 9: "Exclusive Gramado", 10: "Buona Vitta Gramado",
        # Porto Alegre
        11: "Hotel Master Cosmopolitan", 12: "Hotel Continental", 13: "Plaza São Rafael", 14: "Double Tree by Hilton", 15: "Hotel Laghetto Viverone Moinhos"
    }
    
    nomes_experiencias = {
        # Bento Gonçalves (Pontos 1-5 e Experiências 6-10)
        1: "Vale del Vino", 2: "Parque da Ovelha", 3: "Parque Temático Epopeia Italiana", 4: "Pipa Pórtico", 5: "Vale do Rio das Antas",
        6: "Faça um passeio de maria fumaça!", 7: "Conheça o preparo tradicional do chimarrão", 8: "Piquenique nos vinhedos", 9: "Viva a aventura e adrenalina com voo de balão", 10: "Experiência única no Parque Caminhos da Aventura",
        # Gramado (Pontos 11-15 e Experiências 16-20)
        11: "Lago Negro", 12: "Mini Mundo", 13: "Rua Coberta", 14: "Snowland", 15: "Museu de Cera Dreamland",
        16: "Viva o natal em gramado", 17: "Se impressione com carros antigos e classicos de Hollywood!", 18: "Experimente outro nivel de gastronomia", 19: "Parta para um dos cartões postais da Serra Gaúcha", 20: "Tire fotos na Rua Torta",
        # Porto Alegre (Pontos 21-25 e Experiências 26-30)
        21: "Orla do Guaíba", 22: "Casa de Cultura Mario Quintana", 23: "Memorial do Rio Grande do Sul", 24: "Praça da Matriz", 25: "Parque Moinhos de Vento",
        26: "Viva a atmosfera gremista!", 27: "Veleje pelo Guaíba", 28: "Explore a gastronomia local!", 29: "Assista a um espetáculo no histórico Theatro São Pedro", 30: "Entre na arte da cidade"
    }

    # 2. LÓGICA PARA HOSPEDAGENS (HOTEIS)
    if tipo == 'hotel':
        try:
            # Tenta buscar do banco de dados primeiro
            hotel = Hotel.query.get(item_id)
            item_nome = hotel.nome if hotel else nomes_hoteis.get(item_id, f"Hotel {item_id}")
        except Exception:
            # Fallback seguro caso a tabela do banco não esteja pronta
            item_nome = nomes_hoteis.get(item_id, f"Hotel {item_id}")
        
        # Mapeamento de Imagens dos Hotéis por Região e Extensão Real
        if item_id <= 5:
            item_imagem = f"images/bento/hotel{item_id}.bento.jfif"
        elif item_id >= 6 and item_id <= 10:
            # Gramado usa formatos mistos (.webp e .jpg)
            mapa_gramado_ht = {6: "gram_ht01.webp", 7: "gram_ht02.jpg", 8: "gram_ht03.jpg", 9: "gram_ht04.jpg", 10: "gram_ht05.webp"}
            item_imagem = f"images/gramado/{mapa_gramado_ht[item_id]}"
        elif item_id >= 11 and item_id <= 15:
            mapa_poa_ht = {11: "hotel1.poa.jfif", 12: "hotel2.poa.jfif", 13: "hotel3.poa.jfif", 14: "hotel4.poa.jfif", 15: "hotel5.poa.jfif"}
            item_imagem = f"images/poa/{mapa_poa_ht[item_id]}"

    # 3. LÓGICA PARA PONTOS TURÍSTICOS E EXPERIÊNCIAS
    else:  # tipo == 'experiencia'
        item_nome = nomes_experiencias.get(item_id, f"Experiência {item_id}")
        
        # Mapeamento de Imagens das Experiências por Região e Extensão Real
        if item_id <= 5:
            item_imagem = f"images/bento/ponto{item_id}.jfif"
        elif item_id <= 10:
            item_imagem = f"images/bento/exp{item_id - 5}.jfif"
        elif item_id >= 11 and item_id <= 20:
            # Gramado usa pnt_turXX com várias extensões e gramadoexpXX.jfif
            mapa_gramado_exp = {
                11: "pnt_tur01.webp", 12: "pnt_tur02.jpg", 13: "pnt_tur03.jpg", 14: "pnt_tur04.avif", 15: "pnt_tur05.jpg",
                16: "gramadoexp1.jfif", 17: "gramadoexp2.jfif", 18: "gramadoexp3.jfif", 19: "gramadoexp4.jfif", 20: "gramadoexp5.jfif"
            }
            item_imagem = f"images/gramado/{mapa_gramado_exp[item_id]}"
        elif item_id >= 21 and item_id <= 30:
            # Porto Alegre usa nomes textuais diretos (.jfif)
            mapa_poa_exp = {
                21: "orla.jfif", 22: "marioquintana.jfif", 23: "memorialrs.jfif", 24: "pracamatriz.jfif", 25: "moinhos.jfif",
                26: "arena.jfif", 27: "guaiba.jfif", 28: "rdelaboca.jfif", 29: "theatro.jfif", 30: "iberec.jfif"
            }
            item_imagem = f"images/poa/{mapa_poa_exp[item_id]}"

    # 4. RENDERIZAÇÃO DO TEMPLATE ÚNICO DE CHECKOUT
    return render_template('reserva.html', 
                           user=current_user, 
                           tipo=tipo, 
                           item_id=item_id, 
                           nome=item_nome,
                           imagem=item_imagem)