from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import openai

app = Flask(__name__)

# Connexion à Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

# Initialisation de l'API OpenAI
openai.api_key = 'key-value'


# Fonction pour interroger Elasticsearch
def search(query):
    res = es.search(index="indexBachelorarbeit", body={"query": {"match": {"content": query}}})
    hits = res['hits']['hits']
    return [hit['_source']['content'] for hit in hits]


# Fonction pour interagir avec ChatGPT
def chat_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].text.strip()


# Endpoint pour la recherche et la génération de réponse
@app.route('/api/search', methods=['POST'])
def search_and_generate_response():
    data = request.get_json()
    query = data['query']
    search_results = search(query)
    if search_results:
        response = chat_gpt(search_results[0])
        return jsonify({'response': response})
    else:
        return jsonify({'response': 'Aucun résultat trouvé'})


if __name__ == '__main__':
    app.run(debug=True)
