from typing import Dict, Any
from langchain_ollama import ChatOllama
from estado import EstadoReposicao

llm = ChatOllama(model="qwen2.5:1.5b", temperature=0)


def gerar_recomendacao(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 7: A IA (Qwen 2.5) analisa os fornecedores filtrados e redige um
    resumo executivo consolidado com a análise de confiabilidade e localização.
    """
    priorizados = estado.get("fornecedores_priorizados", [])
    avisos = list(estado.get("avisos", []))
    quantidade = estado["quantidade_necessaria"]
    nome_produto = estado["nome_produto"]
    localizacao = estado.get("localizacao_usuario", "Sua região")
    dist_max = estado.get("distancia_maxima_km", 40.0)
    nota_min = estado.get("nota_minima", 3.0)

    if not priorizados:
        return {
            "fornecedor_escolhido": None,
            "fornecedores_recomendados": [],
            "status": "falha",
            "relatorio_decisao": f"Não foi possível repor '{nome_produto}': nenhum fornecedor atendeu ao raio de {dist_max} km e avaliação mínima de {nota_min}★ em {localizacao}.",
        }

    top_5_fornecedores = priorizados[:5]
    escolhido = top_5_fornecedores[0]

    resumo_fornecedores_texto = ""
    for idx, f in enumerate(top_5_fornecedores, 1):
        resumo_fornecedores_texto += (
            f"{idx}. {f['nome_fornecedor']}: Distância: {f['distancia_km']} km, "
            f"Avaliação: {f.get('nota_media', 'N/A')}★ ({f['quantidade_avaliacoes']} avaliações)\n"
        )

    prompt = f"""
Você é um especialista em logística de compras para delivery.
O usuário solicitou reposição de: {quantidade} unidades de "{nome_produto}".
Local de entrega do usuário: {localizacao}.
Critérios definidos pelo usuário: Raio máx de {dist_max} km e avaliação mínima de {nota_min} estrelas.

Fornecedores selecionados e ranqueados:
{resumo_fornecedores_texto}

Elabore um resumo conciso e objetivo:
1. Destaque o fornecedor principal ({escolhido['nome_fornecedor']}) explicando o equilíbrio entre proximidade e confiabilidade das notas.
2. Mencione se as opções alternativas atendem satisfatoriamente como plano B.
3. Conclua com uma recomendação direta de ação de compra.
"""

    try:
        resposta = llm.invoke(prompt)
        relatorio = resposta.content.strip()
    except Exception as e:
        avisos.append(f"Aviso LLM: {e}")
        relatorio = (
            f"Recomendação Automática: O fornecedor principal selecionado é {escolhido['nome_fornecedor']} "
            f"a {escolhido['distancia_km']} km de distância "
            f"(Nota: {escolhido.get('nota_media', 'N/A')}★)."
        )

    return {
        "fornecedor_escolhido": escolhido,
        "fornecedores_recomendados": top_5_fornecedores,
        "status": "aprovado",
        "avisos": avisos,
        "relatorio_decisao": relatorio,
    }
