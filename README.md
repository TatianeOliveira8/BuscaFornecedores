# Busca Fornecedores

## Sobre o projeto

O Busca Fornecedores analisa um CSV de estoque e encontra fornecedores próximos para os produtos que precisam de reposição. A busca considera a cidade ou CEP informado, o raio máximo definido e a relevância dos resultados encontrados.

Ao final, o sistema lista até 5 fornecedores e gera uma recomendação objetiva de compra com apoio de IA.

## Regras de negócio

- Produtos com estoque maior que zero não geram busca de fornecedor.
- Produtos com estoque igual a zero entram no processo de reposição.
- O CSV deve conter `nome_produto`, `estoque_atual` e `quantidade_necessaria`.
- A busca usa a cidade ou o CEP informado pelo usuário.
- Apenas fornecedores dentro do raio máximo configurado são considerados.
- São exibidos no máximo 5 fornecedores por produto.
- Os fornecedores são ordenados pela menor distância e pela relevância retornada pela busca.
- Notas e avaliações não são utilizadas como critério.
- O primeiro fornecedor da lista é considerado o principal.
- A IA explica a escolha do fornecedor principal, apresenta as alternativas e recomenda a ação de compra em uma frase.
- A recomendação não confirma preço, disponibilidade ou quantidade em estoque do fornecedor.
- Quando houver site público, o agente pode investigá-lo para procurar o produto consultado e meios de contato.
- Informações não encontradas no site são exibidas como não disponíveis; o sistema não inventa dados.
- A IA avalia a compatibilidade do produto com as evidências encontradas e classifica a compatibilidade como confirmada, provável ou não confirmada.
- Quando a evidência for insuficiente, o agente pode realizar uma única pesquisa adicional específica por fornecedor e produto.

## User stories

### US-01 — Identificar produtos para reposição

Como responsável pelo estoque, quero enviar uma planilha CSV para identificar quais produtos estão sem estoque, para saber o que precisa ser comprado.

### US-02 — Buscar fornecedores por localização

Como responsável pelas compras, quero informar uma cidade ou CEP e um raio máximo, para encontrar fornecedores próximos ao local de entrega.

### US-03 — Comparar fornecedores

Como responsável pelas compras, quero visualizar até 5 fornecedores ordenados por distância e relevância, para escolher uma opção adequada.

### US-04 — Receber recomendação de compra

Como responsável pelas compras, quero receber uma análise resumida, para entender qual fornecedor é o principal, quais são as alternativas e qual ação devo tomar.

### US-05 — Investigar fornecedores encontrados

Como responsável pelas compras, quero que o agente investigue os fornecedores encontrados, para obter informações comerciais relevantes antes de escolher onde comprar.

### US-06 — Consultar informações comerciais

Como responsável pelas compras, quero visualizar produtos identificados e meios de contato disponíveis, para avaliar quais fornecedores atendem às minhas necessidades.

### US-07 — Receber recomendações fundamentadas

Como responsável pelas compras, quero receber recomendações baseadas nas informações coletadas, para entender por que determinado fornecedor foi indicado.

### US-08 — Identificar informações não encontradas

Como responsável pelas compras, quero saber quando uma informação não estiver disponível, para evitar decisões baseadas em dados presumidos ou incorretos.

### US-09 — Investigar produtos nos fornecedores

Como usuário, quero que o sistema utilize os resultados da busca e as páginas comerciais dos fornecedores para encontrar evidências de que eles trabalham com os produtos solicitados.

### US-10 — Avaliar a compatibilidade dos produtos com IA

Como usuário, quero que a IA interprete as informações encontradas e avalie se os produtos anunciados correspondem ao produto solicitado, mesmo quando houver diferenças na descrição.

### US-11 — Realizar pesquisas adicionais quando necessário

Como usuário, quero que o agente realize uma nova pesquisa específica quando as informações iniciais forem insuficientes, sem repetir buscas desnecessárias.

### US-12 — Receber recomendações fundamentadas

Como usuário, quero receber recomendações baseadas na compatibilidade, distância e evidências disponíveis.

### US-13 — Identificar informações não confirmadas

Como usuário, quero que o sistema diferencie informações encontradas de informações não confirmadas.

## Instalar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd frontend
npm install
```

Configure a chave do Serper no arquivo `.env`:

```env
SERPER_API_KEY=sua_chave
```

## Rodar

Terminal 1 (backend):

```bash
source .venv/bin/activate
uvicorn api:app --reload --port 8000
```

Terminal 2 (frontend):

```bash
cd frontend
npm run dev
```

Acesse: http://localhost:3000
