from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

@app.post("/execute")
def execute():
    data = request.json
    filename = data["filename"]
    input_filename = data["input_filename"]
    output = subprocess.run(["java", filename], input=input_filename)
    print(output.stdout)
    print(output.stderr)
    return jsonify(1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)