from flask import Flask, render_template, request, send_file, abort
from os import system, getcwd, listdir
from os.path import join



app = Flask(__name__)

def retira_extensao(texto):
    contador = 0
    for i in range(len(texto)):
        if texto[i] == '.':
            contador = i
    return texto[:contador]

@app.route("/", methods=["POST"])
def post_arquivo():
    # return listdir(getcwd())
    arquivo = request.files.get("arquivo")
    if str(arquivo.filename) != "" and arquivo != None:

        nome_do_arquivo = arquivo.filename
        nome_sem_extensao = retira_extensao(nome_do_arquivo)
        diretorio = join(getcwd(),"temp_files/")
        ip = request.remote_addr.replace(".","_")
        arquivo.save(diretorio + ip + nome_do_arquivo)
        system(f"pdftotext -layout {diretorio + ip + nome_do_arquivo} {diretorio+ip+nome_sem_extensao}.txt")
        return send_file(diretorio+ip+nome_sem_extensao+".txt", as_attachment=True, download_name=nome_sem_extensao+".txt")
    return abort(400, description="Nenhum arquivo foi enviado")
    # return retira_extensao(nome_do_arquivo)


if __name__ == "__main__":
    app.run(port=5001, host='0.0.0.0')