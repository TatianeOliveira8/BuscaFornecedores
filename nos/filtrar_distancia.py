import pandas as pd
from typing import Dict, Any
from estado import EstadoReposicao


def filtrar_por_distancia(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 2: Filtra e descarta fornecedores que estejam a mais de 40 km de distância.
    """
    fornecedores = estado["fornecedores_encontrados"]
    if not fornecedores:
        return {"fornecedores_dentro_raio": []}

    df = pd.DataFrame(fornecedores)

    # Regra de negócio: descartar distância superior a 40 km
    df_validos = df[df["distancia_km"] <= 40.0]

    descartados = len(df) - len(df_validos)
    avisos = list(estado.get("avisos", []))

    if descartados > 0:
        avisos.append(f"{descartados} fornecedor(es) descartado(s) por estarem a mais de 40 km.")

    if df_validos.empty:
        return {
            "fornecedores_dentro_raio": [],
            "status": "sem_fornecedor",
            "avisos": avisos,
        }

    return {
        "fornecedores_dentro_raio": df_validos.to_dict(orient="records"),
        "avisos": avisos,
    }
