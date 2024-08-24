from flask import Flask, render_template, request, redirect, url_for
from .main import initialize_model, initialize_chromadb, initialize_prompt_template, process_user_input

# Initialize the Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Initialize components
model = initialize_model()
collection = initialize_chromadb()
prompt = initialize_prompt_template()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        
        # Process the user input and generate a response
        response = process_user_input(user_input, model, prompt, collection)

        # Redirect to the same page with the response data as a GET request
        return redirect(url_for('index', user_input=user_input, response=response))

    # On GET request, retrieve query parameters
    user_input = request.args.get('user_input')
    response = request.args.get('response')

    return render_template('index.html', user_input=user_input, response=response)

if __name__ == "__main__":
    app.run
