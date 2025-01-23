from flask import Flask, request, jsonify
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.json.get("code")
    if not code:
        return jsonify({"error": "No code provided"}), 400

    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parse_tree = parser.parse()
        interpreter = Interpreter(parse_tree)
        interpreter.execute()
        return jsonify({"parse_tree": parse_tree}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
