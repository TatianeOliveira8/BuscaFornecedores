import os
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from estado import EstadoReposicao

# Carrega variáveis do arquivo .env
load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")


def buscar_fornecedores_web(estado: EstadoReposicao) -> Dict[str, Any]:
    """
    Nó 2: Realiza busca de empresas e distribuidores via Google Places (Serper API)
    direcionada para a região de Pindamonhangaba, Taubaté e Vale do Paraíba.
    """
    nome_produto = estado["nome_produto"]
    avisos = list(estado.get("avisos", []))
    avisos.append(f"Consultando Google Places (Serper) para distribuidores de '{nome_produto}'...")

    # Query direcionada para distribuidores/atacado da região
    query = f"distribuidora atacado {nome_produto} Pindamonhangaba SP"

    url = "https://google.serper.dev/places"
    payload = json.dumps({
        "q": query,
        "gl": "br",
        "hl": "pt-br"
    })
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            lugares = dados.get("places", [])
            
            # Se não encontrou lugares na primeira busca, tenta query mais ampla no Vale
            if not lugares:
                payload_amplo = json.dumps({
                    "q": f"distribuidora {nome_produto} Vale do Paraíba SP",
                    "gl": "br",
                    "hl": "pt-br"
                })
                resp_ampla = requests.post(url, headers=headers, data=payload_amplo, timeout=10)
                if resp_ampla.status_code == 200:
                    lugares = resp_ampla.json().get("places", [])

            resultados_texto = json.dumps(lugares, ensure_ascii=False, indent=2)
        else:
            resultados_texto = f"Erro Serper status {response.status_code}: {response.text}"
            avisos.append(f"Aviso Serper API: status {response.status_code}")
    except Exception as e:
        resultados_texto = f"Erro na requisição Serper: {e}"
        avisos.append(f"Aviso de conexão com Serper: {str(e)}")

    return {
        "resultados_web_brutos": resultados_texto,
        "avisos": avisos,
    }
