from typing import Dict, Any, Optional
from geopy.distance import geodesic
from estado import EstadoReposicao

# Coordenadas fixas do seu delivery (Moreira César / Pindamonhangaba - SP, CEP 12443-190)
COORD_ORIGEM_DELIVERY = (-22.9248, -45.4616)


def calcular_distancia_km(lat: Optional[float], lon: Optional[float]) -> float:
    """
    Calcula a distância geodésica real (em km) entre o CEP do delivery e as
    coordenadas oficiais de latitude e longitude entregues pelo Google Places.
    """
    if lat is not None and lon is not None:
        try:
            return round(geodesic(COORD_ORIGEM_DELIVERY, (float(lat), float(lon))).km, 1)
        except (ValueError, TypeError):
            pass
    return 999.0


def calcular_geolocalizacao(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 4: Calcula a distância geográfica exata de cada fornecedor
    em relação ao CEP 12443-190 utilizando as coordenadas do Google Places.
    """
    fornecedores = estado.get("fornecedores_encontrados", [])
    avisos = list(estado.get("avisos", []))

    if not fornecedores:
        return {"fornecedores_encontrados": [], "avisos": avisos}

    fornecedores_com_distancia = []
    for f in fornecedores:
        lat = f.get("latitude")
        lon = f.get("longitude")

        distancia = calcular_distancia_km(lat, lon)
        f["distancia_km"] = distancia
        fornecedores_com_distancia.append(f)

    avisos.append(
        f"Distâncias reais calculadas para {len(fornecedores_com_distancia)} fornecedores via coordenadas do Google Places."
    )

    return {
        "fornecedores_encontrados": fornecedores_com_distancia,
        "avisos": avisos,
    }
