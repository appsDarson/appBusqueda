import os
import json
from flask import Flask, request, jsonify, render_template
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Cargar credenciales desde variables de entorno
creds_json = os.getenv('GOOGLE_CREDENTIALS')  # Obtener la variable de entorno
creds_dict = json.loads(creds_json)  # Convertir el JSON de texto a un diccionario
creds = Credentials.from_service_account_info(creds_dict, scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)

# Abre la hoja de cálculo
sheet = client.open("Copia de Mapa Picking").sheet1

# Ruta para buscar un modelo
@app.route('/buscar', methods=['GET'])
def buscar():
    modelo = request.args.get('modelo')
    datos = sheet.get_all_records()
    resultado = [fila for fila in datos if fila['MODELO'] == modelo]
    return jsonify(resultado)

# Ruta para obtener todos los datos
@app.route('/tabla', methods=['GET'])
def tabla():
    datos = sheet.get_all_records()
    return jsonify(datos)

# Ruta para la página principal (búsqueda)
@app.route('/')
def index():
    return render_template('buscar.html')

# Ruta para la página de la tabla completa
@app.route('/tabla_completa')
def tabla_completa():
    return render_template('tabla.html')
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usar el puerto de Render o 5000 por defecto
    app.run(host='0.0.0.0', port=port)
