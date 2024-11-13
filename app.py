from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('home.html')

# Ruta para la página de contacto
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Ruta para la página de artículos
@app.route('/articles')
def articles():
    return render_template('articles.html')

# Ruta para la página de herramientas gratuitas
@app.route('/tools')
def tools():
    return render_template('tools.html')


if __name__ == '__main__':  
    app.run(host='0.0.0.0', debug=True)
