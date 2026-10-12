from pathlib import Path
import pandas as pd
from grafo import construir_grafo
from estado import EstadoReposicao


def main():
    pasta_dados = Path(__file__).parent / "data"
    arquivo_estoque = pasta_dados / "estoque.csv"

    # Carrega dados a partir apenas do CSV de estoque (sem precisar de fornecedores.csv)
    df_estoque = pd.read_csv(arquivo_estoque)

    # Constrói e compila o agente inteligente do LangGraph
    app = construir_grafo()

    itens_estoque = df_estoque.to_dict(orient="records")

    print("=" * 65)
    print("AGENTE AUTÔNOMO DE REPOSIÇÃO - SMARTRESTOCK COM BUSCA WEB & IA")
    print("Base do Delivery: Pindamonhangaba - SP (CEP: 12443-190)")
    print(f"Itens monitorados em {arquivo_estoque.name}: {len(itens_estoque)}")
    print("=" * 65)

    for item in itens_estoque:
        # Estado inicial enviado para o agente
        estado_inicial: EstadoReposicao = {
            "nome_produto": item["nome_produto"],
            "estoque_atual": int(item["estoque_atual"]),
            "quantidade_necessaria": int(item["quantidade_necessaria"]),
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

        print(f"\n[PRODUTO]: {item['nome_produto']} (Estoque: {item['estoque_atual']} | Necessário: {item['quantidade_necessaria']})")

        # Invoca o agente autônomo
        resultado = app.invoke(estado_inicial)

        print(f"Status Final: {resultado['status']}")

        if resultado["avisos"]:
            print("Alertas registrados durante a execução:")
            for aviso in resultado["avisos"]:
                print(f"  • {aviso}")

        print("\n--- PARECER EXECUTIVO DA IA ---")
        print(resultado["relatorio_decisao"])
        print("-" * 65)


if __name__ == "__main__":
    main()
