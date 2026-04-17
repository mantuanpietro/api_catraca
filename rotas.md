@app.route("/aluno", methods =['GET'])
def get_aluno():
    charada = random.choice(charadas)
    return jsonify(charada), 200

#method POST para adicionar um novo aluno na academia
@app.route("/aluno", methods =['POST'])
def criar_charadas():
    dados = request.get_json()


    nova_charada = {
            "pergunta": dados["pergunta"],         
            "resposta": dados["resposta"]
        }
    charadas.append(nova_charada) 
    return jsonify({"message": "Charada criada com sucesso","charada":nova_charada}), 201

#rota para deletar charada
@app.route("/charadas/<int:index>", methods =['DELETE'])
def deletar_charada(index):
    if index < 0 or index >= len(charadas):
        return jsonify({"error": "Índice inválido."}), 400

    charada_deletada = charadas.pop(index)
    return jsonify({"message": "Charada deletada com sucesso","charada":charada_deletada}), 200

if __name__ == "__main__":
    app.run(debug=True)