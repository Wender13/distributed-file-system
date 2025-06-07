import tkinter.font
from tkinter import colorchooser
import pathlib
import customtkinter as ctk
from tkinter import messagebox
import xmlrpc.client
import os
import socket
import datetime

# Aparência inicial
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Conexão RPC
proxy = xmlrpc.client.ServerProxy("http://localhost:5001/", allow_none=True)

# === Janela Principal ===
app = ctk.CTk()
app.title("RPC Terminal ZSH")
app.geometry("1000x600")
app.configure(fg_color="#101010")  # terminal black

# Transparência inicial
app.attributes('-alpha', 0.95)

# Estado visual (pode ser atualizado pela janela de config)
state = {
    "bg": "#101010",
    "fg": "#00ff88",
    "font": ("Courier New", 13),
    "alpha": 0.95
}

# === Caixa de Saída do Terminal ===
output = ctk.CTkTextbox(app, font=state["font"], fg_color=state["bg"], text_color=state["fg"])
output.pack(fill="both", expand=True, padx=10, pady=(10, 0))
output.configure(state="normal")
output.insert("end", "🧠 Conectado a RPC Server...\nDigite comandos como em um terminal.\n\n")
output.configure(state="disabled")

# === Campo de Entrada ===
entry = ctk.CTkEntry(app, font=state["font"], placeholder_text="Digite comandos aqui...")
entry.pack(fill="x", padx=10, pady=10)

# === Função do Prompt estilo zsh ===
def gerar_prompt():
    user = os.getenv("USER") or "usuario"
    host = socket.gethostname()
    path = os.getcwd().replace(os.path.expanduser("~"), "~")
    hora = datetime.datetime.now().strftime("%H:%M")
    return f"{user}@{host} {path} [{hora}] ➜ "

# === Execução do Comando ===
def executar_comando(event=None):
    comando = entry.get().strip()
    if not comando:
        return

    prompt = gerar_prompt()

    output.configure(state="normal")
    output.insert("end", f"{prompt}{comando}\n")

    try:
        args = comando.split()
        cmd = args[0]
        path = args[1] if len(args) > 1 else ""
        text = " ".join(args[2:]) if len(args) > 2 else ""

        match cmd:
            case "ls": result = proxy.listar_arquivos(path)
            case "rm": result = proxy.remover(path)
            case "mkdir": result = proxy.criar_diretorio(path)
            case "touch": result = proxy.criar_arquivo(path)
            case "cat": result = proxy.cat_file(path)
            case "echo": result = proxy.echo(path, text)
            case "help":
                result = (
                    "📖 Comandos disponíveis:\n"
                    "  ls [path]           → Listar arquivos\n"
                    "  rm [path]           → Remover arquivo/pasta\n"
                    "  mkdir [path]        → Criar diretório\n"
                    "  touch [path]        → Criar arquivo\n"
                    "  cat [path]          → Ler conteúdo do arquivo\n"
                    "  echo [path] [texto] → Escrever texto no arquivo\n"
                    "  clear               → Limpar terminal\n"
                    "  help                → Mostrar ajuda"
                )
            case "clear":
                output.delete("1.0", "end")
                entry.delete(0, "end")
                return
            case _: result = f"[Comando desconhecido] Digite 'help' para ajuda."

        if isinstance(result, list):
            result = "\n".join(result) if result else "[vazio]"
        output.insert("end", f"{result}\n\n")
    except Exception as e:
        output.insert("end", f"[ERRO] {e}\n\n")

    entry.delete(0, "end")
    output.see("end")
    output.configure(state="disabled")

entry.bind("<Return>", executar_comando)

# === Janela de Configurações ===
def abrir_config():
    config = ctk.CTkToplevel(app)
    config.title("Configurações do Terminal")
    config.geometry("400x300")

    # Cor de fundo
    ctk.CTkLabel(config, text="Cor de Fundo").pack()
    bg_menu = ctk.CTkOptionMenu(config, values=["#101010", "#202020", "#1f1f2e", "#000000"], command=lambda c: atualizar_cor("bg", c))
    bg_menu.set(state["bg"])
    bg_menu.pack(pady=5)

    # Cor do texto
    ctk.CTkLabel(config, text="Cor do Texto").pack()
    fg_menu = ctk.CTkOptionMenu(config, values=["#00ff88", "#00ffff", "#ffffff", "#ffcc00"], command=lambda c: atualizar_cor("fg", c))
    fg_menu.set(state["fg"])
    fg_menu.pack(pady=5)

    # Fonte
    ctk.CTkLabel(config, text="Fonte").pack()
    fontes = ["Courier New", "Consolas", "Ubuntu Mono", "Monaco"]
    font_menu = ctk.CTkOptionMenu(config, values=fontes, command=lambda f: atualizar_fonte(f))
    font_menu.set(state["font"][0])
    font_menu.pack(pady=5)

    # Transparência
    ctk.CTkLabel(config, text="Transparência").pack()
    slider = ctk.CTkSlider(config, from_=0.6, to=1.0, number_of_steps=4, command=lambda val: atualizar_transparencia(float(val)))
    slider.set(state["alpha"])
    slider.pack(pady=10)

def atualizar_cor(tipo, valor):
    state[tipo] = valor
    output.configure(**{f"{'fg' if tipo == 'fg' else 'fg_color'}": valor})

def atualizar_fonte(fonte):
    state["font"] = (fonte, 13)
    output.configure(font=state["font"])
    entry.configure(font=state["font"])

def atualizar_transparencia(valor):
    state["alpha"] = valor
    app.attributes('-alpha', valor)

# === Botão de Configuração ===
botao_config = ctk.CTkButton(app, text="⚙️", width=30, command=abrir_config)
botao_config.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

app.mainloop()