import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import urllib3

# Desactivamos las advertencias de SSL porque la página del BCV a veces tiene certificados vencidos
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def actualizar_tasa():
    url = "https://www.bcv.org.ve/"
    try:
        # Extraemos la página
        response = requests.get(url, verify=False, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscamos los valores del Dólar y Euro
        usd_text = soup.find(id="dolar").find('strong').text.strip().replace(',', '.')
        eur_text = soup.find(id="euro").find('strong').text.strip().replace(',', '.')
        
        usd_val = float(usd_text)
        eur_val = float(eur_text)
    except Exception as e:
        print(f"Error extrayendo datos del BCV: {e}")
        return

    # Obtenemos la fecha y el año actual
    ahora = datetime.now()
    fecha_actual = ahora.strftime("%d/%m/%Y")
    anio_actual = ahora.strftime("%Y")

    nuevo_dato = {"d": fecha_actual, "u": usd_val, "e": eur_val}

    # Cargamos el archivo JSON existente
    try:
        with open('datos_bcv.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("El archivo JSON no existe. Creando uno nuevo.")
        data = {}
    except Exception as e:
        print(f"Error abriendo el JSON: {e}")
        return

    # Si el año actual no existe en el JSON, lo creamos
    if anio_actual not in data:
        data[anio_actual] = []

    # Verificamos que el dato de hoy no esté duplicado
    if len(data[anio_actual]) == 0 or data[anio_actual][0]['d'] != fecha_actual:
        data[anio_actual].insert(0, nuevo_dato) # Lo insertamos de primero
        
        # Guardamos los cambios en el archivo
        with open('datos_bcv.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Tasa actualizada exitosamente! USD: {usd_val} | EUR: {eur_val}")
    else:
        print(f"La tasa del {fecha_actual} ya estaba registrada. No se hicieron cambios.")

if __name__ == "__main__":
    actualizar_tasa()
