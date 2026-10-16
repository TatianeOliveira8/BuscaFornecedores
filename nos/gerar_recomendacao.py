import os
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from estado import EstadoReposicao

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("API_KEY"),
    temperature=0,
)


def gerar_recomendacao(estado: EstadoReposicao) -> Dict[str, Any]:
    priorizados = estado.get("fornecedores_priorizados", [])
    avisos = list(estado.get("avisos", []))
    quantidade = estado["quantidade_necessaria"]
    nome_produto = estado["nome_produto"]
    localizacao = estado.get("localizacao_usuario", "Sua região")
    dist_max = estado.get("distancia_maxima_km", 40.0)

    if not priorizados:
        return {
            "fornecedor_escolhido": None,
            "fornecedores_recomendados": [],
            "status": "falha",
            "relatorio_decisao": f"Não foi possível repor '{nome_produto}': nenhum fornecedor foi encontrado no raio de {dist_max} km em {localizacao}.",
        }

    top_5_fornecedores = priorizados[:5]
    escolhido = top_5_fornecedores[0]

    resumo_fornecedores_texto = ""
    for idx, f in enumerate(top_5_fornecedores, 1):
        investigacao = f.get("investigacao", {})
        resumo_fornecedores_texto += (
            f"{idx}. {f['nome_fornecedor']}: Distância: {f.get('distancia_km', 'N/A')} km, "
            f"Relevância da busca: {f.get('relevancia', 'N/A')}, "
            f"Produtos identificados: {investigacao.get('produtos_identificados', [])}, "
            f"Contatos: {investigacao.get('contatos', [])}, "
            f"Compatibilidade: {investigacao.get('compatibilidade', 'nao_confirmada')}, "
            f"Justificativa: {investigacao.get('justificativa', 'não encontrada')}\n"
        )

    prompt = f"""
Você é um especialista em logística de compras para delivery.
O usuário solicitou reposição de: {quantidade} unidades de "{nome_produto}".
Local de entrega do usuário: {localizacao}.
Critério definido pelo usuário: raio máximo de {dist_max} km.
Use somente informações verificadas na busca e nas páginas consultadas. Se uma informação não estiver disponível, diga que ela não foi encontrada.
Não trate compatibilidade provável como confirmação de venda ou disponibilidade.

Fornecedores selecionados e ranqueados:
{resumo_fornecedores_texto}

Elabore um resumo conciso e objetivo:
1. Explique em uma frase por que o fornecedor principal ({escolhido['nome_fornecedor']}) foi escolhido, considerando distância, relevância e informações investigadas.
2. Mencione as alternativas e os contatos encontrados em uma frase.
3. Recomende a ação de compra em uma frase, informando dados ausentes quando necessário.
"""

    try:
        resposta = llm.invoke(prompt)
        relatorio = resposta.content.strip()
    except Exception as e:
        avisos.append(f"Aviso LLM: {e}")
        relatorio = (
            f"Recomendação Automática: O fornecedor principal selecionado é {escolhido['nome_fornecedor']} "
            f"a {escolhido['distancia_km']} km de distância "
            f"(relevância da busca: {escolhido.get('relevancia', 'N/A')})."
        )

    return {
        "fornecedor_escolhido": escolhido,
        "fornecedores_recomendados": top_5_fornecedores,
        "status": "aprovado",
        "avisos": avisos,
        "relatorio_decisao": relatorio,
    }
