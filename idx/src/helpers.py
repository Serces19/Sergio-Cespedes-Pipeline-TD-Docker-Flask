import csv
import datetime
import pytz
import requests
import urllib
import uuid
import json
from pprint import pprint

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(
            url,
            cookies={"session": str(uuid.uuid4())},
            headers={"Accept": "*/*", "User-Agent": "python-requests"},
        )
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        price = round(float(quotes[-1]["Adj Close"]), 2)
        return {"price": price, "symbol": symbol}
    except (KeyError, IndexError, requests.RequestException, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"





######################################################################


def get_shots_pendientes():
    api_url = 'https://4ntkrcxysh.execute-api.us-east-1.amazonaws.com/scanTable'

    try:
        response = requests.post(api_url)
        response = response.text
        print('Shots cargados correctamente')

    except Exception as e:
        print(f"Error inesperado: {e}")
        response = None

    shots_pendientes = json.loads(response)
    print('Se encontraron esta cantidad de shots:', len(shots_pendientes))
    return(shots_pendientes)



def updateData(shot:str, nuevos_datos:dict):
    api_url = 'https://4ntkrcxysh.execute-api.us-east-1.amazonaws.com/scope_updateData'
    shot = shot.lower()

    data = {
        'shot': shot,
        'tabla': 'atom_shots_DB',
        "nuevos_datos": nuevos_datos,
    }
    print('Los datos a mandar a la tabla shots son:', data)

    try:
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            print('Datos correctamente actualizados')
            
        else:
            print(f'Error: La petición no fue exitosa. Código de estado: {response.status_code}') 

    except Exception as e:
        print('No se pudo agregar ruta a la tabla shots', e)

