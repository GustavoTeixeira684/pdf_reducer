from flask import Flask, render_template, request, send_file, abort
import requests
import pandas as pd
from datetime import date, datetime
from os import getcwd, path, remove, listdir

app = Flask(__name__)

def retira_extensao(texto):
    contador = 0
    for i in range(len(texto)):
        if texto[i] == '.':
            contador = i
    return texto[:contador]

def grava_log(acao, hora, nome_arquivo_entrada, nome_arquivo_saida):
    with open(getcwd()+"/log/log_archive.csv", 'r+') as file:
        texto = file.read()
        file.write(f"{acao};{hora};{nome_arquivo_entrada};{nome_arquivo_saida}\n")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/convert")
def convert():
    return render_template('convert.html')

@app.route("/reduce")
def reduce():
    return render_template('reduce.html')

@app.route("/pdf_to_txt", methods=["POST"])
def pdf_to_txt():
    arquivo = request.files.get("arquivo")
    if arquivo.filename != "" and arquivo != None:
        ip = request.remote_addr
        nome_sem_extensao = retira_extensao(arquivo.filename)
        diretorio = getcwd()+"/temp_files/"
        dados = {"arquivo": arquivo}
        response = requests.post("http://127.0.0.1:5001", files=dados)
        with open(diretorio+ip+nome_sem_extensao+".txt", 'wb') as file:
            file.write(response.content)

        grava_log("pdf_to_txt", datetime.now(), arquivo.filename, nome_sem_extensao+".txt")
        return send_file(diretorio+ip+nome_sem_extensao+".txt", as_attachment=True, download_name=nome_sem_extensao+".txt")
    return abort(400, description="Nenhum arquivo foi enviado")

@app.route("/pdf_reduce", methods=["POST"])
def pdf_reduce():
    arquivo = request.files.get("arquivo")
    if arquivo.filename != "" and arquivo != None:
        dpi = request.form.get("selectDPI")
        ip = request.remote_addr
        diretorio = getcwd()+"/temp_files/"
        arquivos = {"arquivo": arquivo}
        dados = {"selectDPI" : dpi}
        response = requests.post("http://127.0.0.1:5002", files=arquivos, data=dados)
        with open(diretorio + ip + "pdf_reduced.pdf", 'wb') as file:
            file.write(response.content)
        grava_log("pdf_reduce", datetime.now(), arquivo.filename, "pdf_reduced.pdf")

        return send_file(diretorio + ip + "pdf_reduced.pdf", as_attachment=True, download_name="pdf_reduced.pdf")
    return abort(400, description="Nenhum arquivo foi enviado")

@app.route("/log", methods=["POST"])
def gera_log():
    hoje = datetime.today()
    um_mes_atras = pd.to_datetime(date(hoje.year, hoje.month-1, hoje.day))

    df = pd.read_csv(getcwd()+"/log/log_archive.csv", sep=";", header=None)
    df[1] = pd.to_datetime(df[1])
    df = df[df[1] >= um_mes_atras]
    df.to_csv(getcwd()+"/temp_files/log_download.csv", sep=';', header=False)
    
    
    return send_file(getcwd()+"/temp_files/log_download.csv", as_attachment=True, download_name="log_download.csv")


    
# Optamos por armazenar o log em um arquivo txt mesmo nesse trabalho. Uma vez que o log é simples
if __name__ == "__main__":
    # Garante que o arquivo exista
    if not path.isfile(getcwd()+"/log/log_archive.csv"):
        arquivo = open(getcwd()+"/log/log_archive.csv", 'w')
        arquivo.flush()
        arquivo.close()

    apagar = listdir(getcwd()+"/temp_files/")
    for item in apagar:
        remove(getcwd()+"/temp_files/"+item)

    app.run(debug=True, port=8080, host='0.0.0.0')
    