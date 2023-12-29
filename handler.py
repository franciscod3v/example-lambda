#Importar json y logger
import json
import logging
import uuid

logger = logging.getLogger() #Crear variable logger
logger.setLevel(logging.INFO) #Setear lvl a logger

#Hacer una pequeña validación de cabecera
API_PASSWORD = "clave_de_acceso"

def lambda_handler(event, context):
    headers = event.get("headers")
    print(f"headers: {headers}")
    api_key = headers.get("x-api-key")
    print(f"api_key: {api_key}")
    logger.info(f"El evento es : {event}")

    if api_key != API_PASSWORD:
        return {"statusCode": 401, "body": json.dumps("Acceso no autorizado")}
    
    #Todas estas variables las tomamos del request context del event
    http = event.get("requestContext").get("http")
    method = http.get("method")
    path = http.get("path")

    print(f"Este es el path: {path}")
    print(f"Este es el method: {method}")

    if method not in ["GET", "POST"]:
        return {"statusCode": 405, "body": json.dumps("Metodo no encontrado")}
    
    def manejar_get(path):
        print("Entro a Manejar get")
        if path == "/libreria":
            print("Entro a libreria")
            return getLibros()
        elif path == "/autores":
            print("Entro a autores")
            return getAutores()
        else:
            print("No entro a nada")
            return None
            
    
    def getLibros():

        libros = [
            {"id": 1, "name": "Ensayo sobre la ceguera", "autor": "Jose Saramago"},
            {"id": 2, "name": "Ensayo sobre la lucidez", "autor": "Jose Saramago"},
            {"id": 3, "name": "Padre rico, padre pobre", "autor": "Robert Kiyosaki"}
        ]
        logger.info(libros)
        return libros
    

    def getAutores():
        return [
            {"id": str(uuid.uuid4), "name": "Jose Saramago"},
            {"id": str(uuid.uuid4), "name": "Robert Kiyosaki"}
        ]
    
    if method == "GET":
        print("Entro al GET")
        response = manejar_get(path)
        print(f"El response es: {response}")
        return {"statusCode": 200, "body": json.dumps(response)}
    
    return {"statusCode": 500, "body": json.dumps("Error")} #Json.dumps() vuelve un objeto python a una cadena con formato JSON

    
