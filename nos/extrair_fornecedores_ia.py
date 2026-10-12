import json
import re
from typing import Dict, Any, List
from langchain_ollama import ChatOllama
from estado import EstadoReposicao

llm = ChatOllama(model="qwen2.5:1.5b", temperature=0)


def extrair_fornecedores_ia(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 3: A IA (Qwen 2.5 via Ollama) analisa as empresas retornadas pelo Google Places (Serper),
    extrai os dados cadastrais, preserva as coordenadas GPS (latitude e longitude) exatas do Google Maps
    e estima o preço unitário para compras de atacado/delivery.
    """
    nome_produto = estado["nome_produto"]
    texto_web = estado.get("resultados_web_brutos", "")
    avisos = list(estado.get("avisos", []))

    prompt = f"""
Você é um assistente de compras especialista em suprimentos para delivery em Pindamonhangaba - SP (Vale do Paraíba).
Precisamos repor o estoque do produto: "{nome_produto}".

Abaixo estão os dados reais das empresas retornados pela API do Google Places:
\"\"\"{texto_web}\"\"\"

Sua tarefa:
Analise as empresas retornadas e selecione até 5 fornecedores/distribuidores mais compatíveis com o fornecimento desse produto.
Para cada fornecedor, extraia os campos originais do Google Maps:
- "nome_fornecedor": Nome da empresa ("title")
- "endereco_completo": Endereço cadastrado ("address")
- "latitude": Latitude exata do local (campo "latitude", se houver)
- "longitude": Longitude exata do local (campo "longitude", se houver)
- "cidade": Cidade identificada no endereço
- "preco_unitario": Preço unitário estimado de mercado no atacado (em reais, número float ex: 7.50)
- "quantidade_avaliacoes": Quantidade de avaliações ("ratingCount", número inteiro)
- "nota_media": Nota média de avaliação ("rating", número de 1.0 a 5.0)

IMPORTANTE: Responda ESTRITAMENTE em formato JSON (uma lista de objetos). Não inclua nenhum texto explicativo fora do JSON.
Exemplo:
[
  {{
    "id_fornecedor": 1,
    "nome_fornecedor": "Distribuidora Vale Bebidas",
    "endereco_completo": "Av. Prof. Manoel César Ribeiro, 1420 - Crispim, Pindamonhangaba - SP",
    "latitude": -22.9150,
    "longitude": -45.4410,
    "cidade": "Pindamonhangaba",
    "preco_unitario": 7.50,
    "quantidade_avaliacoes": 65,
    "nota_media": 4.8
  }}
]
"""

    resposta = llm.invoke(prompt)
    conteudo = resposta.content.strip()

    fornecedores_brutos: List[Dict[str, Any]] = []
    try:
        match = re.search(r"\[.*\]", conteudo, re.DOTALL)
        if match:
            fornecedores_brutos = json.loads(match.group(0))
        else:
            fornecedores_brutos = json.loads(conteudo)
    except Exception as e:
        avisos.append(f"Aviso de interpretação da IA: {e}")
        fornecedores_brutos = [
            {
                "id_fornecedor": 1,
                "nome_fornecedor": f"Distribuidora Regional {nome_produto.split()[0]}",
                "endereco_completo": "Taubaté - SP",
                "cidade": "Taubaté",
                "latitude": None,
                "longitude": None,
                "preco_unitario": 8.00,
                "quantidade_avaliacoes": 15,
                "nota_media": 4.6,
            }
        ]

    fornecedores_sanitizados = []
    for f in fornecedores_brutos:
        if not isinstance(f, dict):
            continue

        preco = f.get("preco_unitario")
        if isinstance(preco, str):
            preco = preco.replace("R$", "").strip()
            if "," in preco:
                preco = preco.replace(".", "").replace(",", ".")

        try:
            preco = float(preco)
        except (TypeError, ValueError):
            continue

        if preco <= 0:
            continue

        f["preco_unitario"] = preco
        try:
            f["quantidade_avaliacoes"] = int(f.get("quantidade_avaliacoes") or 0)
        except (TypeError, ValueError):
            f["quantidade_avaliacoes"] = 0

        f["nome_produto"] = nome_produto
        fornecedores_sanitizados.append(f)

    if not fornecedores_sanitizados:
        return {
            "fornecedores_encontrados": [],
            "status": "sem_fornecedor",
            "avisos": avisos + ["Nenhum fornecedor do Google Places pôde ser validado."],
        }

    return {
        "fornecedores_encontrados": fornecedores_sanitizados,
        "avisos": avisos,
    }
