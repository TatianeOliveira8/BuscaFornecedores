import pandas as pd
from typing import Dict, Any
from estado import EstadoReposicao


def priorizar_fornecedores(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 6: Aplica a nota mínima de confiabilidade solicitada pelo usuário (ex: 3.0, 4.0 ou 5.0 estrelas)
    e ordena os fornecedores restantes pelo menor preço unitário e maior nota.
    """
    fornecedores = estado["fornecedores_dentro_raio"]
    nota_minima = float(estado.get("nota_minima") or 3.0)

    if not fornecedores:
        return {"fornecedores_priorizados": []}

    df = pd.DataFrame(fornecedores)

    if "nota_media" in df.columns:
        df_confiaveis = df[df["nota_media"] >= nota_minima]
        if df_confiaveis.empty:
            df_confiaveis = df
        else:
            df = df_confiaveis

    df["confiavel"] = df["quantidade_avaliacoes"] >= 5

    df_ordenado = df.sort_values(
        by=["confiavel", "preco_unitario", "nota_media", "distancia_km"],
        ascending=[False, True, False, True],
    )

    return {"fornecedores_priorizados": df_ordenado.to_dict(orient="records")}
