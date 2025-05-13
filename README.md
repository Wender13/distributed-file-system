# 🧠 Shell RPC - Sistema de Arquivos Distribuído

Este shell permite interação remota com um servidor de arquivos via **XML-RPC**, simulando comandos comuns de sistemas Unix para manipulação de arquivos e diretórios de forma distribuída.

---

## 🚀 Como usar

### 1. **Configuração**

No início do script, configure o host do servidor XML-RPC:

```python
HOST = "http://localhost:5001/"
```

Mude `localhost` e a porta conforme o endereço do seu servidor.

---

## 📦 Comandos Disponíveis

### `ls [CAMINHO]`

Lista arquivos e pastas de um diretório remoto.

- **Sem argumentos**: lista o diretório raiz remoto.
- **Com caminho**: lista o conteúdo de um diretório específico.

```bash
ls
ls pasta/
```

---

### `rm CAMINHO1 CAMINHO2 ...`

Remove um ou mais arquivos ou diretórios no servidor remoto.

```bash
rm arquivo1.txt pasta/arquivo2.txt
```

---

### `cp ORIGEM DESTINO`

Copia arquivos entre o cliente e o servidor.

#### Upload (cliente ➝ servidor)

```bash
cp local:meuarquivo.txt remote:
```

#### Download (servidor ➝ cliente)

```bash
cp remote:documento.pdf local:
```

> 📌 **Importante:** Se o destino for apenas `remote:` ou `local:` (sem caminho específico), o arquivo será enviado ou baixado diretamente para a **pasta principal (HOME)** do respectivo lado.

---

### `mkdir NOME_DO_DIRETORIO`

Cria um novo diretório remoto.

```bash
mkdir nova_pasta
```

---

### `touch NOME_DO_ARQUIVO`

Cria um arquivo vazio no servidor remoto.

```bash
touch novo_arquivo.txt
```

---

### `cat NOME_DO_ARQUIVO`

Exibe o conteúdo de um arquivo remoto.

```bash
cat relatorio.txt
```

---

### `echo NOME_DO_ARQUIVO`

Adiciona texto a um arquivo remoto.

```bash
echo anotacoes.txt
Digite o texto a ser adicionado: Revisar comandos RPC.
```

---

### `help`

Exibe os comandos disponíveis se não houver argumento, adicione um argumento (comando) para ver detalhes sobre o mesmo.

---

### `exit`

Encerra o shell.

---

## 📝 Observações

- **Prefixos obrigatórios em `cp`**:
  - `local:` para caminhos locais (cliente).
  - `remote:` para caminhos remotos (servidor).
- **Arquivos baixados** terão seus diretórios criados automaticamente, se necessário.
- **Arquivos enviados** devem existir localmente e não podem ser diretórios.

---

## 🛠️ Requisitos

- Python 3
- Servidor XML-RPC ativo escutando na porta configurada.

---

## 📂 Exemplo de Execução

```bash
➜ ls
➜ mkdir arquivos
➜ cp local:exemplo.txt remote:arquivos/
➜ cp remote:arquivos/exemplo.txt local:copias/
➜ cat remote:arquivos/exemplo.txt
➜ echo remote:arquivos/exemplo.txt
➜ exit
```

---

## 📧 Suporte

Para dúvidas ou sugestões, abra uma issue ou envie um pull request.

---
