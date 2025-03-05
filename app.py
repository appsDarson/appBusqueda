import os
import json
from flask import Flask, request, jsonify, render_template
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Cargar credenciales desde variables de entorno
creds_json = os.getenv('GOOGLE_CREDENTIALS')  # Obtener la variable de entorno
if not creds_json:
    raise ValueError("La variable de entorno GOOGLE_CREDENTIALS no está configurada.")

creds_dict = json.loads(creds_json)  # Convertir el JSON de texto a un diccionario
creds = Credentials.from_service_account_info(creds_dict, scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)

# Abre la hoja de cálculo
    sheet = client.open("Copia de Mapa Picking").sheet1
except Exception as e:
    print(f"Error al cargar las credenciales o abrir la hoja de cálculo: {e}")
    sheet = None  # Si hay un error, sheet será None

# Ruta para buscar un modelo
@app.route('/buscar', methods=['GET'])
def buscar():
    try:
        modelo = request.args.get('modelo', '').lower()  # Convertir a minúsculas
        if not modelo:
            return jsonify({"error": "Por favor, proporciona un modelo para buscar."}), 400
        
        if not sheet:
            return jsonify({"error": "Error al acceder a la hoja de cálculo."}), 500
        
        datos = sheet.get_all_records()
        resultado = [fila for fila in datos if modelo in fila['MODELO'].lower()]
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener todos los datos
@app.route('/tabla', methods=['GET'])
def tabla():
    try:
        if not sheet:
            return jsonify({"error": "Error al acceder a la hoja de cálculo."}), 500
        
        datos = sheet.get_all_records()
        return jsonify(datos)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para la página principal (búsqueda)
@app.route('/')
def index():
    return render_template('buscar.html')

# Ruta para la página de la tabla completa
@app.route('/tabla_completa')
def tabla_completa():
    return render_template('tabla.html')

# Configurar el puerto para Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usar el puerto de Render o 5000 por defecto
    app.run(host='0.0.0.0', port=port, debug=False)  # Desactivar debug en producción
