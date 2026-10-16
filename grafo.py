from langgraph.graph import StateGraph, START, END
from estado import EstadoReposicao
from nos import ( verificar_estoque, buscar_fornecedores_web, extrair_fornecedores_ia, avaliar_fornecedores, calcular_geolocalizacao, filtrar_por_distancia, priorizar_fornecedores, gerar_recomendacao,
)


def construir_grafo():
    grafo = StateGraph(EstadoReposicao)

    grafo.add_node("verificar_estoque", verificar_estoque)
    grafo.add_node("buscar_fornecedores_web", buscar_fornecedores_web)
    grafo.add_node("extrair_fornecedores_ia", extrair_fornecedores_ia)
    grafo.add_node("avaliar_fornecedores", avaliar_fornecedores)
    grafo.add_node("calcular_geolocalizacao", calcular_geolocalizacao)
    grafo.add_node("filtrar_distancia", filtrar_por_distancia)
    grafo.add_node("priorizar_fornecedores", priorizar_fornecedores)
    grafo.add_node("gerar_recomendacao", gerar_recomendacao)

    def rota_apos_verificar_estoque(estado: EstadoReposicao):
        if estado["status"] == "em_estoque":
            return "fim"
        return "buscar_web"

    def rota_apos_filtrar_distancia(estado: EstadoReposicao):
        if not estado.get("fornecedores_dentro_raio"):
            return "recomendar"
        return "priorizar"

    grafo.add_edge(START, "verificar_estoque")

    grafo.add_conditional_edges(
        "verificar_estoque",
        rota_apos_verificar_estoque,
        {
            "fim": END,
            "buscar_web": "buscar_fornecedores_web",
        },
    )

    grafo.add_edge("buscar_fornecedores_web", "extrair_fornecedores_ia")
    grafo.add_edge("extrair_fornecedores_ia", "calcular_geolocalizacao")
    grafo.add_edge("calcular_geolocalizacao", "filtrar_distancia")

    grafo.add_conditional_edges(
        "filtrar_distancia",
        rota_apos_filtrar_distancia,
        {
            "recomendar": "gerar_recomendacao",
            "priorizar": "avaliar_fornecedores",
        },
    )

    grafo.add_edge("avaliar_fornecedores", "priorizar_fornecedores")
    grafo.add_edge("priorizar_fornecedores", "gerar_recomendacao")
    grafo.add_edge("gerar_recomendacao", END)

    return grafo.compile()
