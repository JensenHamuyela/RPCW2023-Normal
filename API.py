from flask import Flask, jsonify

app = Flask(__name__)

# lista de contratos
contracts = [
    {'id': 1, 'name': 'Contract A', 'institution': 'Institution X', 'year': 2022, 'course': 'Course A'},
    {'id': 2, 'name': 'Contract B', 'institution': 'Institution Y', 'year': 2021, 'course': 'Course B'},
    {'id': 3, 'name': 'Contract C', 'institution': 'Institution Z', 'year': 2022, 'course': 'Course C'}
]

# rota para retornar todos os contratos
@app.route('/contracts')
def get_contracts():
    return jsonify(contracts)

if __name__ == '__main__':
    app.run(port=15015, debug=True)


# rota para retornar o contrato com o ID correspondente
@app.route('/contracts/<int:contract_id>')
def get_contract(contract_id):
    for contract in contracts:
        if contract['id'] == contract_id:
            return jsonify(contract)
    return jsonify({'error': 'Contract not found'})

if __name__ == '__main__':
    app.run(port=15015, debug=True)


# rota para retornar a lista de contratos realizados no ano especificado
@app.route('http://localhost:15015')
def get_contracts_by_year():
    year = request.args.get('year')
    if year:
        year = int(year)
        filtered_contracts = [contract for contract in contracts if contract['year'] == year]
        return jsonify(filtered_contracts)
    return jsonify({'error': 'Year not specified'})

if __name__ == '__main__':
    app.run(port=15015, debug=True)


# rota para retornar a lista de contratos realizados pela instituição especificada
@app.route('http://localhost:15015')
def get_contracts_by_institution():
    institution = request.args.get('inst')
    if institution:
        filtered_contracts = [contract for contract in contracts if contract['institution'] == institution]
        return jsonify(filtered_contracts)
    return jsonify({'error': 'Institution not specified'})

if __name__ == '__main__':
    app.run(port=15015, debug=True)

# rota para retornar a lista de cursos dos contratados sem repetições
@app.route('http://localhost:15015')
def get_courses():
    courses_set = set(contract['course'] for contract in contracts)
    courses_list = list(courses_set)
    return jsonify(courses_list)


# rota para retornar a lista de instituições contratantes sem repetições
@app.route('http://localhost:15015')
def get_institutions():
    institutions_set = set(contract['institution'] for contract in contracts)
    institutions_list = list(institutions_set)
    return jsonify(institutions_list)

if __name__ == '__main__':
    app.run(port=15015, debug=True)



next_id = 5  # próximo id disponível para um novo contrato

# rota para adicionar um novo contrato
@app.route('http://localhost:15015', methods=['POST'])
def add_contract():
    global next_id  # permite alterar a variável global next_id
    contract = request.json  # obtém o contrato enviado no corpo da requisição em formato JSON
    contract['id'] = next_id  # define o id do novo contrato
    contracts.append(contract)  # adiciona o novo contrato na lista
    next_id += 1  # atualiza o próximo id disponível
    return jsonify(contract), 201  # retorna o novo contrato em formato JSON com código 201 (Created)

# rota para remover um contrato
@app.route('http://localhost:15015/<int:id>', methods=['DELETE'])
def delete_contract(id):
    global contracts
    before_len = len(contracts)  # tamanho da lista de contratos antes da remoção
    contracts = [c for c in contracts if c['id'] != id]  # remove o contrato com o id especificado
    if len(contracts) == before_len:  # se nenhum contrato foi removido, retorna código 404 (Not Found)
        abort(404)
    return '', 204  # retorna resposta vazia com código 204 (No Content)

if __name__ == '__main__':
    app.run(port=15015, debug=True)
