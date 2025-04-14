import pandas as pd

def atualizar_estoques(caminho_estoque, caminho_produtos, caminho_saida):
    df_estoque = pd.read_excel(caminho_estoque)
    df_produtos = pd.read_excel(caminho_produtos)

    df_estoque['CODIGO'] = df_estoque['CODIGO'].astype(str).str.strip()
    estoque_dict = dict(zip(df_estoque['CODIGO'], df_estoque['DISP. PE']))

    df_produtos['SKU LIMPO'] = df_produtos['Código (SKU)'].astype(str).str.replace(r"(?i)^pedido\s+", "", regex=True).str.strip()

    for idx, row in df_produtos.iterrows():
        sku = row['SKU LIMPO']
        dias = row.get('Dias para preparação', None)
        if sku in estoque_dict and dias not in [0, 2]:
            df_produtos.at[idx, 'Estoque'] = estoque_dict[sku]

    df_produtos.drop(columns=['SKU LIMPO'], inplace=True)
    df_produtos.to_excel(caminho_saida, index=False)
