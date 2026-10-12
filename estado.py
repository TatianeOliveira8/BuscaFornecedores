from typing import TypedDict, List, Dict, Any, Optional, Tuple


class EstadoReposicao(TypedDict):
    # Produto sob análise do estoque
    nome_produto: str
    estoque_atual: int
    quantidade_necessaria: int

    # Localização definida pelo usuário (Cidade/UF ou CEP)
    localizacao_usuario: str
    coord_origem: Optional[Tuple[float, float]]
    distancia_maxima_km: float
    nota_minima: float

    # Dados brutos retornados da busca web
    resultados_web_brutos: str

    # Fornecedores extraídos e processados ao longo do fluxo
    fornecedores_encontrados: List[Dict[str, Any]]
    fornecedores_dentro_raio: List[Dict[str, Any]]
    fornecedores_priorizados: List[Dict[str, Any]]

    # Resultado e relatório final (Top fornecedores recomendados)
    fornecedor_escolhido: Optional[Dict[str, Any]]
    fornecedores_recomendados: List[Dict[str, Any]]
    status: str            # 'em_estoque', 'aprovado', 'sem_fornecedor', 'falha'
    avisos: List[str]      # Alertas e observações geradas pelo fluxo
    relatorio_decisao: str # Parecer executivo da IA
