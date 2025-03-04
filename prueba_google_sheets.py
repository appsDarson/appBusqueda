import gspread
from google.oauth2.service_account import Credentials

# Configura las credenciales
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

# Abre la hoja de cálculo
sheet = client.open("Copia de Mapa Picking").sheet1

# Lee todos los datos
datos = sheet.get_all_records()
print(datos)