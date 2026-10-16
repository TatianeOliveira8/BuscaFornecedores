from typing import TypedDict, List, Dict, Any, Optional, Tuple


class EstadoReposicao(TypedDict):
    nome_produto: str
    estoque_atual: int
    quantidade_necessaria: int
    localizacao_usuario: str
    coord_origem: Optional[Tuple[float, float]]
    distancia_maxima_km: float
    resultados_web_brutos: str
    fornecedores_encontrados: List[Dict[str, Any]]
    fornecedores_dentro_raio: List[Dict[str, Any]]
    fornecedores_priorizados: List[Dict[str, Any]]
    fornecedor_escolhido: Optional[Dict[str, Any]]
    fornecedores_recomendados: List[Dict[str, Any]]
    status: str
    avisos: List[str]
    relatorio_decisao: str
