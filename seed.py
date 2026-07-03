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
        Hotel(nome="Pousada Pipas Terroir", descricao="Hospedagem charmosa em pipas de vinho.", cidade_id=bento.id, endereco="Vale dos Vinhedos", telefone="(54) 9999-0001", preco=1350.00, latitude=-29.1764, longitude=-51.5727),
        Hotel(nome="Döra Experience", descricao="Cabanas modernas e imersivas.", cidade_id=bento.id, endereco="Linha Leopoldina", telefone="(54) 9999-0002", preco=420.00, latitude=-29.1670, longitude=-51.5583),
        Hotel(nome="Budget Farroupilha", descricao="Hotel prático e econômico.", cidade_id=bento.id, endereco="Centro", telefone="(54) 9999-0003", preco=215.00, latitude=-29.221822, longitude=-51.334116),
        Hotel(nome="Hotel Bem-Te-Vi", descricao="Acolhedor e cercado pela natureza.", cidade_id=bento.id, endereco="Caminhos de Pedra", telefone="(54) 9999-0004", preco=260.00, latitude=-29.173626, longitude=-51.344823),
        Hotel(nome="Spa do Vinho Condomínio", descricao="Hotel de luxo e bem-estar no vale.", cidade_id=bento.id, endereco="Vale dos Vinhedos", telefone="(54) 9999-0005", preco=680.00, latitude=-29.186916, longitude=-51.580977)
    ]
    db.session.add_all(hoteis_bento)
    db.session.commit()

    # Acessibilidade Real dos Hotéis de Bento
    db.session.add_all([
        Acessibilidade(hotel_id=hoteis_bento[0].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(hotel_id=hoteis_bento[1].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(hotel_id=hoteis_bento[2].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(hotel_id=hoteis_bento[3].id, rampa=False, elevador=False, banheiro_acessivel=False, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(hotel_id=hoteis_bento[4].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=True, piso_tatil=False, braille=False)
    ])
    db.session.commit()

    # Pontos Turísticos e Experiências - Bento (Colocado em lista para capturar IDs)
    exps_bento = [
        # Pontos Turísticos
        Experiencia(nome="Vale del Vino", descricao="Vinícolas e belas paisagens.", cidade_id=bento.id, categoria="Ponto Turistico", preco=0.00, latitude=-29.166969, longitude=-51.517234),
        Experiencia(nome="Parque da Ovelha", descricao="Vivência da rotina de uma fazenda.", cidade_id=bento.id, categoria="Ponto Turistico", preco=90.00, latitude=-29.176599, longitude=-51.432329),
        Experiencia(nome="Parque Temático Epopeia Italiana", descricao="Espetáculo teatral sobre a imigração.", cidade_id=bento.id, categoria="Ponto Turistico", preco=35.00, latitude=-29.172771, longitude=-51.518435),
        Experiencia(nome="Pipa Pórtico", descricao="Entrada principal da cidade em formato de pipa.", cidade_id=bento.id, categoria="Ponto Turistico", preco=0.00, latitude=-29.174589, longitude=-51.521786),
        Experiencia(nome="Belvedere Vale Das Antas", descricao="Mirantes e paisagens exuberantes.", cidade_id=bento.id, categoria="Ponto Turistico", preco=0.00, latitude=-29.050711, longitude=-51.582610),
        # Experiências
        Experiencia(nome="Maria fumaça (Trem do Vinho)", descricao="Passeio de trem a vapor com música e degustação.", cidade_id=bento.id, categoria="Experiencia", preco=178.00, latitude=-29.173507, longitude=-51.517621),
        Experiencia(nome="Casa da Erva Mate", descricao="Aprenda a fazer a bebida típica dos gaúchos.", cidade_id=bento.id, categoria="Experiencia", preco=0.00, latitude=-29.177126, longitude=-51.407422),
        Experiencia(nome="Complexo Turistico Casa Valduga", descricao="Tarde relaxante com frios e vinhos locais.", cidade_id=bento.id, categoria="Experiencia", preco=120.00, latitude=-29.179754, longitude=-51.5566399),
        Experiencia(nome="Vinícula Miolo", descricao="Vista panorâmica incrível da região.", cidade_id=bento.id, categoria="Experiencia", preco=450.00, latitude=-29.184122, longitude=-51.582642),
        Experiencia(nome="Parque Caminhos da Aventura", descricao="Atividades ao ar livre e ecoturismo.", cidade_id=bento.id, categoria="Experiencia", preco=60.00, latitude=-29.175126, longitude=-51.427737)
    ]
    db.session.add_all(exps_bento)
    db.session.commit()

    # Acessibilidade das Experiências de Bento
    db.session.add_all([
        # exps_bento[1] é o "Parque da Ovelha"
        Acessibilidade(experiencia_id=exps_bento[1].id, rampa=True, elevador=False, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(experiencia_id=exps_bento[2].id, rampa=True, elevador=False, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(experiencia_id=exps_bento[4].id, rampa=True, elevador=False, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(experiencia_id=exps_bento[5].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(experiencia_id=exps_bento[6].id, rampa=True, elevador=False, banheiro_acessivel=True, sinalizacao_visual=True, piso_tatil=False, braille=True),
        Acessibilidade(experiencia_id=exps_bento[7].id, rampa=True, elevador=False, banheiro_acessivel=True, sinalizacao_visual=True, piso_tatil=False, braille=True),
        Acessibilidade(experiencia_id=exps_bento[8].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(experiencia_id=exps_bento[9].id, rampa=True, elevador=False, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False)
    ])
    db.session.commit()


    # ==========================================
    # 2. GRAMADO
    # ==========================================
    gramado = Cidade(nome="Gramado", estado="RS")
    db.session.add(gramado)
    db.session.commit()

    # Hotéis - Gramado (Adicionado preco, latitude e longitude)
    hoteis_gramado = [
        Hotel(nome="Hotel Valle D’incanto", descricao="Considerado um dos hotéis mais românticos.", cidade_id=gramado.id, endereco="Av. Borges de Medeiros", telefone="(54) 8888-0001", preco=550.00, latitude=-29.365108, longitude=-50.858427),
        Hotel(nome="Hotel Ritta Höppner", descricao="Tradicional, charmoso e com chalés.", cidade_id=gramado.id, endereco="Planalto", telefone="(54) 8888-0002", preco=490.00, latitude=-29.384691, longitude=-50.876620),
        Hotel(nome="WoodStone Gramado Hotel", descricao="Design moderno em madeira e pedra.", cidade_id=gramado.id, endereco="Centro", telefone="(54) 8888-0003", preco=380.00, latitude=-29.355266, longitude=-50.885899),
        Hotel(nome="Exclusive Gramado", descricao="Conforto e sofisticação com bandeira Atlantica.", cidade_id=gramado.id, endereco="Av. das Hortênsias", telefone="(54) 8888-0004", preco=420.00, latitude=-29.366573, longitude=-50.860135),
        Hotel(nome="Buona Vitta Gramado", descricao="Inspirado na região da Toscana, Itália.", cidade_id=gramado.id, endereco="Estrada da Carazal", telefone="(54) 8888-0005", preco=620.00, latitude=-29.366294, longitude=-50.858040)
    ]
    db.session.add_all(hoteis_gramado)
    db.session.commit()

    # Acessibilidade Real dos Hotéis de Gramado
    db.session.add_all([
        Acessibilidade(hotel_id=hoteis_gramado[0].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(hotel_id=hoteis_gramado[1].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(hotel_id=hoteis_gramado[2].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=True, piso_tatil=False, braille=False),
        Acessibilidade(hotel_id=hoteis_gramado[3].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=True, braille=True),
        Acessibilidade(hotel_id=hoteis_gramado[4].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=True, piso_tatil=False, braille=False)
    ])
    db.session.commit()

    # Pontos Turísticos e Experiências - Gramado (Colocado em lista para capturar IDs)
    exps_gramado = [
        # Pontos Turísticos
        Experiencia(nome="Lago Negro", descricao="Lago artificial cercado por árvores da Floresta Negra.", cidade_id=gramado.id, categoria="Ponto Turistico", preco=0.00, latitude=-29.395, longitude=-50.8761),
        Experiencia(nome="Mini Mundo", descricao="Parque de miniaturas detalhadas ao ar livre.", cidade_id=gramado.id, categoria="Ponto Turistico", preco=56.00, latitude=-29.384296, longitude=-50.875917),
        Experiencia(nome="Rua Coberta", descricao="Centro gastronômico e de compras coberto.", cidade_id=gramado.id, categoria="Ponto Turistico", preco=0.00, latitude=-29.378725, longitude=-50.873594),
        Experiencia(nome="Snowland", descricao="Primeiro parque de neve indoor das Américas.", cidade_id=gramado.id, categoria="Ponto Turistico", preco=169.00, latitude=-29.344159, longitude=-50.922031),
        Experiencia(nome="Museu de Cera Dreamland", descricao="Réplicas de cera de ícones da cultura pop.", cidade_id=gramado.id, categoria="Ponto Turistico", preco=90.00, latitude=-29.361147, longitude=-50.848640),
        # Experiências
        Experiencia(nome="Avenida Borges de Medeiros", descricao="Espetáculos lúdicos e iluminação do Natal Luz.", cidade_id=gramado.id, categoria="Experiencia", preco=0.00, latitude=-29.385462, longitude=-50.873908),
        Experiencia(nome="Hollywood Dream Cars", descricao="Visita ao Hollywood Dream Cars.", cidade_id=gramado.id, categoria="Experiencia", preco=80.00, latitude=-29.365697, longitude=-50.859772),
        Experiencia(nome="Cuccina Boniatto", descricao="A comida italina da serra gaúcha.", cidade_id=gramado.id, categoria="Experiencia", preco=140.00, latitude=-29.385618, longitude=-50.874234),
        Experiencia(nome="Igreja Matriz São Pedro", descricao="Igreja Matriz São Pedro.", cidade_id=gramado.id, categoria="Experiencia", preco=0.00, latitude=-29.379762, longitude=-50.874564),
        Experiencia(nome="Tire fotos na Rua Torta", descricao="A famosa rua sinuosa e cheia de flores.", cidade_id=gramado.id, categoria="Experiencia", preco=0.00, latitude=-29.3789, longitude=-50.8762)
    ]
    db.session.add_all(exps_gramado)
    db.session.commit()

    # Acessibilidade das Experiências de Gramado
    db.session.add_all([
        # exps_gramado[1] é o "Mini Mundo"
        Acessibilidade(experiencia_id=exps_gramado[1].id, rampa=True, elevador=False, banheiro_acessivel=True, sinalizacao_visual=True, piso_tatil=False, braille=True),
        Acessibilidade(experiencia_id=exps_gramado[3].id, rampa=True, elevador=True, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(experiencia_id=exps_gramado[4].id, rampa=True, elevador=False, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(experiencia_id=exps_gramado[6].id, rampa=True, elevador=False, banheiro_acessivel=True, sinalizacao_visual=False, piso_tatil=False, braille=False),
        Acessibilidade(experiencia_id=exps_gramado[7].id, rampa=True, elevador=False, banheiro_acessivel=True, sinalizacao_visual=True, piso_tatil=False, braille=True),
        
    ])
    db.session.commit()


    # ==========================================
    # 3. PORTO ALEGRE
    # ==========================================
    poa = Cidade(nome="Porto Alegre", estado="RS")
    db.session.add(poa)
    db.session.commit()

    # Hotéis - Porto Alegre (Adicionado preco, latitude e longitude)
    hoteis_poa = [
        Hotel(nome="Hotel Master Cosmopolitan", descricao="Excelente localização no bairro Moinhos de Vento.", cidade_id=poa.id, endereco="Bairro Moinhos", telefone="(51) 7777-0001", preco=290.00, latitude=-30.019142, longitude=-51.202192),
        Hotel(nome="Hotel Continental", descricao="Tradicional e próximo ao centro histórico.", cidade_id=poa.id, endereco="Largo Vespasiano", telefone="(51) 7777-0002", preco=240.00, latitude=-30.023598, longitude=-51.218458),
        Hotel(nome="Plaza São Rafael", descricao="Clássico da hotelaria gaúcha com águas termais.", cidade_id=poa.id, endereco="Av. Alberto Bins", telefone="(51) 7777-0003", preco=310.00, latitude=-30.028051, longitude=-51.221330),
        Hotel(nome="Double Tree by Hilton", descricao="Moderno e com vista deslumbrante para o Guaíba.", cidade_id=poa.id, endereco="Av. Padre Cacique", telefone="(51) 7777-0004", preco=450.00, latitude=-30.079790, longitude=-51.248368),
        Hotel(nome="Hotel Laghetto Viverone Moinhos", descricao="Fusão de casarão histórico com torre moderna.", cidade_id=poa.id, endereco="Moinhos de Vento", telefone="(51) 7777-0005", preco=380.00, latitude=-30.027110, longitude=-51.206295)
    ]
    db.session.add_all(hoteis_poa)
    db.session.commit()

    # Acessibilidade Real dos Hotéis de Porto Alegre
    db.session.add_all([
        Acessibilidade(hotel_id=hoteis_poa[0].id, rampa=True, elevador=True, banheiro_acessivel=True, braille=True, sinalizacao_visual=True, piso_tatil=True),
        Acessibilidade(hotel_id=hoteis_poa[1].id, rampa=True, elevador=True, banheiro_acessivel=True, braille=False, sinalizacao_visual=False, piso_tatil=False),
        Acessibilidade(hotel_id=hoteis_poa[2].id, rampa=True, elevador=True, banheiro_acessivel=True, braille=False, sinalizacao_visual=False, piso_tatil=True),
        Acessibilidade(hotel_id=hoteis_poa[3].id, rampa=True, elevador=True, banheiro_acessivel=True, braille=True, sinalizacao_visual=True, piso_tatil=False),
        Acessibilidade(hotel_id=hoteis_poa[4].id, rampa=True, elevador=True, banheiro_acessivel=True, braille=False, sinalizacao_visual=True, piso_tatil=False)
    ])
    db.session.commit()

    # Pontos Turísticos e Experiências - Porto Alegre (Colocado em lista para capturar IDs)
    exps_poa = [
        # Pontos Turísticos
        Experiencia(nome="Orla do Guaíba", descricao="Revitalizada, ótima para caminhadas e ver o pôr do sol.", cidade_id=poa.id, categoria="Ponto Turistico", preco=0.00, latitude=-30.055655, longitude=-51.233814),
        Experiencia(nome="Casa de Cultura Mario Quintana", descricao="Antigo hotel transformado em centro cultural contendo acervos.", cidade_id=poa.id, categoria="Ponto Turistico", preco=0.00, latitude=-30.030967, longitude=-51.234467),
        Experiencia(nome="Memorial do Rio Grande do Sul", descricao="Preservação da história e cultura do estado.", cidade_id=poa.id, categoria="Ponto Turistico", preco=0.00, latitude=-30.028419, longitude=-51.230975),
        Experiencia(nome="Praça Marechal Deodoro (Praça da Matriz)", descricao="Coração político e histórico da capital.", cidade_id=poa.id, categoria="Ponto Turistico", preco=0.00, latitude=-30.032848, longitude=-51.230231),
        Experiencia(nome="Parque Moinhos de Vento", descricao="Conhecido como Parcão, ideal para lazer.", cidade_id=poa.id, categoria="Ponto Turistico", preco=0.00, latitude=-30.026756, longitude=-51.200683),
        # Experiências
        Experiencia(nome="Arena do Grêmio", descricao="Visita na Arena do Grêmio.", cidade_id=poa.id, categoria="Experiencia", preco=40.00, latitude=-29.973823, longitude=-51.194850),
        Experiencia(nome="Veleje no Guaíba", descricao="Passeio de barco pegando a brisa da lagoa.", cidade_id=poa.id, categoria="Experiencia", preco=65.00, latitude=-30.097162, longitude=-51.256186),
        Experiencia(nome="Churrascaria Santo Antônio.", descricao="Experiência de churrasco em um ambiente acolhedor.", cidade_id=poa.id, categoria="Experiencia", preco=0.00, latitude=-30.018058, longitude=-51.201348),
        Experiencia(nome="Theatro São Pedro", descricao="Um dos palcos mais antigos e imponentes.", cidade_id=poa.id, categoria="Experiencia", preco=50.00, latitude=-30.0311797, longitude=-51.230478),
        Experiencia(nome="Fundação Iberê Camargo", descricao="Fundação Iberê Camargo.", cidade_id=poa.id, categoria="Experiencia", preco=0.00, latitude=-30.077559, longitude=-51.245748)
    ]
    db.session.add_all(exps_poa)
    db.session.commit()

    # Acessibilidade das Experiências de Porto Alegre
    db.session.add_all([
        # exps_poa[0] é a "Orla do Guaíba"
        Acessibilidade(experiencia_id=exps_poa[0].id, rampa=True, elevador=False, banheiro_acessivel=True, braille=False, sinalizacao_visual=True, piso_tatil=True),
        # exps_poa[1] é a "Casa de Cultura Mario Quintana"
        Acessibilidade(experiencia_id=exps_poa[1].id, rampa=True, elevador=True, banheiro_acessivel=True, braille=True, sinalizacao_visual=True, piso_tatil=True),
        Acessibilidade(experiencia_id=exps_poa[2].id, rampa=True, elevador=True, banheiro_acessivel=True, braille=True, sinalizacao_visual=True, piso_tatil=True),
        Acessibilidade(experiencia_id=exps_poa[5].id, rampa=True, elevador=True, banheiro_acessivel=True, braille=True, sinalizacao_visual=True, piso_tatil=True),
        Acessibilidade(experiencia_id=exps_poa[6].id, rampa=True, elevador=False, banheiro_acessivel=False, braille=False, sinalizacao_visual=False, piso_tatil=False),
        Acessibilidade(experiencia_id=exps_poa[7].id, rampa=True, elevador=False, banheiro_acessivel=True, braille=True, sinalizacao_visual=True, piso_tatil=False),
        Acessibilidade(experiencia_id=exps_poa[8].id, rampa=True, elevador=True, banheiro_acessivel=True, braille=True, sinalizacao_visual=True, piso_tatil=True),
        Acessibilidade(experiencia_id=exps_poa[9].id, rampa=True, elevador=True, banheiro_acessivel=True, braille=True, sinalizacao_visual=True, piso_tatil=True)
    ])
    db.session.commit()

    print("Banco de dados povoado com sucesso!")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    
    with app.app_context():
        popular_banco()