# 🚪 API Catraca

API REST desenvolvida em **Python + Flask** para gerenciamento de acesso de alunos em uma catraca, com autenticação via token e integração com **Firebase Firestore**.

---

## 📌 Sobre o projeto

A **API Catraca** tem como objetivo controlar o acesso de alunos por meio do CPF, permitindo:

* ✅ Cadastro de alunos
* 🔍 Validação de acesso
* 🔄 Controle de status (ativo/inativo)
* 🚪 Integração com sistemas de catraca

A API segue o padrão **REST**, utilizando métodos HTTP como `GET`, `POST`, `PATCH` e `DELETE`.

---

## ⚙️ Tecnologias utilizadas

* 🐍 Python
* 🔥 Flask
* ☁️ Firebase Firestore
* 🔐 Autenticação via Token
* 🌐 API REST

---

## 📁 Estrutura do Projeto

```
api_catraca/
│
├── app.py                # Arquivo principal da aplicação
├── config.py             # Configurações do projeto
├── firebase_config.py    # Conexão com Firestore
├── routes/               # Rotas da API
├── utils/                # Funções auxiliares
└── requirements.txt      # Dependências
```

---

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/mantuanpietro/api_catraca.git
cd api_catraca
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

Ative o ambiente:

* **Linux/Mac**

```bash
source venv/bin/activate
```

* **Windows**

```bash
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Firebase

* Adicione sua credencial JSON do Firebase
* Configure a conexão no arquivo correspondente

### 5. Execute a API

```bash
python app.py
```

📍 A API estará disponível em:
👉 http://localhost:5000

---

## 🔐 Autenticação

Algumas rotas exigem autenticação via token.

Envie no header:

```
Authorization: Bearer SEU_TOKEN
```

---

## 📚 Endpoints da API

### 👨‍🎓 Alunos

#### ➕ Cadastrar aluno

```
POST /alunos
```

**Body:**

```json
{
  "nome": "João Silva",
  "cpf": "12345678900",
  "status": "ativo"
}
```

**Respostas:**

* `201` → Aluno cadastrado
* `400` → Dados inválidos
* `500` → Erro interno

---

#### 📋 Listar alunos

```
GET /alunos
```

**Resposta:**

```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "cpf": "12345678900",
    "status": "ativo"
  }
]
```

---

#### 🔍 Buscar aluno por CPF

```
GET /alunos/<cpf>
```

**Respostas:**

* `200` → Aluno encontrado
* `404` → Não encontrado

---

#### ✏️ Atualizar aluno

```
PATCH /alunos/<id>
```

**Body:**

```json
{
  "nome": "Novo Nome",
  "status": "inativo"
}
```

---

#### ❌ Deletar aluno

```
DELETE /alunos/<id>
```

---

#### ✅ Validar acesso (catraca)

```
GET /alunos/validar?cpf=12345678900
```

**Regras:**

* CPF precisa existir
* Status deve ser **ativo**

**Resposta (sucesso):**

```json
{
  "acesso": true
}
```

**Resposta (falha):**

```json
{
  "acesso": false,
  "motivo": "Aluno inativo ou não encontrado"
}
```

---

## ⚠️ Regras de Negócio

* CPF deve ser **único**
* Apenas alunos **ativos** podem acessar
* Validação feita via **query param**
* Tratamento de erro para dados inválidos

---

## 🛡️ Tratamento de erros

A API retorna erros padronizados:

```json
{
  "error": "Mensagem de erro",
  "detalhes": "Descrição técnica"
}
```

---

## 🌐 Deploy

🚀 Acesse a API online:
👉 https://api-catraca-mu.vercel.app/

---

## 📊 Melhorias futuras

* 🔑 Autenticação completa com JWT
* 📈 Logs de acesso à catraca
* 🧾 Histórico de entradas/saídas
* 🧑‍💼 Painel administrativo
* 📄 Documentação com Swagger (Flasgger)

---

## 👨‍💻 Autor

Desenvolvido por **Pietro Mantuan**
