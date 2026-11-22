import os
from flask import Flask, render_template_string, request, redirect
import mysql.connector
app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
       password=os.environ["MYSQL_PASSWORD"],
        database="esi_activa"
    )

@app.route("/")
def inicio():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, pregunta, fecha FROM consultas ORDER BY fecha DESC")
    consultas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template_string("""
        <h1>ESI ACTIVA - Chats</h1>
        <form action="/publicar" method="POST">
            <textarea name="pregunta" placeholder="Escribí tu publicación" required></textarea>
            <button type="submit">Publicar</button>
        </form>
        <h2>Publicaciones</h2>
        {% for consulta in consultas %}
            <div>
                <p>{{ consulta[1] }}</p>
                <small>{{ consulta[2] }}</small>
            </div>
        {% endfor %}
    """, consultas=consultas)

@app.route("/publicar", methods=["POST"])
def publicar():
    pregunta = request.form["pregunta"].strip()

    if pregunta:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO consultas (pregunta) VALUES (%s)",
            (pregunta,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)