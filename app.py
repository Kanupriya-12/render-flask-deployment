from flask import Flask

app = Flask(__name__)

@app.route("/",methods=['GET'])
def home():
    return "<h1>Kanupriya's Flask App</h1>"

@app.route('/get_name', methods=['GET'])
def get_name():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Missing 'name' parameter"}), 400
    
    return f"<h1>{name}'s Flask App</h1>"

if __name__== "__main__":
    app.run()