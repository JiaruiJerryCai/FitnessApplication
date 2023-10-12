from flask import Flask

app = Flask(__name__)

@app.route("/test")
def test_method():
    return 'Hello'

@app.route("/")
def HomePage():
    return 'Home Page'

@app.route("/Greeting/<name>")
def NameRoute(name):
    return 'Hello ' + name

@app.route("/Increment")
def NumberRoute():
    number = 0 
    number += 1
    return str(number)

@app.route('/videoresult')
def videoResultRoute():

    analyzedVideo = runAnalysis("pushup", "videoFileLocation")
    return analyzedVideo

if __name__ == '__main__':
    app.run(host='0.0.0.0')