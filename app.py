from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

@app.post("/execute")
def execute():
    try:
        data = request.json
        filename = data["filename"]
        input_filename = data["input_filename"]
        file = ""

        print(filename, input_filename)
        with open(input_filename, "rb") as f:
            file = f.read()

        output = subprocess.run(["java", filename], input=file, capture_output=True)
        stdout = output.stdout.decode().strip()
        stderr = output.stderr.decode().strip()

        if len(stderr) > len(stdout):
            return jsonify({"output": stderr})
        else:
            return jsonify({"output": stdout})
        
    except Exception as e:
        print(e)
        return jsonify({"output": "something went wrong"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)