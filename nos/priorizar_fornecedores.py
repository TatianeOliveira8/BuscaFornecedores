import pandas as pd
from typing import Dict, Any
from estado import EstadoReposicao


def priorizar_fornecedores(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 6: Aplica a nota mínima de confiabilidade solicitada pelo usuário (ex: 3.0, 4.0 ou 5.0 estrelas)
    e ordena os fornecedores restantes pela confiabilidade, nota e distância.
    """
    fornecedores = estado["fornecedores_dentro_raio"]
    nota_minima = float(estado.get("nota_minima") or 3.0)

    if not fornecedores:
        return {"fornecedores_priorizados": []}

    df = pd.DataFrame(fornecedores)

    if "nota_media" not in df.columns:
        return {"fornecedores_priorizados": []}

    df = df[df["nota_media"].notna() & (df["nota_media"] >= nota_minima)]
    if df.empty:
        return {"fornecedores_priorizados": []}

    df["confiavel"] = df["quantidade_avaliacoes"].fillna(0) >= 5

    df_ordenado = df.sort_values(
        by=["confiavel", "nota_media", "distancia_km"],
        ascending=[False, False, True],
    )

    return {"fornecedores_priorizados": df_ordenado.to_dict(orient="records")}
