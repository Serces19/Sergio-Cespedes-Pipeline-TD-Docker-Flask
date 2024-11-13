import os
import jwt
import boto3
from flask import Flask, flash, redirect, render_template, request, session, send_file, get_flashed_messages, url_for, jsonify
from flask_session import Session
from botocore.exceptions import ClientError

from helpers import apology, login_required, lookup, usd, get_shots_pendientes

##################################################################################################################

# Configuración de AWS Cognito
COGNITO_USER_POOL_ID = 'us-east-1_EYkOR7y0k'
COGNITO_CLIENT_ID = '6k1p690lgkki7ve53hh1eedv2j'
COGNITO_REGION = 'us-east-1'
cognito_client = boto3.client('cognito-idp', region_name=COGNITO_REGION)


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def home():
    # Recupera el mensaje flash de la URL
    message = request.args.get("message")
    print('user id es:', session.get('user_id'))
    
    # Renderiza la plantilla HTML y pasa los mensajes flash a la plantilla
    return render_template("index.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            print('Apology')
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
            
        # Obtener el nombre de usuario y la contraseña del formulario
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password)

        if username == 'sergio' and password == 'sergio':
            session['user_id'] = username
            # Dentro de la función login después de autenticar al usuario correctamente
            flash("Usuario autenticado exitosamente", "success")
            return redirect(url_for("home", message="success"))

        else:
            flash('Usuario o contraseña incorrectos')
            return render_template('login.html', message="error")

        # try:
            # # Intenta autenticar al usuario con Cognito
            # response = cognito_client.initiate_auth(
            #     ClientId=COGNITO_CLIENT_ID,
            #     AuthFlow='USER_PASSWORD_AUTH',
            #     AuthParameters={
            #         'USERNAME': username,
            #         'PASSWORD': password
            #     }
            # )
            
            # # Suponiendo que response es la respuesta exitosa de la autenticación
            # id_token = response['AuthenticationResult']['IdToken']
            # decoded_token = jwt.decode(id_token, algorithms=["RS256"], verify=False)  # Decodifica el token de identificación sin verificar la firma (por simplicidad)

            # # Obtén el identificador único del usuario del token decodificado
            # user_id = decoded_token['sub']

            # Almacena el identificador único del usuario en la sesión de Flask


        # except ClientError as e:
        #     # Si ocurre un error durante la autenticación, muestra un mensaje de error
        #     print(e)
        #     error = 'Usuario o contraseña incorrectos'
        #     return render_template('login.html')

    if request.method == "GET":
        return render_template('login.html')


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/views")
def views():
    """See the table views"""
    shots = get_shots_pendientes()
    return render_template('views.html', shots=shots)


@app.route("/test")
def test():
    """See the table views"""
    shots = get_shots_pendientes()
    return render_template('test.html', shots=shots)



@app.route("/shots")
def shots():
    session['user_id'] = 'sergio'
    if session.get('user_id'):
        shots = get_shots_pendientes()
        return render_template('shots.html', shots=shots)
    else:
        return redirect("/")


def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()

