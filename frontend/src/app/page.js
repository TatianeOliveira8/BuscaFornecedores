"use client";

import { useState } from "react";
import { Download, Upload, Search, MapPin, Route, ExternalLink, Loader2, CheckCircle2, AlertCircle } from "lucide-react";

export default function Home() {
  const [cidade, setCidade] = useState("Pindamonhangaba - SP");
  const [distancia, setDistancia] = useState("40");
  const [arquivo, setArquivo] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");
  const [dadosResposta, setDadosResposta] = useState(null);

  const baixarModeloCSV = () => {
    const conteudo = "nome_produto,estoque_atual,quantidade_necessaria\nRefrigerante Cola 2L,0,30\nPão de Hambúrguer,25,10\nQueijo Cheddar Fatiado,0,15\nBatata Palha Tradicional,12,8\nBacon Fatiado Defumado,18,5\n";
    const blob = new Blob([conteudo], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "modelo_estoque.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const analisarEstoque = async (e) => {
    e.preventDefault();
    setErro("");
    setDadosResposta(null);

    if (!arquivo) {
      setErro("Por favor, selecione uma planilha CSV com os produtos.");
      return;
    }

    if (!cidade.trim()) {
      setErro("Informe a sua cidade ou região.");
      return;
    }

    setCarregando(true);

    try {
      const formData = new FormData();
      formData.append("cidade", cidade);
      formData.append("distancia_maxima_km", distancia);
      formData.append("arquivo_csv", arquivo);

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const resp = await fetch(`${apiUrl}/api/analisar`, {
        method: "POST",
        body: formData,
      });

      if (!resp.ok) {
        const erroJson = await resp.json();
        throw new Error(erroJson.detail || "Erro ao processar dados.");
      }

      const data = await resp.json();
      setDadosResposta(data);
    } catch (err) {
      setErro(err.message || "Não foi possível conectar com o servidor.");
    } finally {
      setCarregando(false);
    }
  };

  return (
    <main className="max-w-5xl mx-auto px-4 py-10">
      <header className="mb-8 text-center sm:text-left border-b border-slate-800 pb-6">
        <h1 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
          Smart<span className="text-emerald-400">Restock</span>
        </h1>
        <p className="mt-2 text-slate-400 text-sm sm:text-base">
          Encontre fornecedores para repor seu estoque de forma inteligente.
Envie sua planilha de estoque, informe sua localização e defina a distância máxima para encontrar fornecedores próximos. O sistema analisa os produtos que precisam de reposição, pesquisa estabelecimentos na região e reúne informações públicas para ajudar você a identificar opções de compra.
Com o apoio de inteligência artificial, você recebe uma recomendação baseada nas informações encontradas, na localização dos fornecedores e nos dados disponíveis sobre os produtos.
        </p>
      </header>

      <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-xl mb-10">
        <form onSubmit={analisarEstoque} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
                <MapPin className="w-4 h-4 text-emerald-400" />
                Sua Cidade ou Região
              </label>
              <input
                type="text"
                value={cidade}
                onChange={(e) => setCidade(e.target.value)}
                placeholder="Ex: Pindamonhangaba - SP ou Taubaté - SP"
                className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
                <Route className="w-4 h-4 text-emerald-400" />
                Distância Máxima
              </label>
              <select
                value={distancia}
                onChange={(e) => setDistancia(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="15">Até 15 km (Muito Próximo)</option>
                <option value="20">Até 20 km (Próximo)</option>
                <option value="30">Até 30 km (Médio)</option>
                <option value="40">Até 40 km (Padrão)</option>
                <option value="50">Até 50 km (Regional)</option>
              </select>
            </div>

          </div>

          <div className="border-t border-slate-800 pt-6 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
            <div className="flex-1">
              <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
                <Upload className="w-4 h-4 text-emerald-400" />
                Planilha CSV de Estoque
              </label>
              <input
                type="file"
                accept=".csv"
                onChange={(e) => setArquivo(e.target.files[0])}
                className="block w-full text-sm text-slate-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-slate-800 file:text-emerald-400 hover:file:bg-slate-700 cursor-pointer"
              />
            </div>

            <button
              type="button"
              onClick={baixarModeloCSV}
              className="flex items-center justify-center gap-2 px-4 py-2.5 border border-slate-700 rounded-xl text-slate-300 text-sm hover:bg-slate-800 hover:text-white transition-colors"
            >
              <Download className="w-4 h-4 text-emerald-400" />
              Baixar Modelo de CSV
            </button>
          </div>

          {erro && (
            <div className="p-4 bg-rose-950/50 border border-rose-800 text-rose-300 rounded-xl text-sm flex items-center gap-3">
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              <span>{erro}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={carregando}
            className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold py-3.5 rounded-xl transition-colors flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {carregando ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Buscando Fornecedores no Google e Analisando com IA...
              </>
            ) : (
              <>
                <Search className="w-5 h-5" />
                Buscar
              </>
            )}
          </button>
        </form>
      </section>

      {dadosResposta && (
        <section className="space-y-8">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              Recomendações de Compra
            </h2>
            <span className="text-xs text-slate-400">
              Local: {dadosResposta.localizacao_consultada} | Raio: {dadosResposta.distancia_maxima_km} km
            </span>
          </div>

          {dadosResposta.resultados.map((item, idx) => (
            <div key={idx} className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-md space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-4">
                <div>
                  <h3 className="text-lg font-bold text-white">{item.nome_produto}</h3>
                  <p className="text-sm text-slate-400">
                    Estoque atual: <strong className={item.estoque_atual === 0 ? "text-rose-400" : "text-emerald-400"}>{item.estoque_atual} un.</strong> | Necessário: <strong>{item.quantidade_necessaria} un.</strong>
                  </p>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold self-start sm:self-auto ${
                  item.status === "aprovado" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" :
                  item.status === "em_estoque" ? "bg-blue-950 text-blue-400 border border-blue-800" :
                  "bg-amber-950 text-amber-400 border border-amber-800"
                }`}>
                  {item.status === "aprovado" ? "Reposição Recomendada" :
                   item.status === "em_estoque" ? "Estoque Regular" : "Sem Fornecedor Válido"}
                </span>
              </div>

              {item.fornecedores_recomendados && item.fornecedores_recomendados.length > 0 ? (
                <div>
                  <h4 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-3">
                    Locais Encontrados & Cotados:
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {item.fornecedores_recomendados.map((forn, fIdx) => (
                      <div
                        key={fIdx}
                        className={`p-4 rounded-xl border transition-all ${
                          fIdx === 0
                            ? "bg-emerald-950/30 border-emerald-500/50"
                            : "bg-slate-950/60 border-slate-800"
                        }`}
                      >
                        <div className="flex items-start justify-between gap-2">
                          <h5 className="font-semibold text-white text-sm">
                            {fIdx + 1}º {forn.nome_fornecedor}
                            {fIdx === 0 && (
                              <span className="ml-2 text-xs bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded">
                                Principal
                              </span>
                            )}
                          </h5>
                          {forn.link && (
                            <a
                              href={forn.link}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-emerald-400 hover:text-emerald-300 text-xs flex items-center gap-1 flex-shrink-0"
                            >
                              Ver no Maps <ExternalLink className="w-3.5 h-3.5" />
                            </a>
                          )}
                        </div>

                        <p className="text-xs text-slate-400 mt-1 line-clamp-1">
                          {forn.endereco_completo || forn.cidade}
                        </p>

                        {forn.investigacao && (
                          <div className="mt-3 space-y-1 text-xs text-slate-400">
                            <p>
                              Produtos identificados:{" "}
                              {forn.investigacao.produtos_identificados?.length
                                ? forn.investigacao.produtos_identificados.join(", ")
                                : "não encontrado"}
                            </p>
                            <p>
                              Contato:{" "}
                              {forn.investigacao.contatos?.length
                                ? forn.investigacao.contatos.join(", ")
                                : "não encontrado"}
                            </p>
                            <p>
                              Página investigada:{" "}
                              {forn.investigacao.pagina_consultada ? "sim" : "não disponível"}
                            </p>
                            <p>
                              Compatibilidade:{" "}
                              {forn.investigacao.compatibilidade || "não confirmada"}
                            </p>
                            <p>
                              Evidência:{" "}
                              {forn.investigacao.justificativa || "não encontrada"}
                            </p>
                          </div>
                        )}

                        <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                          <span className="text-slate-400">
                            {forn.distancia_km != null
                              ? `${forn.distancia_km} km de distância`
                              : "Distância não informada"}
                          </span>
                          <span className="text-slate-400">
                            Relevância: {forn.relevancia ?? "N/A"}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : null}

              {item.relatorio_decisao && (
                <div className="bg-slate-950 border border-slate-800 rounded-xl p-4">
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                    Resumo do Agente com IA:
                  </h4>
                  <p className="text-sm text-slate-300 whitespace-pre-line leading-relaxed">
                    {item.relatorio_decisao}
                  </p>
                </div>
              )}
            </div>
          ))}
        </section>
      )}
    </main>
  );
}
