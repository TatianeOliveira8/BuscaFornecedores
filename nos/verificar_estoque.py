from typing import Dict, Any
from estado import EstadoReposicao


def verificar_estoque(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 1: Avalia se o estoque está zerado (0).
    Se estiver zerado, encaminha para a busca de fornecedores na web.
    """
    nome_produto = estado["nome_produto"]
    estoque_atual = estado["estoque_atual"]

    if estoque_atual > 0:
        return {
            "status": "em_estoque",
            "relatorio_decisao": f"Produto '{nome_produto}' ainda possui {estoque_atual} unidade(s) em estoque. Nenhuma compra necessária.",
            "fornecedores_encontrados": [],
        }

    return {
        "status": "estoque_zerado",
        "avisos": [f"Estoque zerado para '{nome_produto}'. Disparando agente de busca web."],
    }
