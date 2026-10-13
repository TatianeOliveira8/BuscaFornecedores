import requests
from typing import Dict, Any, Optional, Tuple
from geopy.distance import geodesic
from estado import EstadoReposicao

CACHE_LOCALIZACAO: Dict[str, Tuple[float, float]] = {}


def obter_coordenadas_local(localizacao: str) -> Optional[Tuple[float, float]]:
    """
    Descobre latitude e longitude de qualquer cidade do Brasil
    usando a API oficial do Nominatim com headers e fallback seguro.
    """
    local_limpo = localizacao.strip().lower()
    if local_limpo in CACHE_LOCALIZACAO:
        return CACHE_LOCALIZACAO[local_limpo]

    headers = {"User-Agent": "SmartRestock_App_Agent/2.0 (contact: support@smartrestock.local)"}

    # 1. Tentativa via OpenStreetMap direto
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
        pass

    # 2. Se for CEP, tenta ViaCEP + Nominatim
    cep_digitos = "".join([c for c in localizacao if c.isdigit()])
    if len(cep_digitos) == 8:
        try:
            r = requests.get(f"https://viacep.com.br/ws/{cep_digitos}/json/", timeout=4)
            if r.status_code == 200:
                cidade_cep = r.json().get("localidade", "")
                if cidade_cep:
                    return obter_coordenadas_local(cidade_cep)
        except Exception:
            pass

    return None


def calcular_geolocalizacao(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 4: Calcula a distância real em km de cada fornecedor em relação
    à localização digitada pelo usuário na tela.
    Garante que fornecedores da própria cidade nunca sejam descartados.
    """
    fornecedores = estado.get("fornecedores_encontrados", [])
    localizacao = estado.get("localizacao_usuario", "").strip() or "São Paulo - SP"
    origem = estado.get("coord_origem") or obter_coordenadas_local(localizacao)

    avisos = list(estado.get("avisos", []))

    if not fornecedores:
        return {"fornecedores_encontrados": [], "avisos": avisos}

    fornecedores_com_distancia = []
    cidade_usuario_pura = localizacao.split("-")[0].strip().lower()

    for f in fornecedores:
        lat = f.get("latitude")
        lon = f.get("longitude")
        endereco_forn = (f.get("endereco_completo") or f.get("cidade") or "").lower()

        distancia = None

        # 1. Se o fornecedor tem latitude e longitude e temos a coordenada de origem:
        if origem and lat is not None and lon is not None:
            try:
                distancia = round(geodesic(origem, (float(lat), float(lon))).km, 1)
            except Exception:
                distancia = None

        # Sem coordenadas confiáveis, a distância permanece desconhecida.
        # Não substitua a distância real por uma estimativa inventada.

        f["distancia_km"] = distancia
        fornecedores_com_distancia.append(f)

    avisos.append(
        f"Distâncias reais calculadas para {len(fornecedores_com_distancia)} fornecedores em '{localizacao}'."
    )

    return {
        "fornecedores_encontrados": fornecedores_com_distancia,
        "avisos": avisos,
    }
