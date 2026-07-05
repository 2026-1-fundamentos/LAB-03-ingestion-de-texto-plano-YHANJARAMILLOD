"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import re
import pandas as pd




def pregunta_01():
    datos = []
    cluster_actual = None
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
        for linea in f:
            linea_limpia = linea.strip()
            if not linea_limpia or linea_limpia.startswith("---"):
                continue

              # 2. Intentar buscar el inicio de una fila real usando Regex
              # Busca: [Número] -> [Número] -> [Porcentaje] -> [El resto del texto]
            patron_inicio = re.match(
                r"^\s*(\d+)\s+(\d+)\s+(\d+,\d+\s*%)\s+(.*)", linea
            )
            if patron_inicio:
                # Si ya estábamos procesando un cluster anterior, lo guardamos
                if cluster_actual:
                    datos.append(cluster_actual)

                # Creamos el diccionario para el nuevo cluster
                cluster_actual = {
                    "cluster": int(patron_inicio.group(1)),
                    "cantidad_palabras": int(patron_inicio.group(2)),
                    "porcentaje": patron_inicio.group(3).strip(),
                    "principales_palabras_clave": patron_inicio.group(
                        4
                    ).strip(),
                }
            else:
                # 3. Si la línea NO empieza por números, es una continuación del texto de arriba
                if cluster_actual:
                    # Limpiamos los espacios extras gigantes que pueda tener en medio el texto
                    texto_continuacion = re.sub(r"\s+", " ", linea_limpia)
                    # Lo pegamos al cluster que estamos acumulando
                    cluster_actual["principales_palabras_clave"] += (
                        " " + texto_continuacion
                    )

        # Al salir del bucle, aseguramos guardar el último cluster procesado
        if cluster_actual:
            datos.append(cluster_actual)

    # 4. Convertimos la lista de datos limpios en un DataFrame de Pandas
    df = pd.DataFrame(datos)
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    # Limpieza final por si quedaron dobles espacios dentro del texto acumulado
    df["principales_palabras_clave"] = df[
        "principales_palabras_clave"
    ].str.replace(r"\s+", " ", regex=True)
    

    return df
    
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos. ===
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
