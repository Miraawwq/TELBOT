from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/career')
def career():
    return render_template('career.html')

@app.route('/contact')
def career():
    return render_template('contact.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443)
