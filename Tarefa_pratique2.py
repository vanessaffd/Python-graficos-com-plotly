import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
from dash import Dash,html,dcc

df=pd.read_csv('ecommerce_estatistica.csv')


pd.set_option('display.width',None)
pd.set_option('display.max_colwidth',None)


#Grafico de Histograma
fig1=px.histogram(df , x='Preço', nbins=30 ,title ='Histograma - Preços')


# Gráfico de dispersão
fig2 = px.scatter(df, x='Nota', y='Preço' ,color='Qtd_Vendidos', hover_data='Marca')
fig2.update_layout(
    title='Dispersão-Preço e Nota',
    xaxis_title='Nota',
    yaxis_title= 'Preço'
)

# # Mapa de calor
df_corr= df[['Nota_MinMax', 'N_Avaliações_MinMax', 'Desconto_MinMax', 'Preço_MinMax','Qtd_Vendidos_Cod']].corr()
fig3=px.imshow(df_corr,text_auto=True,color_continuous_scale= px.colors.sequential.Blues_r)
fig3.update_layout(
    xaxis_title='Variáveis',
    yaxis_title='Variáveis',
    title= 'Mapa de Calor - Correlação'
)

# # Gráfico de barra
fig4=px.bar(df, x='Nota',y='Preço', title='Distribuição de Notas por Preço')
fig4.update_layout(
    xaxis_title='Nota',
    yaxis_title='Preço'
)

# Gráfico de pizza
fig5 = px.pie(df , names= 'Qtd_Vendidos', color= 'Qtd_Vendidos',hole=0.6, color_discrete_sequence=px.colors.sequential.Blues_r)
fig5.update_layout(
    title='Gráfico de Pizza - Categoria Quantidade de Vendidos'
)
# # Gráfico de densidade
dados_preco = pd.to_numeric(df['Preço'], errors='coerce').dropna()

kde=gaussian_kde(dados_preco)
x_range = np.linspace(min(dados_preco), max(dados_preco), 1000)
y_kde=kde(x_range)
fig6=go.Figure()
fig6.add_trace(go.Scatter(
    x=x_range,
    y=y_kde,
    mode='lines',
    fill='tozeroy',
    name='Densidade'
))

fig6.update_layout(
    title='Densidade de Preço',
    xaxis_title='Preço',
    yaxis_title='Densidade'
)


#
#
# # Gráfico de Regressão
fig7=px.scatter(df, x='N_Avaliações_MinMax' , y='Qtd_Vendidos_Cod', trendline='ols', title= 'Regressão do Número de Avaliações pela Quantidade de Vendas')



#Cria app
app= Dash(__name__)

app.layout= html.Div([
    dcc.Graph(figure=fig1, id='fig1'),
    dcc.Graph(figure=fig2, id='fig2'),
    dcc.Graph(figure=fig3, id='fig3'),
    dcc.Graph(figure=fig4, id='fig4'),
    dcc.Graph(figure=fig5, id='fig5'),
    dcc.Graph(figure=fig6, id='fig6'),
    dcc.Graph(figure=fig7, id='fig7')
])

#Executa App
app.run(debug=True, port=8050)