from flask import Flask  # Import the Flask class
app = Flask(__name__)    # Create an instance of the class for our use
app.secret_key = 'secret_key' 

if __name__ == "webapp":
    app.debug = True
    app.run()