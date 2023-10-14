from flask import Flask, request, jsonify, render_template_string
import subprocess

app = Flask(_name_)

# HTML content and JavaScript logic
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Remote Terminal</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f0f0f0;
        }

        .container {
            max-width: 500px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            border-radius: 5px;
        }

        h1 {
            color: #333;
        }

        textarea {
            width: 100%;
            height: 200px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-bottom: 10px;
        }

        button {
            background-color: #007BFF;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        #output {
            margin-top: 10px;
            padding: 10px;
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to the Remote Terminal</h1>
        <textarea id="pythonCode" placeholder="Enter Python code here"></textarea>
        <button onclick="executePythonCode()">Execute</button>
        <div id="output"></div>
    </div>
    
    <script>
        function executePythonCode() {
            const pythonCode = document.getElementById("pythonCode").value;

            // Send the Python code to the Flask backend for execution
            fetch("/execute", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ code: pythonCode }),
            })
            .then((response) => response.json())
            .then((data) => {
                // Display the output in the 'output' div
                document.getElementById("output").innerText = data.output;
            })
            .catch((error) => {
                console.error("Error:", error);
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html_content)

@app.route("/execute", methods=["POST"])
def execute_python_code():
    try:
        data = request.get_json()
        python_code = data["code"]

        # Execute the Python code
        result = subprocess.check_output(["python3", "-c", python_code], stderr=subprocess.STDOUT, text=True)

        return jsonify({"output": result.strip()})
    except Exception as e:
        return jsonify({"error": str(e)})

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=8080)