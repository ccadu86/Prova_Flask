import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import random

csv_file_path = 'arquivo.csv'

if not os.path.exists(csv_file_path):
    default_columns = ["ID", "Nome", "Idade", "Cidade"]
    pd.DataFrame(columns=default_columns).to_csv(csv_file_path, index=False)

if os.path.getsize(csv_file_path) > 0:
    df = pd.read_csv(csv_file_path)
else:
    df = pd.DataFrame(columns=["ID", "Nome", "Idade", "Cidade"])

app = Flask(__name__)
CORS(app)

def generate_unique_id():
    return str(random.randint(1000, 9999))

@app.route('/read', methods=['GET'])
def read():
    data = df.to_dict(orient='records')
    return jsonify(data), 200

@app.route('/create', methods=['POST'])
def create():
    global df
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados vazios!'}), 400

    data['ID'] = generate_unique_id()
    new_data = pd.DataFrame([data], columns=["ID", "Nome", "Idade", "Cidade"])

    if not set(new_data.columns) == set(df.columns):
        return jsonify({'error': 'Dados com formato incorreto!'}), 400

    while data['ID'] in df['ID'].values:
        data['ID'] = generate_unique_id()

    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(csv_file_path, index=False)
    return jsonify({'message': 'Registro criado com sucesso!', 'ID': data['ID']}), 201

@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    global df
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados vazios!'}), 400

    try:
        df['ID'] = df['ID'].astype(str)
        id = str(id)

        if id not in df['ID'].values:
            return jsonify({'error': 'ID não encontrado!'}), 404

        df.loc[df['ID'] == id, ["Nome", "Idade", "Cidade"]] = data["Nome"], data["Idade"], data["Cidade"]
        df.to_csv(csv_file_path, index=False)
        return jsonify({'message': 'Registro atualizado com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': 'Erro ao atualizar registro!'}), 500



@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    global df
    try:
        df['ID'] = df['ID'].astype(str)
        id = str(id)        
        df = df[df['ID'] != id].reset_index(drop=True)        
        df.to_csv(csv_file_path, index=False)
        return jsonify({'message': 'Registro deletado com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao deletar registro!'}), 500

if __name__ == '__main__':
    app.run(debug=True)
