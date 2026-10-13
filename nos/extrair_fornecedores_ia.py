import json
import re
import requests
from typing import Dict, Any, List
from estado import EstadoReposicao


def extrair_fornecedores_ia(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 3: Extrai e estrutura os dados reais do Google Places (Serper).
    Preserva rigorosamente a cidade, notas reais e links de cada fornecedor encontrado.
    """
    nome_produto = estado["nome_produto"]
    texto_web = estado.get("resultados_web_brutos", "")
    localizacao = estado.get("localizacao_usuario", "").strip() or "São Paulo - SP"
    avisos = list(estado.get("avisos", []))

    lugares_google = []
    try:
        if texto_web and texto_web.strip().startswith("["):
            lugares_google = json.loads(texto_web)
    except Exception:
        lugares_google = []

    fornecedores_base = []
    for idx, p in enumerate(lugares_google[:6], start=1):
        nome = p.get("title", f"Distribuidora {nome_produto}")
        endereco = p.get("address", localizacao)
        lat = p.get("latitude")
        lon = p.get("longitude")
        rating = p.get("rating")
        rating_count = p.get("ratingCount")
        try:
            rating = float(rating) if rating is not None else None
        except (TypeError, ValueError):
            rating = None
        try:
            rating_count = int(rating_count) if rating_count is not None else None
        except (TypeError, ValueError):
            rating_count = None
        link = p.get("website") or f"https://www.google.com/maps/search/?api=1&query={requests.utils.quote(nome + ' ' + localizacao)}"

        # Descobre a cidade pelo endereço ou usa a digitada
        cidade_forn = localizacao
        if "," in endereco:
            partes = [pt.strip() for pt in endereco.split(",")]
            if len(partes) >= 2:
                cidade_forn = partes[-2]

        fornecedores_base.append({
            "id_fornecedor": idx,
            "nome_fornecedor": nome,
            "endereco_completo": endereco,
            "latitude": lat,
            "longitude": lon,
            "cidade": cidade_forn,
            "link": link,
            "quantidade_avaliacoes": rating_count,
            "nota_media": rating,
            "nome_produto": nome_produto,
        })

    # Não inventa um fornecedor quando o Serper não respondeu com locais reais.
    if not fornecedores_base:
        avisos.append(
            f"Nenhum fornecedor real foi retornado pelo Serper para '{localizacao}'."
        )

    return {
        "fornecedores_encontrados": fornecedores_base,
        "avisos": avisos,
    }
