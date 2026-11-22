
import os
from flask import Flask, render_template, request, redirect, url_for
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

    cursor.execute(
        "SELECT id, pregunta, fecha FROM consultas ORDER BY fecha DESC"
    )
    consultas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("publicaciones.html", consultas=consultas)


@app.route("/publicar", methods=["POST"])
def publicar():
    pregunta = request.form.get("pregunta", "").strip()

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

    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
