import pyodbc  #ferramenta utilizada pra carregar banco de dados SQL
import pandas as pd  #para ler dados SQL
import matplotlib.pyplot as plt  #para printar gráficos

## Integração padrão com SQL
integracao = ('Driver={SQL Server};'
              'Server=LEANDRO;'
              'Database=ContosoRetailDW;')


with pyodbc.connect(integracao) as conexao:

## Código padrão para executar funções dentro do banco de dados
    cursor = conexao.cursor()

## Para carregar os dados em DataFrame e chunksize para definir a quantidade dividida de dataframes carregados por vez
    lucro_df_iter = pd.read_sql('SELECT * FROM ContosoRetailDW.dbo.FactSales', conexao, chunksize=3500)

    chunks = []

    for chunk in lucro_df_iter:
        chunks.append(chunk)  

## Juntar (concatenar) os chunks divididos em um só
lucro_df = pd.concat(chunks, ignore_index=True)

# print(lucro_df)

## Salvando o DataFrame em um arquivo CSV
lucro_df.to_csv('dados.csv', index=False)

dados_df = pd.read_csv('dados.csv')
dados_df['TotalBR'] = dados_df['SalesAmount'] - dados_df['TotalCost'] - dados_df['DiscountAmount']
# print(dados_df[['SalesAmount','TotalCost', 'DiscountAmount', 'TotalBR']])

## Agrupar e somar os dados do DataFrame
somatorio = dados_df.groupby(['DateKey']).sum()
somatorio['TotalBR'].plot(figsize=(15, 10))
plt.show()