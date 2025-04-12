# 🗃️ Sistema Distribuído de Arquivos em Python

Este projeto implementa um **sistema simples de arquivos distribuídos** usando `Python` e `Sockets`. Ele permite que um cliente se conecte a um servidor para realizar as seguintes operações:

- 📄 Listar arquivos disponíveis no servidor
- ⬆️ Enviar arquivos (upload)
- ⬇️ Baixar arquivos (download)
- 🗑️ Remover arquivos do servidor

---

## 📦 Estrutura do Projeto

```
Distributed file system/
├── client/
│   └── client.py        # Cliente interativo com menu
├── server/
│   ├── server.py        # Servidor que escuta conexões e executa comandos
│   └── files/           # Pasta onde os arquivos enviados são armazenados
└── README.md            # Este guia
```

---

## 🚀 Como iniciar

### 1. Inicie o servidor

No terminal:

```bash
cd server
python3 server.py
```

O servidor estará ouvindo na porta `5001`.

---

### 2. Use o cliente

Em outro terminal:

```bash
cd client
python3 client.py
```

Será exibido um **menu interativo** com as opções.

---

## 🧭 Menu interativo do cliente

```
========= MENU =========
1. Listar arquivos no servidor
2. Enviar arquivo para o servidor
3. Baixar arquivo do servidor
4. Remover arquivo do servidor
0. Sair
```

---

## 🧰 Funcionalidades

### 1. Listar arquivos

Exibe todos os arquivos disponíveis no servidor.

### 2. Enviar arquivo

- O cliente varre sua pasta `/home/seu_usuário` e lista os arquivos encontrados.
- Você pode escolher pelo número exibido ou digitar o caminho completo.
- O arquivo será enviado para a pasta `server/files/`.

### 3. Baixar arquivo

- Solicita o nome do arquivo armazenado no servidor.
- Você pode escolher salvar com o mesmo nome ou outro.

### 4. Remover arquivo

- Remove o arquivo especificado da pasta `server/files/`.

---

## 📌 Requisitos

- Python 3.x
- Sem bibliotecas externas (100% padrão)

---

## 🛠️ Melhorias futuras (ideias)

- Suporte a múltiplos clientes concorrentes (threads)
- Interface gráfica com Tkinter ou web (Flask)
- Log de operações
- Filtros por tipo de arquivo (.txt, .pdf etc.)

---

## 📧 Autor

Feito por Wender Júnior – um projeto educacional de sistemas distribuídos com sockets.
