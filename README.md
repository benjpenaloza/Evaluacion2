# Evaluacion2
Repositorio de Evaluacion 2 Realizado por Marko Morales y Benjamin Peñaloza

# Calculadora de Rutas con GraphHopper

Este script en Python utiliza la API de [GraphHopper](https://www.graphhopper.com/) para calcular rutas entre dos ubicaciones geográficas. Permite al usuario ingresar un lugar de origen y uno de destino, elegir un perfil de vehículo (auto, bicicleta o a pie), y luego obtener instrucciones detalladas de la ruta, incluyendo distancia y tiempo estimado de viaje.

## Características

- **Geocodificación**: Convierte ubicaciones textuales a coordenadas geográficas usando la API de GraphHopper.
- **Cálculo de rutas**: Obtiene la ruta más rápida entre dos puntos usando la API de GraphHopper.
- **Perfiles de vehículo**: El usuario puede elegir entre varios perfiles de transporte: 
  - `car` (Auto)
  - `bike` (Bicicleta)
  - `foot` (A pie)
- **Narrativa de viaje**: Proporciona instrucciones paso a paso con distancias y tiempos estimados.

## Requisitos

- Python 3.x
- Librerías:
  - `requests` (Puedes instalarla con `pip install requests`)
- Clave API de GraphHopper (puedes obtenerla registrándote en [GraphHopper](https://www.graphhopper.com/))

## Uso

1. **Obtener una clave API**: Regístrate en [GraphHopper](https://www.graphhopper.com/) y obtén tu clave de API.
2. **Ejecutar el script**: Corre el archivo Python en tu terminal o IDE favorito.

   ```bash
   python nombre_del_archivo.py

