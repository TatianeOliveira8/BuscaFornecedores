from typing import Dict, Any
from estado import EstadoReposicao


def priorizar_fornecedores(estado: EstadoReposicao) -> Dict[str, Any]:
    fornecedores = estado["fornecedores_dentro_raio"]

    if not fornecedores:
        return {"fornecedores_priorizados": []}

    ordenados = sorted(
        fornecedores,
        key=lambda fornecedor: (
            fornecedor.get("investigacao", {}).get("compatibilidade") == "nao_confirmada",
            fornecedor.get("investigacao", {}).get("compatibilidade") != "confirmada",
            fornecedor.get("distancia_km") is None,
            fornecedor.get("distancia_km") or 0,
            -fornecedor.get("relevancia", 0),
        ),
    )
    return {"fornecedores_priorizados": ordenados[:5]}
