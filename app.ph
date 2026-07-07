from flask import Flask app = Flask(__name__) 
@app.route("/") def home():
    return "<h1>School Management 
    System</h1><p>System is running 
    successfully.</p>"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
