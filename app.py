from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2

app = Flask(__name__)

# Conexão com PostgreSQL
conn = psycopg2.connect(
    dbname="cadastro_atletas",
    user="fabio",
    password="1234",
    host="localhost",
    port="5432"
)

@app.route("/")
def index():
    try:
        cursor = conn.cursor()
        cursor.execute("SET search_path TO public;")
        cursor.execute("SELECT * FROM atletas ORDER BY id ASC;")
        atletas = cursor.fetchall()
        cursor.close()
        return render_template("index.html", atletas=atletas)
    except Exception as e:
        conn.rollback()
        print("Erro ao buscar atletas:", e)
        return "Erro ao buscar atletas", 500

@app.route("/cadastro")
def cadastro():
    editar_id = request.args.get("editar")
    atleta = None
    if editar_id:
        cursor = conn.cursor()
        cursor.execute("SET search_path TO public;")
        cursor.execute("SELECT * FROM atletas WHERE id = %s", (editar_id,))
        atleta = cursor.fetchone()
        cursor.close()
    return render_template("cadastro.html", atleta=atleta)

@app.route("/salvar", methods=["POST"])
def salvar():
    try:
        data = request.form
        editar_id = data.get("editar_id")

        def limpar_num(valor):
            return float(valor) if valor and valor.strip() != "" else None

        nome = data["nome"]
        idade = int(data["idade"])
        tempo = limpar_num(data["tempo_treino"])

        # Coletar até 5 categorias existentes
        categorias = []
        for i in range(1, 6):
            cat = data.get(f"categoria{i}")
            nota = limpar_num(data.get(f"nota{i}"))
            classificacao = data.get(f"classificacao{i}")
            categorias.append((cat, nota, classificacao))

        # Completar com None se tiver menos que 5
        while len(categorias) < 5:
            categorias.append((None, None, None))

        cursor = conn.cursor()
        cursor.execute("SET search_path TO public;")

        if editar_id:
            cursor.execute("""
                UPDATE atletas SET
                    nome = %s, idade = %s, tempo_treino = %s,
                    categoria1 = %s, nota1 = %s, classificacao1 = %s,
                    categoria2 = %s, nota2 = %s, classificacao2 = %s,
                    categoria3 = %s, nota3 = %s, classificacao3 = %s,
                    categoria4 = %s, nota4 = %s, classificacao4 = %s,
                    categoria5 = %s, nota5 = %s, classificacao5 = %s
                WHERE id = %s
            """, (
                nome, idade, tempo,
                categorias[0][0], categorias[0][1], categorias[0][2],
                categorias[1][0], categorias[1][1], categorias[1][2],
                categorias[2][0], categorias[2][1], categorias[2][2],
                categorias[3][0], categorias[3][1], categorias[3][2],
                categorias[4][0], categorias[4][1], categorias[4][2],
                editar_id
            ))
        else:
            cursor.execute("""
                INSERT INTO atletas (
                    nome, idade, tempo_treino,
                    categoria1, nota1, classificacao1,
                    categoria2, nota2, classificacao2,
                    categoria3, nota3, classificacao3,
                    categoria4, nota4, classificacao4,
                    categoria5, nota5, classificacao5
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                nome, idade, tempo,
                categorias[0][0], categorias[0][1], categorias[0][2],
                categorias[1][0], categorias[1][1], categorias[1][2],
                categorias[2][0], categorias[2][1], categorias[2][2],
                categorias[3][0], categorias[3][1], categorias[3][2],
                categorias[4][0], categorias[4][1], categorias[4][2]
            ))

        conn.commit()
        cursor.close()
        return redirect(url_for("index"))
    except Exception as e:
        conn.rollback()
        print("Erro ao salvar atleta:", e)
        return "Erro ao salvar atleta", 500

@app.route("/atualizar_classificacao/<int:atleta_id>", methods=["POST"])
def atualizar_classificacao(atleta_id):
    try:
        data = request.get_json()
        coluna = data.get("coluna")
        valor = data.get("valor")
        if coluna in [f"classificacao{i}" for i in range(1, 6)]:
            cursor = conn.cursor()
            cursor.execute("SET search_path TO public;")
            cursor.execute(f"UPDATE atletas SET {coluna} = %s WHERE id = %s", (valor, atleta_id))
            conn.commit()
            cursor.close()
            return jsonify({"status": "ok"})
        return jsonify({"status": "erro"})
    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar classificação:", e)
        return jsonify({"status": "erro"})

@app.route("/deletar/<int:atleta_id>", methods=["POST"])
def deletar(atleta_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SET search_path TO public;")
        cursor.execute("DELETE FROM atletas WHERE id = %s", (atleta_id,))
        conn.commit()
        cursor.close()
        return redirect(url_for("index"))
    except Exception as e:
        conn.rollback()
        print("Erro ao deletar atleta:", e)
        return "Erro ao deletar atleta", 500
    
@app.route("/api/atleta/<int:atleta_id>")
def api_atleta(atleta_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SET search_path TO public;")
        cursor.execute("SELECT * FROM atletas WHERE id = %s", (atleta_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            keys = [
                "id", "nome", "idade", "tempo_treino",
                "categoria1", "nota1", "classificacao1",
                "categoria2", "nota2", "classificacao2",
                "categoria3", "nota3", "classificacao3",
                "categoria4", "nota4", "classificacao4",
                "categoria5", "nota5", "classificacao5"
            ]
            atleta = dict(zip(keys, row))
            return jsonify(atleta)
        return jsonify({"erro": "Atleta não encontrado"}), 404
    except Exception as e:
        print("Erro na API do atleta:", e)
        return jsonify({"erro": "Erro interno"}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
