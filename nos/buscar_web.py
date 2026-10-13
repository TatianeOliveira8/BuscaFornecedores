import os
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from estado import EstadoReposicao

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")


def buscar_fornecedores_web(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 2: Realiza busca de distribuidores via Google Places usando termos comerciais flexíveis.
    Garante que a pesquisa encontre atacadistas e depósitos na cidade informada pelo usuário.
    """
    nome_produto = estado["nome_produto"]
    localizacao = estado.get("localizacao_usuario", "").strip() or "São Paulo - SP"
    avisos = list(estado.get("avisos", []))
    avisos.append(f"Consultando Google Places para '{nome_produto}' em {localizacao}...")

    # Extrai o termo principal do produto (ex: "Refrigerante" em vez de "Refrigerante Cola 2L")
    termo_base = nome_produto.split()[0] if nome_produto else "bebidas"

    queries = [
        f"distribuidora {termo_base} {localizacao}",
        f"atacado alimentos bebidas {localizacao}",
        f"distribuidora atacado {localizacao}",
    ]

    url = "https://google.serper.dev/places"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    lugares = []
    for q in queries:
        try:
            payload = {"q": q, "gl": "br", "hl": "pt-br"}
            resp = requests.post(url, headers=headers, json=payload, timeout=8)
            if resp.status_code == 200:
                places = resp.json().get("places", [])
                if places:
                    lugares.extend(places)
                    break
                avisos.append(f"O Serper não encontrou locais para a busca '{q}'.")
            else:
                avisos.append(
                    f"Serper retornou HTTP {resp.status_code} para a busca '{q}'."
                )
        except (requests.RequestException, ValueError) as e:
            avisos.append(f"Aviso de busca: {e}")

    # Remove duplicidades
    vistos = set()
    lugares_unicos = []
    for p in lugares:
        nome = p.get("title")
        if nome and nome not in vistos:
            vistos.add(nome)
            lugares_unicos.append(p)

    return {
        "resultados_web_brutos": json.dumps(lugares_unicos, ensure_ascii=False, indent=2),
        "avisos": avisos,
    }
