from flask import Flask, jsonify, request
import subprocess
import logging
import os

app = Flask(__name__)

# Logging configuration
logging.basicConfig(format="{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S")

@app.post("/execute")
def execute():
    logging.debug(f"{request.method} - {request.url} - {request.json}")
    try:
        data = request.json
        code = data["code"]
        language_name = data["language_name"]
        user_uuid = data["user_uuid"]
        input = data["input"]
        file = ""
        stdout = ""
        stderr = ""

        filename = ""

        os.makedirs(os.path.dirname(f"/home/codes/{user_uuid}/"), exist_ok=True)
        with open(f"/home/codes/{user_uuid}/input.txt", "w") as f:
            f.write(input)

        if language_name == "Java":
            filename = f"/home/codes/{user_uuid}/Solution.java"
            with open(filename, "w") as f:
                f.write(code)
        elif language_name == "Python":
            filename = f"/home/codes/{user_uuid}/solution.py"
            with open(filename, "w") as f:
                f.write(code)
        
        with open(f"/home/codes/{user_uuid}/input.txt", "rb") as f:
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
    app.run(host="0.0.0.0", port=5001, debug=True)