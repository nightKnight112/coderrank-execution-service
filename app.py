from flask import Flask, jsonify, request
import subprocess
import logging
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Logging configuration
logging.basicConfig(format="{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S")

@app.post("/execute")
def execute():
    logging.error(f"{request.method} - {request.url} - {request.json}")
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
        logging.error(f"{code}, {language_name}, {user_uuid}, {input}")

        os.makedirs(os.path.dirname(f"/home/codes/{user_uuid}/"), exist_ok=True)
        with open(f"/home/codes/{user_uuid}/input.txt", "w") as f:
            logging.error(f"Writing input to /home/codes/{user_uuid}/input.txt")
            f.write(input)

        if language_name == "Java":
            filename = f"/home/codes/{user_uuid}/Solution.java"
            with open(filename, "w") as f:
                logging.error(f"Writing java code to /home/codes/{user_uuid}/Solution.java")
                f.write(code)
        elif language_name == "Python":
            filename = f"/home/codes/{user_uuid}/solution.py"
            with open(filename, "w") as f:
                logging.error(f"Writing python code to /home/codes/{user_uuid}/solution.py")
                f.write(code)
        
        with open(f"/home/codes/{user_uuid}/input.txt", "rb") as f:
            file = f.read()

        if language_name == "Java":
            try:
                output = subprocess.run(["java", filename], input=file, capture_output=True)
                stdout = output.stdout.decode().strip()
                stderr = output.stderr.decode().strip()
            except Exception as e:
                logging.error(e)
                logging.error("Error in running java code")
        else:
            try:
                output = subprocess.run(["python3", filename], input=file, capture_output=True)
                stdout = output.stdout.decode().strip()
                stderr = output.stderr.decode().strip()
            except Exception as e:
                logging.error(e)
                logging.error("Error in running python code")

        logging.error(f"stdout: {stdout}")
        logging.error(f"stderr: {stderr}")
        logging.error(f"output: {stdout if len(stderr) < len(stdout) else stderr}")

        if len(stderr) > len(stdout):
            return jsonify({"output": stderr})
        else:
            return jsonify({"output": stdout})
        
    except Exception as e:
        logging.error(e)
        return jsonify({"output": "something went wrong"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)