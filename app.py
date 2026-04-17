from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from auth import gerar_token, token_obrigatorio
import json
from dotenv import load_dotenv
import os


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app, origins="*")


# Configurações de Administrador
ADM_USUARIO = os.getenv("ADM_USUARIO")
ADM_SENHA = os.getenv("ADM_SENHA")

# Inicialização do Firebase
if os.getenv("VERCEL"):
    cred = credentials.Certificate(json.loads(os.getenv("FIREBASE_KEY")))
else:
    cred = credentials.Certificate("firebase.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


# ---- Rotas publicas e login ----

#Rotaa raiz para verificar se a API está rodando (GET / )
@app.route("/", methods=["GET"])
def root():
    return jsonify({
        'app': 'API Catraca',
        'author': 'Pietro e Mauro',
        'version': '2.0'
    }), 200

# Rota de login para autenticar o administrador e gerar um token JWT (POST /login)
@app.route("/login", methods=["POST"])
def login():
    """
    Rota de login para autenticar o administrador e gerar um token JWT.

    Requisição:
    - JSON com "usuario" e "senha"

    Resposta:
    - JSON com "token" se as credenciais forem válidas
    - Erro 401 se as credenciais forem inválidas
    """
    dados = request.get_json()
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if usuario == ADM_USUARIO and senha == ADM_SENHA:
        token = gerar_token(usuario)
        return jsonify({"token": token})
    else:
        return jsonify({"erro": "Credenciais inválidas."}), 401


#Rota para pegar todos os alunos (GET /alunos)
@app.route("/alunos", methods=["GET"])
def alunos_get():
    alunos = []
    lista = db.collection("alunos").stream() #stream() para pegar todos os dados da coleção "catraca" (listar)

    for item in lista:
        alunos.append(item.to_dict()) #to_dict() para converter os dados do firestore em um formato de dicionário

    return jsonify(alunos), 200

#Rota para pegar um aluno específico por ID (GET /alunos/<id>)
@app.route("/alunos/id/<int:id>", methods=["GET"])
def aluno_get_id(id):
    docs = db.collection("alunos").where("id", "==", id).limit(1).get() #where() para filtrar os dados da coleção "catraca" pelo campo "id" e limit(1) para limitar a busca a um único resultado

    if not docs:
        return jsonify({"error": "Aluno não encontrado!"}), 404
    
    aluno = docs[0].to_dict() #to_dict() para converter os dados do firestore em um formato de dicionário
    return jsonify(aluno), 200


#Rota para pegar um aluno específico por cpf (GET /alunos/<cpf>)
@app.route("/alunos/cpf/<cpf>", methods=["GET"])
def aluno_get_cpf(cpf):
    lista = db.collection("alunos").where("cpf","==",cpf).select(["nome","cpf","status"]).stream() #stream() para pegar todos os dados da coleção "alunos" (listar)

    for item in lista:
        return jsonify(item.to_dict()), 200
    return jsonify({ 'message': 'Aluno não encontrado!' }), 404

#rota para validar se o aluno está ativo ou não atraves do cpf (GET /alunos/validar)
@app.route("/alunos/validar", methods=["GET"])
def validar_aluno_get():
    cpf = request.args.get("cpf")

    if not cpf:
        return jsonify({"error": "CPF é obrigatório!"}), 400
    
    # Busca apenas o primeiro documento correspondente
    docs = db.collection("alunos").where("cpf", "==", cpf).limit(1).get()

    if not docs:
        return jsonify({"message": "Aluno não encontrado!"}), 404

    for doc in docs:
        aluno = doc.to_dict()
        if aluno.get("status"):
            return jsonify({"message": "Aluno ativo!"}), 200
        else:
            return jsonify({"message": "Aluno inativo!"}), 200


# Rotas privadas (protegidas por token JWT) (POST, PATCH, DELETE)    
# Rota de atualizar um aluno existente por ID (PATCH /alunos/<id>) alteração parcial
@app.route("/alunos", methods=["POST"])
@token_obrigatorio
def alunos_post():
  
    dados = request.get_json()

    if not dados or "nome" not in dados or "cpf" not in dados or "status" not in dados:
        return jsonify({"error": "Dados inválidos ou incompletos!"}), 400

    try:
        # Verifica CPF ANTES de salvar
        aluno_existente = db.collection("alunos").where("cpf", "==", dados["cpf"]).limit(1).get()

        if aluno_existente:
            return jsonify({"error": "CPF já cadastrado!"}), 400  

        # Controle de ID (tratando erro de documento inexistente)
        contador_ref = db.collection("contador").document("controle_id")
        contador_doc = contador_ref.get()

        if contador_doc.exists:
            ultimo_id = contador_doc.to_dict().get("ultimo_id", 0)
        else:
            ultimo_id = 0

        novo_id = ultimo_id + 1

        #  Atualiza contador
        contador_ref.set({"ultimo_id": novo_id})

        # Salva aluno
        db.collection("alunos").add({
            "id": novo_id,
            "cpf": dados["cpf"],
            "nome": dados["nome"],
            "status": dados["status"]  # agora usa o valor enviado
        })

        return jsonify({"message": "Aluno adicionado com sucesso!"}), 201

    except Exception as e:
        return jsonify({
            "error": "Falha ao adicionar aluno!",
            "detalhes": str(e)
        }), 500

#Rota para atualizar um aluno existente por ID (PATCH /alunos/<id>) alteração parcial
@app.route("/alunos/<int:id>", methods = ['PATCH'])
def alunos_patch(id):

    dados = request.get_json()
    
    if not dados or ("cpf" not in dados and "nome" not in dados and "status" not in dados):
        return jsonify({"error": "Dados inválidos ou incompletos!"}), 400
        
    try:
        docs = db.collection("alunos").where("id", "==", id).limit(1).get()
        if not docs:
            return jsonify({"error": "Aluno não encontrado!"}), 404
        
        doc_ref = db.collection("alunos").document(docs[0].id)
        upd_aluno = {}
        if "nome" in dados:
            upd_aluno["nome"] = dados["nome"]
        
        if "cpf" in dados:
            upd_aluno["cpf"] = dados["cpf"]

        if "status" in dados:
            upd_aluno["status"] = dados["status"]
        
        doc_ref.update(upd_aluno)
        return jsonify({"message": "Aluno atualizado com sucesso!"}), 200
    except:
        return jsonify({"error": "Falha ao atualizar o aluno!"}), 400


#Rota para deletar um aluno por ID (DELETE /alunos/<id>)
@app.route("/alunos/<int:id>", methods = ['DELETE'])
@token_obrigatorio
def alunos_delete(id):
   
    docs = db.collection("alunos").where("id", "==", id).limit(1).get()

    if not docs:
        return jsonify({"error": "Aluno não encontrado!"}), 404
    
    doc_ref = db.collection("alunos").document(docs[0].id)
    doc_ref.delete()
    return jsonify({"message": "Aluno deletado com sucesso!"}), 200
    


if __name__ == "__main__":
    app.run(debug=True)
