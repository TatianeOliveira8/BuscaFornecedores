import "./globals.css";

export const metadata = {
  title: "SmartRestock - Reposição Inteligente de Estoque",
  description: "Agente autônomo com IA e busca no Google para compras de delivery",
};

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased">
        {children}
      </body>
    </html>
  );
}
