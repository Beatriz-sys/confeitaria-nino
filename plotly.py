import pandas as pd
import plotly.express as px

df_vendas = pd.read_excel("valor-produto.xlsx")

if 'Meses' not in df_vendas.columns:
    first_col = df_vendas.columns[0]
    df_vendas = df_vendas.rename(columns={first_col: 'Meses'})

fig_line = px.line(
    df_vendas,
    x="Meses",
    y=df_vendas.columns[1:],
    title="Evolução das Vendas por Produto (Ano Todo)",
    markers=True
)

# Salva o gráfico como HTML para integrar na página
fig_line.write_html("grafico_vendas.html", include_plotlyjs=False)
print("Gráfico salvo como grafico_vendas.html!")
