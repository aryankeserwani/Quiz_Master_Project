from flask import Flask

def createApp():
    app = Flask(__name__)
    return app
app=createApp()

@app.get("/")
def hello():
    return '<h1>Hello World</h1>'

if __name__ == "__main__":
    app.run(debug=True)