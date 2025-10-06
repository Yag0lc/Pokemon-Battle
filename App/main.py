from flask import Flask, json, render_template

app = Flask(__name__)

# Carga de datos del fichero JSON
with open("data/pokemon.json", "r", encoding="utf-8") as f:
    app.config["DATA"] = json.load(f)


@app.route('/')
def home():
    return render_template('Home.html')


if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)