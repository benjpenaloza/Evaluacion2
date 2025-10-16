import requests
import urllib.parse

# 1. Definición de URLs y Clave
route_url = "https://graphhopper.com/api/1/route?"
key = "a0297f7b-fdbd-423b-9417-f65eeab3bc71"  

def geocoding(location, key):
    """
    Función para geocodificar una ubicación (convertir nombre a coordenadas).
    """
    # Manejo de la opción de salir
    if location.lower() in ("s", "salir"):
        return "salir", "salir", "salir", "salir"

    while location == "":
        location = input("Por favor, ingrese la ubicación nuevamente: ")

    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        # Construcción del nombre completo de la ubicación
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")

        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif state:
            new_loc = f"{name}, {state}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name

        print(f"✔️ Éxito en la Geocodificación para: {new_loc} (Tipo: {value})")
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status == 401:
            print("❌ Error API de Geocodificación - Estado: 401. Mensaje: Credenciales incorrectas.")
            print("Por favor, reemplace 'key' con una clave válida de GraphHopper.")
        elif json_status != 200:
            print(f"❌ Error API de Geocodificación - Estado: {json_status}. Mensaje: {json_data.get('message', 'No hay mensaje de error.')}")
        else:
            print(f"❌ Ubicación no encontrada para: {location}")

    return json_status, lat, lng, new_loc

def get_and_print_route(orig_lat, orig_lng, dest_lat, dest_lng, vehicle, key):
    """
    Función para calcular y mostrar la ruta, incluyendo la narrativa del viaje.
    """
    
    # SOLUCIÓN AL ERROR 400: Incluir las coordenadas directamente en 'params'
    # para que urllib.parse.urlencode las formateé correctamente como point=lat1,lng1&point=lat2,lng2
    params = {
        "key": key,
        "vehicle": vehicle,
        "points_encoded": "false",  
        "locale": "es",            
        # Formato esperado: "lat,lng"
        "point": [f"{orig_lat},{orig_lng}", f"{dest_lat},{dest_lng}"] 
    }
    
    # Construcción limpia de la URL. doseq=True es vital para que maneje múltiples 'point'.
    url = route_url + urllib.parse.urlencode(params, doseq=True)
    
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200:
        route = json_data["paths"][0]
        
        # 2. Asegurar dos decimales para valores numéricos
        distance_km = route["distance"] / 1000  # Metros a Kilómetros
        time_ms = route["time"]
        
        # Convertir tiempo de milisegundos a horas/minutos/segundos
        total_seconds = time_ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        time_str = ""
        if hours > 0:
            time_str += f"{hours}h "
        if minutes > 0:
            time_str += f"{minutes}m "
        time_str += f"{seconds}s"
        
        # === IMPRESIÓN DE RESULTADOS ===
        print("\n==================================================")
        print("🗺️  RUTA CALCULADA EXITOSAMENTE")
        print("==================================================")
        print(f"  Perfil de Vehículo: **{vehicle.upper()}**")
        print(f"  Distancia Total: **{distance_km:.2f} km**") # Dos decimales
        print(f"  Tiempo Estimado: **{time_str.strip()}**")
        print("--------------------------------------------------")
        print("  **INSTRUCCIONES DE VIAJE (NARRATIVA)**")
        print("--------------------------------------------------")

        # Imprimir la narrativa del viaje en español
        instructions = route["instructions"]
        for i, instruction in enumerate(instructions, 1):
            text = instruction["text"]
            distance_m = instruction["distance"]
            
            # Distancia de la instrucción con dos decimales
            distance_str = f"{distance_m:.2f} metros" if distance_m < 1000 else f"{(distance_m / 1000):.2f} km"

            print(f"  {i}. {text} (Recorrer: {distance_str})")
            
        print("==================================================")
    else:
        print(f"❌ Error al calcular la ruta - Estado: {json_status}. Mensaje: {json_data.get('message', 'No se pudo encontrar una ruta entre estas ubicaciones.')}")


# === BUCLE PRINCIPAL DEL PROGRAMA ===
while True:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++")
    print("🚗 PERFILES DE VEHÍCULOS DISPONIBLES:")
    print("++++++++++++++++++++++++++++++++++++++++++++++")
    print("car (Auto), bike (Bicicleta), foot (A pie)")
    print("Escriba 's' o 'salir' en cualquier momento para terminar.")

    profile = ["car", "bike", "foot"]
    vehicle = input("👉 Ingrese un perfil de vehículo de la lista: ").lower() 

    # Manejo de la opción de salir
    if vehicle in ("s", "salir"):
        print("Saliendo del programa. ¡Hasta pronto!")
        break
    elif vehicle in profile:
        vehicle = vehicle
    else:
        vehicle = "car"
        print("⚠️ Perfil no válido. Usando el perfil por defecto: **car (Auto)**.")

    # --- Solicitud de Ubicación de Origen ---
    loc1 = input("📍 Ubicación de Origen (Ej: Plaza de Armas, Santiago): ") 
    orig = geocoding(loc1, key)
    
    # Manejo de la opción de salir
    if orig[0] == "salir":
        print("Saliendo del programa. ¡Hasta pronto!")
        break
    
    if orig[1] == "null":
        print("No se pudo geocodificar la ubicación de origen. Volviendo a empezar.")
        continue

    # --- Solicitud de Ubicación de Destino ---
    loc2 = input("🎯 Ubicación de Destino (Ej: Cerro Alegre, Valparaíso): ") 
    dest = geocoding(loc2, key)
    
    # Manejo de la opción de salir
    if dest[0] == "salir":
        print("Saliendo del programa. ¡Hasta pronto!")
        break
    
    if dest[1] == "null":
        print("No se pudo geocodificar la ubicación de destino. Volviendo a empezar.")
        continue

    # --- Cálculo de la Ruta ---
    
    # Extraer Latitud y Longitud
    orig_lat, orig_lng = orig[1], orig[2]
    dest_lat, dest_lng = dest[1], dest[2]
    
    print(f"\nOrigen: **{orig[3]}** | Destino: **{dest[3]}**")

    # Llamar a la función para obtener y mostrar la ruta
    get_and_print_route(orig_lat, orig_lng, dest_lat, dest_lng, vehicle, key)