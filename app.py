
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import mysql.connector

app = Flask(__name__)

# Conexion con la base de datos
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ["MYSQL_PASSWORD"],
        database="esi_activa"
    )

# Foro / Chats
@app.route("/")
def inicio():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id, pregunta, fecha FROM consultas ORDER BY fecha DESC")
    consultas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("publicaciones.html", consultas=consultas)

# Publicar en el foro
@app.route("/publicar", methods=["POST"])
def publicar():
    pregunta = request.form.get("pregunta", "").strip()

    if pregunta:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO consultas (pregunta) VALUES (%s)", (pregunta,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    return redirect(url_for("inicio"))

# Pagina de inicio
@app.route("/inicio")
def pagina_inicio():
    return send_from_directory(app.root_path, "inicio.html")

# Mapa
@app.route("/mapa")
def pagina_mapa():
    return send_from_directory(app.root_path, "mapa.html")

# Registro
@app.route("/registro")
def pagina_registro():
    return send_from_directory(app.root_path, "registro.html")

# Guia ESI
@app.route("/guia-esi")
def pagina_guia():
    return send_from_directory(app.root_path, "guia-esi.html")

# Denuncia
@app.route("/denuncia")
def pagina_denuncia():
    return send_from_directory(app.root_path, "denuncia.html")

# Linea 144
@app.route("/linea144")
def pagina_linea144():
    return send_from_directory(app.root_path, "Linea144.html")

# Articulo 1
@app.route("/articulo1")
def articulo_uno():
    return send_from_directory(app.root_path, "articulo1.html")

# Articulo 2
@app.route("/articulo2")
def articulo_dos():
    return send_from_directory(app.root_path, "articulo2.html")

if __name__ == "__main__":
    app.run(debug=True)
