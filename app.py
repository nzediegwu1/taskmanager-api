from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world, this is Anaeze Nsoffor's todo app from flask"


if __name__ == "__main__":
    app.run("localhost", 3000)
