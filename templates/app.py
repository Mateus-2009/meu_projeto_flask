from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///livros.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    editora = db.Column(db.String(200), default="Sem Editora")
    ativo = db.Column(db.Boolean, default=False)

    def __init__(self, titulo, autor, categoria, ano, editora="Sem Editora", ativo=False):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.ano = ano
        self.editora = editora
        self.ativo = ativo

    def __repr__(self):
        return f"<Livro {self.titulo}>"
    
with app.app_context():
    db.create_all()

    # Ler o arquivo CSV para um DataFrame
    df = pd.read_csv("tabela - livros.csv")

    # Adicionar cada livro à base de dados, se ainda não estiverem presentes
    for index, row in df.iterrows():
        if not Livro.query.filter_by(titulo=row["Titulo do Livro"]).first():
            livro = Livro(
                titulo=row["Titulo do Livro"],
                autor=row["Autor"],
                categoria=row["Categoria"],
                ano=row["Ano de Publicação"],
                ativo=row["Ativo"] == "TRUE",
            )
            db.session.add(livro)
    db.session.commit()

@app.route("/inicio")
def inicio():
    livros = Livro.query.all()
    return render_template("lista.html", lista_de_livros=livros)

@app.route("/curriculo")
def curriculo():
    return render_template("curriculo.html")

@app.route("/novo")
def novo():
    return render_template("novo.html", titulo="Novo Livro")

@app.route("/criar", methods=["POST"])
def criar():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    categoria = request.form["categoria"]
    ano = request.form["ano"]
    editora = request.form["editora"]

    livro = Livro(
        titulo=titulo, autor=autor, categoria=categoria, ano=ano, editora=editora
    )

    db.session.add(livro)
    db.session.commit()

    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)