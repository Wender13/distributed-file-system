from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.client import Binary
import os
import shutil

HOST = '0.0.0.0'
PORT = 5001
SERVER_DIR = os.path.join(os.path.dirname(__file__), 'storage')
os.makedirs(SERVER_DIR, exist_ok=True)

class FileManager:
    def listar_arquivos(self, caminho=""):
        path = os.path.join(SERVER_DIR, caminho)
        if os.path.isdir(path):
            return os.listdir(path)
        else:
            return ["Diretorio nao encontrado"]

    def remover(self, nome):
        target = os.path.join(SERVER_DIR, nome)
        if os.path.isfile(target):
            os.remove(target)
            return "Arquivo removido"
        elif os.path.isdir(target):
            shutil.rmtree(target)
            return "Diretorio removido com sucesso"
        else:
            return "Nenhum arquivo ou diretorio encontrado"

    def criar_diretorio(self, nome):
        path = os.path.join(SERVER_DIR, nome)
        os.makedirs(path, exist_ok=True)
        return "Diretorio criado"

    def criar_arquivo(self, nome):
        path = os.path.join(SERVER_DIR, nome)
        open(path, 'a').close()
        return "Arquivo vazio criado"

    def upload(self, nome, dados):
        path = os.path.join(SERVER_DIR, nome)
        os.makedirs(os.path.dirname(path), exist_ok=True)  # Garante que os diretórios existam
        with open(path, 'wb') as f:
            f.write(dados.data)
        return "Arquivo recebido com sucesso"

    def download(self, nome):
        path = os.path.join(SERVER_DIR, nome)
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                return Binary(f.read())
        return "Arquivo nao encontrado"

    
    def cat_file(self, filename):
        path = os.path.join(SERVER_DIR, filename)
        if not os.path.exists(path):
            return "ERRO: Arquivo não encontrado"

        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            return "ERRO: Arquivo não é um arquivo de texto legível."
        except Exception as e:
            return f"ERRO ao ler arquivo: {e}"

    def echo(args):
        if not args:
            print("[ERRO] Nome do arquivo não informado")
            return
        filename = args[0]
        text = input("Digite o texto a ser adicionado: ")
        try:
            resposta = proxy.echo(filename, text)
            print(resposta)
        except Exception as e:
            print("[ERRO]", e)

    def echo(self, filename, text):
        filepath = os.path.join(SERVER_DIR, filename)
        if not os.path.exists(filepath):
            return "ERRO: Arquivo não encontrado"

        try:
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(text + "\n")
            return "OK: Texto adicionado com sucesso"
        except Exception as e:
            return f"ERRO ao escrever no arquivo: {e}"


# Handler restrito ao caminho /
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/',)

def main():
    with SimpleXMLRPCServer((HOST, PORT), requestHandler=RequestHandler, allow_none=True) as server:
        server.register_introspection_functions()
        server.register_instance(FileManager())
        print(f"[SERVIDOR RPC] Online em {HOST}:{PORT}")
        server.serve_forever()

if __name__ == '__main__':
    main()