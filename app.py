import json

from flask import Flask, request, jsonify
from database import get_connection

app = Flask(__name__)

# Teste API
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API de catalogo de filmes"}), 200

# Ping
@app.route('/ping', methods=['GET'])
def ping():
    conn = get_connection()
    conn.close()
    return jsonify({"message": "pong! API Rodando!", "db": str(conn)}), 200


# 🔹 Listar todos os filmes
@app.route('/filmes', methods=['GET'])
def listar_filmes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM filmes;")
    filmes = cur.fetchall()

    cur.close()
    conn.close()

    resultado = []
    for filme in filmes:
        resultado.append({
            "id": filme[0],
            "titulo": filme[1],
            "ano": filme[2],
            "genero": filme[3]
        })

    return jsonify(resultado)


# 🔹 Buscar filme por ID
@app.route('/filmes/<int:id>', methods=['GET'])
def buscar_filme(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM filmes WHERE id = %s;", (id,))
    filme = cur.fetchone()

    cur.close()
    conn.close()

    if filme is None:
        return jsonify({"erro": "Filme não encontrado"}), 404

    return jsonify({
        "id": filme[0],
        "titulo": filme[1],
        "ano": filme[2],
        "genero": filme[3]
    })


# 🔹 Adicionar novo filme
@app.route('/filmes', methods=['POST'])
def adicionar_filme():
    dados = request.get_json()

    if not dados or not dados.get("titulo"):
        return jsonify({"erro": "Dados inválidos"}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO filmes (titulo, ano, genero) VALUES (%s, %s, %s) RETURNING id;",
        (dados["titulo"], dados["ano"], dados["genero"])
    )

    novo_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "id": novo_id,
        "titulo": dados["titulo"],
        "ano": dados["ano"],
        "genero": dados["genero"]
    }), 201


# 🔹 Atualizar filme
@app.route('/filmes/<int:id>', methods=['PUT'])
def atualizar_filme(id):
    dados = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM filmes WHERE id = %s;", (id,))
    filme = cur.fetchone()

    if filme is None:
        cur.close()
        conn.close()
        return jsonify({"erro": "Filme não encontrado"}), 404

    cur.execute(
        """
        UPDATE filmes
        SET titulo = %s, ano = %s, genero = %s
        WHERE id = %s;
        """,
        (dados["titulo"], dados["ano"], dados["genero"], id)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Filme atualizado com sucesso"})


# 🔹 Remover filme
@app.route('/filmes/<int:id>', methods=['DELETE'])
def deletar_filme(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM filmes WHERE id = %s;", (id,))
    filme = cur.fetchone()

    if filme is None:
        cur.close()
        conn.close()
        return jsonify({"erro": "Filme não encontrado"}), 404

    cur.execute("DELETE FROM filmes WHERE id = %s;", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"mensagem": "Filme removido com sucesso"})


if __name__ == '__main__':
    app.run(debug=True)