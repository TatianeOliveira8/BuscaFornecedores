import pandas as pd
from typing import Dict, Any
from estado import EstadoReposicao


def filtrar_por_distancia(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 5: Filtra fornecedores que estejam acima da distância máxima configurada
    pelo usuário na tela. Caso todos fiquem acima do limite estrito, seleciona
    as opções mais próximas com aviso operacional para não deixar a compra sem alternativas.
    """
    fornecedores = estado.get("fornecedores_encontrados", [])
    distancia_maxima = float(estado.get("distancia_maxima_km") or 40.0)

    if not fornecedores:
        return {"fornecedores_dentro_raio": []}

    df = pd.DataFrame(fornecedores)

    df_validos = df[df["distancia_km"] <= distancia_maxima]
    avisos = list(estado.get("avisos", []))

    # Se nenhum fornecedor estritamente coube no raio selecionado (ex: raio de 15 km),
    # pega os mais próximos disponíveis para não deixar a operação de mãos atadas
    if df_validos.empty:
        avisos.append(
            f"Aviso: nenhum fornecedor encontrado a menos de {distancia_maxima:.0f} km. Exibindo os fornecedores mais próximos da região."
        )
        df_validos = df.sort_values(by="distancia_km", ascending=True).head(5)

    return {
        "fornecedores_dentro_raio": df_validos.to_dict(orient="records"),
        "avisos": avisos,
    }
