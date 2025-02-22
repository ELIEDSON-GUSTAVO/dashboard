from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

# Simulando um banco de dados (lista)
items = []

@app.route("/")
def home():
    return render_template("index.html", items=items)

@app.route("/add", methods=["GET", "POST"])
def add_data():
    if request.method == "POST":
        activity = request.form["activity"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        estimated_time = float(request.form["estimated_time"])

        # Convertendo para datetime
        start_dt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
        end_dt = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")

        # Calculando tempo real gasto
        duration_hours = (end_dt - start_dt).total_seconds() / 3600

        # Definindo status de acordo com tempo estimado
        status = "Dentro do prazo" if duration_hours <= estimated_time else "Atrasado"

        items.append({
            "activity": activity,
            "start_time": start_dt.strftime("%d/%m/%Y %H:%M"),
            "end_time": end_dt.strftime("%d/%m/%Y %H:%M"),
            "duration": round(duration_hours, 2),
            "estimated_time": estimated_time,
            "status": status
        })
        return redirect(url_for("home"))

    return render_template("add.html")

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit_data(index):
    if 0 <= index < len(items):
        if request.method == "POST":
            # Editando os dados
            activity = request.form["activity"]
            start_time = request.form["start_time"]
            end_time = request.form["end_time"]
            estimated_time = float(request.form["estimated_time"])

            # Convertendo para datetime
            start_dt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
            end_dt = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")

            # Calculando tempo real gasto
            duration_hours = (end_dt - start_dt).total_seconds() / 3600

            # Atualizando status
            status = "Dentro do prazo" if duration_hours <= estimated_time else "Atrasado"

            items[index] = {
                "activity": activity,
                "start_time": start_dt.strftime("%d/%m/%Y %H:%M"),
                "end_time": end_dt.strftime("%d/%m/%Y %H:%M"),
                "duration": round(duration_hours, 2),
                "estimated_time": estimated_time,
                "status": status
            }

            return redirect(url_for("home"))
        
        # Preenche os campos com os dados atuais para edição
        item = items[index]
        return render_template("edit.html", item=item, index=index)

    return redirect(url_for("home"))

@app.route("/delete/<int:index>")
def delete_item(index):
    if 0 <= index < len(items):
        items.pop(index)
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", items=items)

if __name__ == "__main__":
    # Use a porta definida pela variável de ambiente PORT ou 5000 como padrão
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
