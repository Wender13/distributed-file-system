
import tkinter as tk
from tkinter import font, colorchooser, filedialog
import customtkinter as ctk
import xmlrpc.client
import os
from datetime import datetime
import getpass

HOST = "http://localhost:5001/"
proxy = xmlrpc.client.ServerProxy(HOST, allow_none=True)
CLIENTE_HOME_DIR = os.path.expanduser("~")

# Funções do cliente
def executar_comando(comando, args):
    try:
        if comando == "ls":
            path = args[0] if args else ""
            arquivos = proxy.listar_arquivos(path)
            return "\n".join(arquivos) if arquivos else "[vazio]"
        elif comando == "rm":
            return "\n".join(f"{p}: {proxy.remover(p)}" for p in args)
        elif comando == "cp":
            if len(args) != 2:
                return "[ERRO] Uso: cp origem destino"
            origem, destino = args
            return cp(origem, destino)
        elif comando == "mkdir":
            return proxy.criar_diretorio(args[0])
        elif comando == "touch":
            return proxy.criar_arquivo(args[0])
        elif comando == "cat":
            return proxy.cat_file(args[0])
        elif comando == "echo":
            filename = args[0]
            text = " ".join(args[1:])
            return proxy.echo(filename, text)
        else:
            return "[ERRO] Comando desconhecido."
    except Exception as e:
        return f"[ERRO] {e}"

def cp(origem, destino):
    def parse_path(path, is_remote):
        if path.startswith("remote:"):
            return path[7:] or ""
        elif path.startswith("local:"):
            return os.path.join(CLIENTE_HOME_DIR, path[6:])
        return path

    if origem.startswith("remote:"):
        remote_path = parse_path(origem, is_remote=True)
        local_path = parse_path(destino, is_remote=False)
        dados = proxy.download(remote_path)
        if isinstance(dados, xmlrpc.client.Binary):
            if os.path.isdir(local_path) or local_path.endswith(os.sep):
                local_path = os.path.join(local_path, os.path.basename(remote_path))
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(dados.data)
            return f"[DOWNLOAD] {remote_path} -> {local_path}"
        return f"[ERRO] {dados}"
    else:
        local_path = parse_path(origem, is_remote=False)
        remote_path = parse_path(destino, is_remote=True)
        if not os.path.exists(local_path):
            return f"[ERRO] Caminho '{local_path}' não existe."
        if os.path.isdir(local_path):
            return f"[ERRO] '{local_path}' é um diretório, não um arquivo."
        if remote_path.endswith("/"):
            try:
                proxy.criar_diretorio(remote_path)
            except:
                pass
        remote_path = os.path.join(remote_path, os.path.basename(local_path))
        with open(local_path, "rb") as f:
            dados = f.read()
        return proxy.upload(remote_path, xmlrpc.client.Binary(dados))

# Interface gráfica
class TerminalApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RPC Terminal")
        self.geometry("900x600")

        self.font_family = tk.StringVar(value="Courier")
        self.font_size = tk.IntVar(value=14)
        self.bg_color = "#1e1e1e"
        self.fg_color = "#00ff00"

        self.criar_widgets()
        self.aplicar_estilo()

    def criar_widgets(self):
        self.menu_btn = ctk.CTkButton(self, text="⚙️", width=30, command=self.abrir_config)
        self.menu_btn.place(x=10, y=10)

        self.terminal = ctk.CTkTextbox(self, wrap="word", corner_radius=0)
        self.terminal.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.75)

        self.input = ctk.CTkEntry(self)
        self.input.place(relx=0.01, rely=0.88, relwidth=0.85)
        self.input.bind("<Return>", self.processar_comando)

        self.enviar_btn = ctk.CTkButton(self, text="➜", command=lambda: self.processar_comando(None))
        self.enviar_btn.place(relx=0.87, rely=0.88, relwidth=0.12)

        self.atualizar_prompt()

    def atualizar_prompt(self):
        usuario = getpass.getuser()
        path = "~"
        hora = datetime.now().strftime("%H:%M")
        prompt = f"{usuario} em {path} às {hora}\n➜ "
        self.prompt = prompt

    def processar_comando(self, event):
        cmd = self.input.get().strip()
        if not cmd:
            return
        self.terminal.insert("end", f"\n{self.prompt}{cmd}\n")
        parts = cmd.split()
        comando, args = parts[0], parts[1:]
        if comando == "exit":
            self.destroy()
            return
        resposta = executar_comando(comando, args)
        self.terminal.insert("end", resposta + "\n")
        self.input.delete(0, "end")
        self.terminal.see("end")
        self.atualizar_prompt()

    def abrir_config(self):
        config = tk.Toplevel(self)
        config.title("Configurações")
        config.geometry("400x400")

        fontes = sorted(set(p.name for p in Path("~/.local/share/fonts").expanduser().glob("*.ttf")))
        fontes.insert(0, "Courier")

        ctk.CTkLabel(config, text="Fonte:").pack()
        fonte_menu = ctk.CTkOptionMenu(config, values=fontes, variable=self.font_family, command=self.aplicar_estilo)
        fonte_menu.pack()

        ctk.CTkLabel(config, text="Tamanho:").pack()
        tamanho = ctk.CTkSlider(config, from_=10, to=30, number_of_steps=20, variable=self.font_size, command=lambda e: self.aplicar_estilo())
        tamanho.pack()

        ctk.CTkButton(config, text="Cor de texto", command=self.mudar_cor_fg).pack(pady=10)
        ctk.CTkButton(config, text="Cor de fundo", command=self.mudar_cor_bg).pack(pady=10)

    def aplicar_estilo(self, *_):
        f = (self.font_family.get(), self.font_size.get())
        self.terminal.configure(font=f, text_color=self.fg_color, fg_color=self.bg_color)
        self.input.configure(font=f, text_color=self.fg_color, fg_color=self.bg_color)
        self.terminal.update()

    def mudar_cor_fg(self):
        cor = colorchooser.askcolor()[1]
        if cor:
            self.fg_color = cor
            self.aplicar_estilo()

    def mudar_cor_bg(self):
        cor = colorchooser.askcolor()[1]
        if cor:
            self.bg_color = cor
            self.aplicar_estilo()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = TerminalApp()
    app.mainloop()
