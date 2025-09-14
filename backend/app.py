# 1. Import the Flask class from the flask library
from flask import Flask

# 2. Create an instance of the Flask class
# __name__ is a special Python variable that gets the name of the current module.
# Flask uses this to know where to look for resources.
app = Flask(__name__)

# 3. Define a "route" and a "view function"
# The @app.route('/') decorator tells Flask what URL should trigger our function.
# '/' is the root URL, or the homepage.
@app.route('/')
def hello_world():
    # This function is the "view function". It returns the response for the URL.
    return 'Hello, World!'

# 4. Run the application
# The if __name__ == '__main__': block ensures this code only runs
# when you execute the script directly (not when it's imported).
if __name__ == '__main__':
    # app.run(debug=True) starts the development server.
    # debug=True is very helpful as it automatically reloads the server when you save changes.
    app.run(debug=True)