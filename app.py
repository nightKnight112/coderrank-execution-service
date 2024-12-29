from flask import Flask, jsonify, request
import subprocess
import logging

app = Flask(__name__)

# Logging configuration
logging.basicConfig(format="{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S")

@app.post("/execute")
def execute():
    try:
        data = request.json
        filename = data["filename"]
        input_filename = data["input_filename"]
        language_name = data["language_name"]
        file = ""
        stdout = ""
        stderr = ""
        
        with open(input_filename, "rb") as f:
            file = f.read()

        if language_name == "Java":
            output = subprocess.run(["java", filename], input=file, capture_output=True)
            stdout = output.stdout.decode().strip()
            stderr = output.stderr.decode().strip()
        else:
            output = subprocess.run(["python3", filename], input=file, capture_output=True)
            stdout = output.stdout.decode().strip()
            stderr = output.stderr.decode().strip()

        if len(stderr) > len(stdout):
            return jsonify({"output": stderr})
        else:
            return jsonify({"output": stdout})
        
    except Exception as e:
        logging.error(e)
        return jsonify({"output": "something went wrong"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
