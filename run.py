#!/usr/bin/env python3
from flask import Flask, Response, request, render_template
from analisysrepository import AnalisysRepository
import io
import matplotlib.pyplot as plt
from parser_raw import ParserRaw
from documentsrepository import DocumentsRepository
from datetime import datetime
from parsermaterdomini import ParserMaterDomini

app = Flask(__name__)
SQLITE_FILE = "analisys.db"

@app.route("/")
def home():
    analisysRepo = AnalisysRepository(SQLITE_FILE)
    documentsRepo = DocumentsRepository(SQLITE_FILE)

    names= analisysRepo.get_all_names()
    names = [name[0] for name in names]
    
    documents = documentsRepo.get_all()
    return render_template(
        "home.html",
        names=names,
        documents = documents,
    )

@app.route("/details/<name>")
def details(name):
    repo = AnalisysRepository(SQLITE_FILE)
    text = "<a href='/'>Back</a>"
    text += f"<h1>Details for {name}</h1>"
    text += f"<img src='/graph/{name}'/>"
    text += "<h2>Values</h2>"
    text += f"<table><tr><th>Date</th><th>Value</th></tr>"
    for value in repo.get_all_values_by_name(name):
        text += f"<tr><td>{value[0]}</td><td>{value[2]}</td></tr>"
    text += "</table>"
    
    return text

@app.route("/graph/<name>")
def graph(name):
    repo = AnalisysRepository(SQLITE_FILE)
    values = repo.get_all_values_by_name(name)
    dates = [value[0] for value in values]
    values = [value[2] for value in values]

    # Create the figure and axis
    fig, ax = plt.subplots()
    ax.plot(dates, values, marker='o', linestyle='-')

    # Save to a BytesIO object
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    plt.close(fig)  # Close the figure to free memory
    img_io.seek(0)

    return Response(img_io, mimetype='image/png')

@app.route("/document/upload", methods=["POST"])
def upload_document():
    file = request.files['file']
    if not file:
        return "No file uploaded"

    file.save(f"./documents/{file.filename}")

    parsers = {
        "generic": ParserRaw,
        "analisys_materdomini": ParserMaterDomini,
    }
    parser = parsers[request.form["type"]](f"./documents/{file.filename}")
    values = parser.get_all_values()
    return render_template(
        "upload_document.html",
        text=parser.raw_content,
        values = values,
        filename=file.filename,
    )


@app.route("/document/save", methods=["POST"])
def save_document():
    documents_repo = DocumentsRepository(SQLITE_FILE)
    analisys_repo = AnalisysRepository(SQLITE_FILE)

    date_str = request.form["date"]
    date = datetime.strptime(date_str, "%Y-%m-%d")
    prestazione = request.form["prestazione"]
    filename = request.form["filename"]
    content = request.form["content"]

    analisys_names = request.form.getlist("analisys_names[]")
    analisys = request.form.getlist("analisys[]")

    try:
        document_id = documents_repo.insert(filename, date, prestazione, content)

        for analisys_name, value in zip(analisys_names, analisys):
            analisys_repo.insert(document_id, date, analisys_name, value)
        
    except Exception as e:
        return f"Error: {e} <br> <a href='/'>Back</a>"
    return "File uploaded correctly <br /><a href='/'>Back</a>"

@app.route("/document/<id>")
def document_detail(id):
    repo = DocumentsRepository(SQLITE_FILE)
    document = repo.get_by_id(id)
    return render_template(
        "document_detail.html",
        document=document,
    )



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=8000)
