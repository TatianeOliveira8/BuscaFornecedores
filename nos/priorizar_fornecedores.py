import pandas as pd
from typing import Dict, Any
from estado import EstadoReposicao


def priorizar_fornecedores(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 3: Ordena pelo menor preço unitário e aplica critério de confiabilidade.
    Dá preferência para fornecedores confiáveis (5 ou mais avaliações).
    """
    fornecedores = estado["fornecedores_dentro_raio"]
    if not fornecedores:
        return {"fornecedores_priorizados": []}

    df = pd.DataFrame(fornecedores)

    # Flag de reputação: dá preferência para fornecedores com 5 ou mais avaliações
    df["confiavel"] = df["quantidade_avaliacoes"] >= 5

    # Ordenação multi-critério:
    # 1º Confiável (True vem antes de False no critério descendente)
    # 2º Menor preço unitário (ascendente)
    # 3º Menor distância (ascendente, desempate)
    df_ordenado = df.sort_values(
        by=["confiavel", "preco_unitario", "distancia_km"],
        ascending=[False, True, True],
    )

    return {"fornecedores_priorizados": df_ordenado.to_dict(orient="records")}
