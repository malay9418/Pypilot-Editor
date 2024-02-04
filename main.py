from flask import Flask, render_template, request, jsonify, send_from_directory
from freeGPT import Client
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/assets/<filename>")
def assets(filename):
    return send_from_directory("assets", filename)

@app.route("/completion", methods=["POST"])
def completion():
    data = request.get_json()
    print("######################### REQUEST ##########################\n", data)
    code = "\n".join(data["code"])
    prompt = f"""You act as a code autocompletion for python. You are provided some lines of code before cursor position in editor and you response next lines of codes, that is inserted at the end of input codes later.
Note: You do not include input codes in your response and takes care of indentation and newlines. You always response within ``` back ticks and in case you can not response just response with three dots ...
Example:
input:```# hello world```
response:```
print("Hello world")```
input:```from flask import Flask
app =```
response:``` Flask(__name__)

@app.route("/")
def index():
    return "Hello world"

if __name__=="__main__":
    app.run()```
Current task:
input:```${code}```
response:"""
    resp = Client.create_completion("gpt3", prompt)
    print("######################### RESPONSE ##########################\n", resp)
    pattern = r"```(.*?)```"
    match = re.search(pattern, resp, re.DOTALL)

    if match:
        completion_code = match.group(1)
    else:
        print("No match found")
        completion_code = "..."

    return jsonify({"completion": completion_code, "time": data["time"]})

if __name__ == "__main__":
    app.run(debug=True)
