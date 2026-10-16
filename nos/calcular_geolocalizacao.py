import requests
from typing import Dict, Any, Optional, Tuple
from geopy.distance import geodesic
from estado import EstadoReposicao

CACHE_LOCALIZACAO: Dict[str, Tuple[float, float]] = {}


def obter_coordenadas_local(localizacao: str) -> Optional[Tuple[float, float]]:
    local_limpo = localizacao.strip().lower()
    if local_limpo in CACHE_LOCALIZACAO:
        return CACHE_LOCALIZACAO[local_limpo]

    headers = {"User-Agent": "SmartRestock_App_Agent/2.0 (contact: support@smartrestock.local)"}

    try:
        url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(localizacao + ', Brasil')}&format=json&limit=1"
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            dados = resp.json()
            if dados:
                coords = (float(dados[0]["lat"]), float(dados[0]["lon"]))
                CACHE_LOCALIZACAO[local_limpo] = coords
                return coords
    except Exception:
        return None
    return None


def calcular_geolocalizacao(estado: EstadoReposicao) -> Dict[str, Any]:
    fornecedores = estado.get("fornecedores_encontrados", [])
    localizacao = estado.get("localizacao_usuario", "").strip() or "São Paulo - SP"
    origem = estado.get("coord_origem") or obter_coordenadas_local(localizacao)

    avisos = list(estado.get("avisos", []))

    if not fornecedores:
        return {"fornecedores_encontrados": [], "avisos": avisos}

    fornecedores_com_distancia = []
    for f in fornecedores:
        lat = f.get("latitude")
        lon = f.get("longitude")

        distancia = None

        if origem and lat is not None and lon is not None:
            try:
                distancia = round(geodesic(origem, (float(lat), float(lon))).km, 1)
            except Exception:
                distancia = None

        f["distancia_km"] = distancia
        fornecedores_com_distancia.append(f)

    avisos.append(
        f"Distâncias reais calculadas para {len(fornecedores_com_distancia)} fornecedores em '{localizacao}'."
    )

    return {
        "fornecedores_encontrados": fornecedores_com_distancia,
        "avisos": avisos,
    }
