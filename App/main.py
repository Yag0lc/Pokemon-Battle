from flask import Flask, json, jsonify
from flask import current_app

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)


with open("data/pokemon.json", encoding="utf-8") as f:
    app.config["DATA"] = json.load(f)



from flask import current_app

# Carga de datos del fichero
...

@app.route("/")
def home():
    return jsonify(current_app.config["data"])