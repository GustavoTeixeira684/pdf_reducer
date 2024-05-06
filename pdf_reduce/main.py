from flask import Flask, request, send_file, abort
from os import system, getcwd, remove
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
        diretorio = join(getcwd(),"temp_files/")
        ip = request.remote_addr.replace(".","_")
        arquivo.save(diretorio + ip +nome_do_arquivo)
        system(f"gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dNOPAUSE -dQUIET -dBATCH -dColorImageResolution={int(request.form.get('selectDPI'))} -sOutputFile={diretorio+ip}pdf_reduced.pdf {diretorio + ip +nome_do_arquivo}")
        remove(diretorio+ip+nome_do_arquivo)
        return send_file(diretorio+ip+"pdf_reduced.pdf", as_attachment=True, download_name="pdf_reduced.pdf")
    return abort(400, description="Nenhum arquivo foi enviado")
    


if __name__ == "__main__":
    app.run(port=5002, host='0.0.0.0')