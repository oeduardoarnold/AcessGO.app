from app import db          # Importa o db configurado no __init__.py da pasta app
from app.models.cidade import Cidade
from app.models.hotel import Hotel
from app.models.experiencia import Experiencia
from app.models.acessibilidade import Acessibilidade

def popular_banco():
    print("Iniciando o povoamento do banco de dados...")
    
    # Limpa o banco antes de inserir para não duplicar dados caso rode duas vezes
    db.drop_all()
    db.create_all()

    # ==========================================
    # 1. BENTO GONÇALVES
    # ==========================================
    bento = Cidade(nome="Bento Gonçalves", estado="RS")
    db.session.add(bento)
    db.session.commit()

    # Hotéis - Bento (Adicionado preco, latitude e longitude)
    hoteis_bento = [
        Hotel(nome="Pousada Pipas Terroir", descricao="Hospedagem charmosa em pipas de vinho.", cidade_id=bento.id, endereco="Vale dos Vinhedos", telefone="(54) 9999-0001", preco=350.00, latitude=-29.1723, longitude=-51.5645),
        Hotel(nome="Döra Experience", descricao="Cabanas modernas e imersivas.", cidade_id=bento.id, endereco="Linha Leopoldina", telefone="(54) 9999-0002", preco=420.00, latitude=-29.1654, longitude=-51.5712),
        Hotel(nome="Budget Farroupilha", descricao="Hotel prático e econômico.", cidade_id=bento.id, endereco="Centro", telefone="(54) 9999-0003", preco=180.00, latitude=-29.1691, longitude=-51.5184),
        Hotel(nome="Hotel Bem-Te-Vi", descricao="Acolhedor e cercado pela natureza.", cidade_id=bento.id, endereco="Caminhos de Pedra", telefone="(54) 9999-0004", preco=260.00, latitude=-29.1022, longitude=-51.5039),
        Hotel(nome="Spa do Vinho Condomínio", descricao="Hotel de luxo e bem-estar no vale.", cidade_id=bento.id, endereco="Vale dos Vinhedos", telefone="(54) 9999-0005", preco=680.00, latitude=-29.1785, longitude=-51.5548)
    ]
    db.session.add_all(hoteis_bento)
    db.session.commit()

    # Acessibilidade Real dos Hotéis de Bento
    db.session.add_all([
        Acessibilidade(hotel_id=hoteis_bento[0].id, rampa=False, elevador=False, banheiro_acessivel=False),
        Acessibilidade(hotel_id=hoteis_bento[1].id, rampa=True, elevador=False, banheiro_acessivel=True),
        Acessibilidade(hotel_id=hoteis_bento[2].id, rampa=True, elevador=True, banheiro_acessivel=True),
        Acessibilidade(hotel_id=hoteis_bento[3].id, rampa=False, elevador=False, banheiro_acessivel=False),
        Acessibilidade(hotel_id=hoteis_bento[4].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=True)
    ])
    db.session.commit()

    # Pontos Turísticos e Experiências - Bento (Adicionado preco, latitude e longitude)
    db.session.add_all([
        # Pontos Turísticos
        Experiencia(nome="Vale del Vino", descricao="Vinícolas e belas paisagens.", cidade_id=bento.id, categoria="Ponto Turistico", preco=0.00, latitude=-29.1687, longitude=-51.5492),
        Experiencia(nome="Parque da Ovelha", descricao="Vivência da rotina de uma fazenda.", cidade_id=bento.id, categoria="Ponto Turistico", preco=90.00, latitude=-29.1009, longitude=-51.5025),
        Experiencia(nome="Parque Temático Epopeia Italiana", descricao="Espetáculo teatral sobre a imigração.", cidade_id=bento.id, categoria="Ponto Turistico", preco=35.00, latitude=-29.1632, longitude=-51.5273),
        Experiencia(nome="Pipa Pórtico", descricao="Entrada principal da cidade em formato de pipa.", cidade_id=bento.id, categoria="Ponto Turistico", preco=0.00, latitude=-29.1869, longitude=-51.5147),
        Experiencia(nome="Vale do Rio das Antas", descricao="Mirantes e paisagens exuberantes.", cidade_id=bento.id, categoria="Ponto Turistico", preco=0.00, latitude=-29.0558, longitude=-51.5342),
        # Experiências
        Experiencia(nome="Faça um passeio de maria fumaça!", descricao="Passeio de trem a vapor com música e degustação.", cidade_id=bento.id, categoria="Experiencia", preco=178.00, latitude=-29.1630, longitude=-51.5271),
        Experiencia(nome="Conheça o preparo tradicional do chimarrão", descricao="Aprenda a fazer a bebida típica dos gaúchos.", cidade_id=bento.id, categoria="Experiencia", preco=0.00, latitude=-29.1699, longitude=-51.5178),
        Experiencia(nome="Piquenique nos vinhedos", descricao="Tarde relaxante com frios e vinhos locais.", cidade_id=bento.id, categoria="Experiencia", preco=120.00, latitude=-29.1752, longitude=-51.5583),
        Experiencia(nome="Viva a aventura e adrenalina com voo de balão", descricao="Vista panorâmica incrível da região.", cidade_id=bento.id, categoria="Experiencia", preco=450.00, latitude=-29.1583, longitude=-51.5050),
        Experiencia(nome="Experiência única no Parque Caminhos da Aventura", descricao="Atividades ao ar livre e ecoturismo.", cidade_id=bento.id, categoria="Experiencia", preco=60.00, latitude=-29.0711, longitude=-51.4872)
    ])


    # ==========================================
    # 2. GRAMADO
    # ==========================================
    gramado = Cidade(nome="Gramado", estado="RS")
    db.session.add(gramado)
    db.session.commit()

    # Hotéis - Gramado (Adicionado preco, latitude e longitude)
    hoteis_gramado = [
        Hotel(nome="Hotel Valle D’incanto", descricao="Considerado um dos hotéis mais românticos.", cidade_id=gramado.id, endereco="Av. Borges de Medeiros", telefone="(54) 8888-0001", preco=550.00, latitude=-29.3621, longitude=-50.8647),
        Hotel(nome="Hotel Ritta Höppner", descricao="Tradicional, charmoso e com chalés.", cidade_id=gramado.id, endereco="Planalto", telefone="(54) 8888-0002", preco=490.00, latitude=-29.3828, longitude=-50.8793),
        Hotel(nome="WoodStone Gramado Hotel", descricao="Design moderno em madeira e pedra.", cidade_id=gramado.id, endereco="Centro", telefone="(54) 8888-0003", preco=380.00, latitude=-29.3754, longitude=-50.8711),
        Hotel(nome="Exclusive Gramado", descricao="Conforto e sofisticação com bandeira Atlantica.", cidade_id=gramado.id, endereco="Av. das Hortênsias", telefone="(54) 8888-0004", preco=420.00, latitude=-29.3663, longitude=-50.8592),
        Hotel(nome="Buona Vitta Gramado", descricao="Inspirado na região da Toscana, Itália.", cidade_id=gramado.id, endereco="Estrada da Carazal", telefone="(54) 8888-0005", preco=620.00, latitude=-29.3951, longitude=-50.8936)
    ]
    db.session.add_all(hoteis_gramado)
    db.session.commit()

    # Acessibilidade Real dos Hotéis de Gramado
    db.session.add_all([
        Acessibilidade(hotel_id=hoteis_gramado[0].id, rampa=True, elevador=True, banheiro_acessivel=True),
        Acessibilidade(hotel_id=hoteis_gramado[1].id, rampa=True, elevador=True, banheiro_acessivel=True),
        Acessibilidade(hotel_id=hoteis_gramado[2].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=True),
        Acessibilidade(hotel_id=hoteis_gramado[3].id, rampa=True, elevador=True, banheiro_acessivel=True, piso_tatil=True, braille=True),
        Acessibilidade(hotel_id=hoteis_gramado[4].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=True)
    ])
    db.session.commit()

    # Pontos Turísticos e Experiências - Gramado (Adicionado preco, latitude e longitude)
    db.session.add_all([
        # Pontos Turísticos
        Experiencia(nome="Lago Negro", descricao="Lago artificial cercado por árvores da Floresta Negra.", cidade_id=gramado.id, categoria="Ponto Turistico", preco=0.00, latitude=-29.3923, longitude=-50.8847),
        Experiencia(nome="Mini Mundo", descricao="Parque de miniaturas detalhadas ao ar livre.", cidade_id=gramado.id, categoria="Ponto Turistico", preco=56.00, latitude=-29.3815, longitude=-50.8781),
        Experiencia(nome="Rua Coberta", descricao="Centro gastronômico e de compras coberto.", cidade_id=gramado.id, categoria="Ponto Turistico", preco=0.00, latitude=-29.3751, longitude=-50.8741),
        Experiencia(nome="Snowland", descricao="Primeiro parque de neve indoor das Américas.", cidade_id=gramado.id, categoria="Ponto Turistico", preco=169.00, latitude=-29.4011, longitude=-50.9169),
        Experiencia(nome="Museu de Cera Dreamland", descricao="Réplicas de cera de ícones da cultura pop.", cidade_id=gramado.id, categoria="Ponto Turistico", preco=90.00, latitude=-29.3524, longitude=-50.8449),
        # Experiências
        Experiencia(nome="Viva o natal em gramado", descricao="Espetáculos lúdicos e iluminação do Natal Luz.", cidade_id=gramado.id, categoria="Experiencia", preco=0.00, latitude=-29.3732, longitude=-50.8765),
        Experiencia(nome="Se impressione com carros antigos e clássicos de Hollywood!", descricao="Visita ao Hollywood Dream Cars.", cidade_id=gramado.id, categoria="Experiencia", preco=80.00, latitude=-29.3562, longitude=-50.8493),
        Experiencia(nome="Experimente outro nível de gastronomia", descricao="O tradicional rodízio de fondue de Gramado.", cidade_id=gramado.id, categoria="Experiencia", preco=140.00, latitude=-29.3768, longitude=-50.8725),
        Experiencia(nome="Parta para um dos cartões postais da Serra Gaúcha", descricao="Igreja Matriz São Pedro.", cidade_id=gramado.id, categoria="Experiencia", preco=0.00, latitude=-29.3752, longitude=-50.8732),
        Experiencia(nome="Tire fotos na Rua Torta", descricao="A famosa rua sinuosa e cheia de flores.", cidade_id=gramado.id, categoria="Experiencia", preco=0.00, latitude=-29.3789, longitude=-50.8762)
    ])


    # ==========================================
    # 3. PORTO ALEGRE
    # ==========================================
    poa = Cidade(nome="Porto Alegre", estado="RS")
    db.session.add(poa)
    db.session.commit()

    # Hotéis - Porto Alegre (Adicionado preco, latitude e longitude)
    hoteis_poa = [
        Hotel(nome="Hotel Master Cosmopolitan", descricao="Excelente localização no bairro Moinhos de Vento.", cidade_id=poa.id, endereco="Bairro Moinhos", telefone="(51) 7777-0001", preco=290.00, latitude=-30.0245, longitude=-51.2012),
        Hotel(nome="Hotel Continental", descricao="Tradicional e próximo ao centro histórico.", cidade_id=poa.id, endereco="Largo Vespasiano", telefone="(51) 7777-0002", preco=240.00, latitude=-30.0232, longitude=-51.2189),
        Hotel(nome="Plaza São Rafael", descricao="Clássico da hotelaria gaúcha com águas termais.", cidade_id=poa.id, endereco="Av. Alberto Bins", telefone="(51) 7777-0003", preco=310.00, latitude=-30.0271, longitude=-51.2215),
        Hotel(nome="Double Tree by Hilton", descricao="Moderno e com vista deslumbrante para o Guaíba.", cidade_id=poa.id, endereco="Av. Padre Cacique", telefone="(51) 7777-0004", preco=450.00, latitude=-30.0556, longitude=-51.2384),
        Hotel(nome="Hotel Laghetto Viverone Moinhos", descricao="Fusão de casarão histórico com torre moderna.", cidade_id=poa.id, endereco="Moinhos de Vento", telefone="(51) 7777-0005", preco=380.00, latitude=-30.0229, longitude=-51.2057)
    ]
    db.session.add_all(hoteis_poa)
    db.session.commit()

    # Acessibilidade Real dos Hotéis de Porto Alegre
    db.session.add_all([
        Acessibilidade(hotel_id=hoteis_poa[0].id, rampa=True, elevador=True, banheiro_acessivel=True, braille=True),
        Acessibilidade(hotel_id=hoteis_poa[1].id, rampa=True, elevador=True, banheiro_acessivel=True),
        Acessibilidade(hotel_id=hoteis_poa[2].id, rampa=True, elevador=True, banheiro_acessivel=True, piso_tatil=True),
        Acessibilidade(hotel_id=hoteis_poa[3].id, rampa=True, elevador=True, banheiro_acessivel=True, braille=True, sinalizacao_visual=True),
        Acessibilidade(hotel_id=hoteis_poa[4].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=True)
    ])
    db.session.commit()

    # Pontos Turísticos e Experiências - Porto Alegre (Adicionado preco, latitude e longitude)
    db.session.add_all([
        # Pontos Turísticos
        Experiencia(nome="Orla do Guaíba", descricao="Revitalizada, ótima para caminhadas e ver o pôr do sol.", cidade_id=poa.id, categoria="Ponto Turistico", preco=0.00, latitude=-30.0368, longitude=-51.2421),
        Experiencia(nome="Casa de Cultura Mario Quintana", descricao="Antigo hotel transformado em centro cultural contendo acervos.", cidade_id=poa.id, categoria="Ponto Turistico", preco=0.00, latitude=-30.0326, longitude=-51.2344),
        Experiencia(nome="Memorial do Rio Grande do Sul", descricao="Preservação da história e cultura do estado.", cidade_id=poa.id, categoria="Ponto Turistico", preco=0.00, latitude=-30.0295, longitude=-51.2292),
        Experiencia(nome="Praça Marechal Deodoro (Praça da Matriz)", descricao="Coração político e histórico da capital.", cidade_id=poa.id, categoria="Ponto Turistico", preco=0.00, latitude=-30.0339, longitude=-51.2301),
        Experiencia(nome="Parque Moinhos de Vento", descricao="Conhecido como Parcão, ideal para lazer.", cidade_id=poa.id, categoria="Ponto Turistico", preco=0.00, latitude=-30.0248, longitude=-51.2039),
        # Experiências
        Experiencia(nome="Viva a atmosfera gremista!", descricao="Visita guiada ou dia de jogo na Arena do Grêmio.", cidade_id=poa.id, categoria="Experiencia", preco=40.00, latitude=-29.9741, longitude=-51.1948),
        Experiencia(nome="Veleje pelo Guaíba", descricao="Passeio de barco pegando a brisa da lagoa.", cidade_id=poa.id, categoria="Experiencia", preco=65.00, latitude=-30.0345, longitude=-51.2443),
        Experiencia(nome="Explore a gastronomia local!", descricao="Churrascarias tradicionais da capital gaúcha.", cidade_id=poa.id, categoria="Experiencia", preco=0.00, latitude=-30.0291, longitude=-51.2078),
        Experiencia(nome="Assista a um espetáculo no histórico Theatro São Pedro", descricao="Um dos palcos mais antigos e imponentes.", cidade_id=poa.id, categoria="Experiencia", preco=50.00, latitude=-30.0333, longitude=-51.2309),
        Experiencia(nome="Entre na arte da cidade", descricao="Visita à Fundação Iberê Camargo.", cidade_id=poa.id, categoria="Experiencia", preco=0.00, latitude=-30.0801, longitude=-51.2486)
    ])

    # Salva de forma definitiva no Banco tudo o que sobreu pendente
    db.session.commit()
    print("Banco de dados povoado com sucesso!")

if __name__ == "__main__":
    from app import create_app  # Ou apenas 'from app import app' dependendo de como está seu __init__.py
    
    # Se o seu __init__.py usa uma função (ex: create_app()):
    app = create_app()
    
    with app.app_context():
        popular_banco()