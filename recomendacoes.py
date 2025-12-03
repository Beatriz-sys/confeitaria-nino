from flask import Blueprint, render_template
import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity

recomendacoes_bp = Blueprint("recomendacoes", __name__)

# Dados fictícios (você pode trocar por dados do banco)
data = {
    "Mil folhas": [1, 0, 0, 1, 0],
    "Cestas": [0, 1, 0, 1, 0],
    "Eclairs": [1, 0, 1, 0, 0],
    "Gateus": [0, 1, 1, 0, 0],
    "Bolos": [1, 0, 0, 1, 1],
    "Dama-emporio": [0, 1, 0, 1, 1],
    "Presentes": [1, 0, 1, 0, 1],
    "Mil folhas Tradicional": [1, 1, 0, 0, 0],
    "Tortas": [0, 1, 1, 0, 0]
}
usuarios = ["Usuário1", "Usuário2", "Usuário3", "Usuário4", "Usuário5"]

df = pd.DataFrame(data, index=usuarios)
produto_matrix = df.T
sim_df = pd.DataFrame(
    cosine_similarity(produto_matrix),
    index=produto_matrix.index,
    columns=produto_matrix.index
)

# Dicionário de imagens (adicione aqui)
imagens_produtos = {
    "Mil folhas": "mil-folhas.png",
    "Cestas": "cestas.jpg",
    "Eclairs": "eclairs.jpg",
    "Gateus": "gateus.jpg",
    "Bolos": "bolos.jpg",
    "Dama-emporio": "dama-emporio.jpg",
    "Presentes": "presentes.jpg",
    "Mil folhas Tradicional": "mil-tradicional.jpg",
    "Tortas": "tortas.jpg"
}


def recomendar_produto(produto, n=3):
    if produto not in sim_df.columns:
        # se produto não existir, retorna os n primeiros produtos como fallback
        return list(sim_df.columns[:n])
    similares = sim_df[produto].sort_values(ascending=False)
    similares = similares.drop(produto)  # remove o próprio produto
    return list(similares.head(n).index)


@recomendacoes_bp.route("/recomendar/<produto>")
def recomendar(produto):
    recomendados = recomendar_produto(produto)
    return render_template(
        "recomendacoes.html",
        produto=produto,
        recomendados=recomendados,
        imagens_produtos=imagens_produtos  # <-- aqui você passa o dicionário pro template
    )