from flask import Flask

app = Flask('tilestore')

@app.route("/", methods=['GET'])
def home():
    return "This is the Home Page"

@app.route("/about")
def about():
    me = {
        "first": "Michael",
        "middle": "James",
        "last": "Costanza",
        "suffix": "Jr",
        "age": 26,
    }
    person = me["first"] + me["middle"] + me["last"] + me["suffix"] + str(me["age"])

    person = ""

    for e in me:
        person+= str(me[e]) + " "


    return person

app.run(debug=True)

