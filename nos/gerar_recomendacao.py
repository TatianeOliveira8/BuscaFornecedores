from typing import Dict, Any
from langchain_ollama import ChatOllama
from estado import EstadoReposicao

llm = ChatOllama(model="qwen2.5:1.5b", temperature=0)


def gerar_recomendacao(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 6: A IA (Qwen 2.5) analisa os fornecedores filtrados e redige um
    parecer executivo recomendando os melhores fornecedores encontrados online.
    """
    priorizados = estado.get("fornecedores_priorizados", [])
    avisos = list(estado.get("avisos", []))
    quantidade = estado["quantidade_necessaria"]
    nome_produto = estado["nome_produto"]

    if not priorizados:
        return {
            "fornecedor_escolhido": None,
            "fornecedores_recomendados": [],
            "status": "falha",
            "relatorio_decisao": f"Não foi possível repor '{nome_produto}': nenhum fornecedor online atendeu aos critérios de distância e viabilidade.",
        }

    # Seleciona até 5 melhores opções
    top_5_fornecedores = priorizados[:5]
    escolhido = top_5_fornecedores[0]

    # Prepara resumo para o prompt do LLM
    resumo_fornecedores_texto = ""
    for idx, f in enumerate(top_5_fornecedores, 1):
        total = f["preco_unitario"] * quantidade
        resumo_fornecedores_texto += (
            f"{idx}. {f['nome_fornecedor']}: Preço R$ {f['preco_unitario']:.2f}/un "
            f"(Total: R$ {total:.2f}), Distância: {f['distancia_km']} km, "
            f"Avaliações: {f['quantidade_avaliacoes']} ({f.get('nota_media', 'N/A')}★)\n"
        )

    prompt = f"""
Você é um especialista em logística e reposição inteligente de estoque de um delivery sediado em Pindamonhangaba - SP (CEP 12443-190).
Precisamos comprar: {quantidade} unidades de "{nome_produto}".

Após busca na web e cálculo de distância real até nosso CEP (raio logístico máximo de 40 km, menor preço e confiabilidade), obtivemos os seguintes fornecedores ranqueados:

{resumo_fornecedores_texto}

Elabore um parecer executivo de compra claro e conciso:
1. Indique com destaque o fornecedor vencedor ({escolhido['nome_fornecedor']}), justificando o porquê da escolha (custo-benefício, distância e reputação).
2. Liste as opções alternativas (até 5) caso o fornecedor principal não consiga atender a demanda imediata.
3. Se houver fornecedores com poucas avaliações (< 5), faça um alerta operacional.
4. Conclua com a ação recomendada para a equipe de compras.
"""

    try:
        resposta = llm.invoke(prompt)
        relatorio = resposta.content
    except Exception as e:
        avisos.append(f"Aviso LLM na recomendação: {e}")
        relatorio = (
            f"RECOMENDAÇÃO AUTOMÁTICA:\n"
            f"Fornecedor Vencedor: {escolhido['nome_fornecedor']}\n"
            f"Preço Unitário: R$ {escolhido['preco_unitario']:.2f} (Total: R$ {escolhido['preco_unitario'] * quantidade:.2f})\n"
            f"Distância: {escolhido['distancia_km']} km\n"
        )

    return {
        "fornecedor_escolhido": escolhido,
        "fornecedores_recomendados": top_5_fornecedores,
        "status": "aprovado",
        "avisos": avisos,
        "relatorio_decisao": relatorio,
    }
