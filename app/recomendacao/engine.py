PESOS_PADRAO = {
    "preco": 0.45,
    "localizacao": 0.45,
}

BONUS_ACESSIBILIDADE = 0.10  # peso extra, fora dos 100% base

CAMPOS_ACESSIBILIDADE = [
    "rampa", "elevador", "banheiro_acessivel",
    "piso_tatil", "braille", "sinalizacao_visual", "sinalizacao_auditiva",
]


def atende_acessibilidade(entidade, requisitos):
    """
    Filtro RÍGIDO: funciona tanto para Hotel quanto para Experiencia,
    já que ambos têm `.acessibilidade` (relationship uselist=False).
    """
    if not requisitos:
        return True
    acess = entidade.acessibilidade
    if acess is None:
        return False
    return all(getattr(acess, campo, False) for campo in requisitos)


def score_acessibilidade_extra(entidade):
    acess = entidade.acessibilidade
    if acess is None:
        return 0.0
    total = sum(1 for c in CAMPOS_ACESSIBILIDADE if getattr(acess, c, False))
    return total / len(CAMPOS_ACESSIBILIDADE)


def score_preco(entidade, preco_max):
    if not preco_max or not entidade.preco:
        return 0.5
    if entidade.preco <= preco_max:
        return 1 - (float(entidade.preco) / float(preco_max)) * 0.5
    return 0.0


def score_localizacao(entidade, cidade_id):
    if not cidade_id:
        return 0.5
    return 1.0 if entidade.cidade_id == int(cidade_id) else 0.0


def calcular_score(entidade, preferencias):
    s_preco = score_preco(entidade, preferencias.get("preco_max"))
    s_local = score_localizacao(entidade, preferencias.get("cidade_id"))
    s_acess = score_acessibilidade_extra(entidade)

    score_base = (
        s_preco * PESOS_PADRAO["preco"]
        + s_local * PESOS_PADRAO["localizacao"]
    )
    return round(score_base + s_acess * BONUS_ACESSIBILIDADE, 4)


def recomendar(entidades, preferencias, top_n=10):
    """
    Genérico: aceita queryset de Hotel OU Experiencia,
    desde que tenham .preco, .cidade_id e .acessibilidade.
    """
    requisitos = preferencias.get("acessibilidade", [])
    candidatos = [e for e in entidades if atende_acessibilidade(e, requisitos)]
    resultados = [(e, calcular_score(e, preferencias)) for e in candidatos]
    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados[:top_n]