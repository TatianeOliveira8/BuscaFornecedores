import io
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from grafo import construir_grafo
from estado import EstadoReposicao

app = FastAPI(title="SmartRestock API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

grafo_app = construir_grafo()


@app.get("/api/modelo-csv")
def baixar_modelo_csv():
    csv_conteudo = "nome_produto,estoque_atual,quantidade_necessaria\nRefrigerante Cola 2L,0,30\nPão de Hambúrguer,25,10\nQueijo Cheddar Fatiado,0,15\nBatata Palha Tradicional,12,8\nBacon Fatiado Defumado,18,5\n"
    return {
        "arquivo": "modelo_estoque.csv",
        "conteudo": csv_conteudo
    }


@app.post("/api/analisar")
async def analisar_reposicao(
    cidade: str = Form(...),
    distancia_maxima_km: float = Form(40.0),
    arquivo_csv: UploadFile = File(...)
):
    try:
        conteudo_bytes = await arquivo_csv.read()
        df = pd.read_csv(io.BytesIO(conteudo_bytes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler arquivo CSV: {str(e)}")

    colunas_obrigatorias = {"nome_produto", "estoque_atual", "quantidade_necessaria"}
    if not colunas_obrigatorias.issubset(set(df.columns)):
        raise HTTPException(
            status_code=400,
            detail=f"O CSV deve conter as colunas: {', '.join(colunas_obrigatorias)}"
        )

    itens = df.to_dict(orient="records")
    resultados = []

    for item in itens:
        estado_inicial: EstadoReposicao = {
            "nome_produto": str(item["nome_produto"]),
            "estoque_atual": int(item["estoque_atual"]),
            "quantidade_necessaria": int(item["quantidade_necessaria"]),
            "localizacao_usuario": str(cidade).strip(),
            "coord_origem": None,
            "distancia_maxima_km": float(distancia_maxima_km),
            "resultados_web_brutos": "",
            "fornecedores_encontrados": [],
            "fornecedores_dentro_raio": [],
            "fornecedores_priorizados": [],
            "fornecedor_escolhido": None,
            "fornecedores_recomendados": [],
            "status": "pendente",
            "avisos": [],
            "relatorio_decisao": "",
        }

        saida = grafo_app.invoke(estado_inicial)

        resultados.append({
            "nome_produto": item["nome_produto"],
            "estoque_atual": item["estoque_atual"],
            "quantidade_necessaria": item["quantidade_necessaria"],
            "status": saida.get("status"),
            "avisos": saida.get("avisos", []),
            "fornecedor_escolhido": saida.get("fornecedor_escolhido"),
            "fornecedores_recomendados": saida.get("fornecedores_recomendados", []),
            "relatorio_decisao": saida.get("relatorio_decisao", ""),
        })

    return {
        "localizacao_consultada": cidade,
        "distancia_maxima_km": distancia_maxima_km,
        "total_produtos": len(resultados),
        "resultados": resultados,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
