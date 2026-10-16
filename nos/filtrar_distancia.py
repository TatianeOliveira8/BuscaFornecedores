import pandas as pd
from typing import Dict, Any
from estado import EstadoReposicao


def filtrar_por_distancia(estado: EstadoReposicao) -> Dict[str, Any]:
    fornecedores = estado.get("fornecedores_encontrados", [])
    distancia_maxima = float(estado.get("distancia_maxima_km") or 40.0)

    if not fornecedores:
        return {"fornecedores_dentro_raio": []}

    avisos = list(estado.get("avisos", []))
    df = pd.DataFrame(fornecedores)
    if "distancia_km" not in df.columns:
        return {"fornecedores_dentro_raio": [], "avisos": avisos}

    df_validos = df[df["distancia_km"].notna() & (df["distancia_km"] <= distancia_maxima)]
    if df_validos.empty:
        avisos.append(
            f"Nenhum fornecedor com distância conhecida foi encontrado a menos de {distancia_maxima:.0f} km."
        )

    return {
        "fornecedores_dentro_raio": df_validos.to_dict(orient="records"),
        "avisos": avisos,
    }
