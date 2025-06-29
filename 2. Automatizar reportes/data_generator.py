import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os


def generate_realistic_epp_reports(
    num_reports=50, output_filename="reportes_averias_puerto.xlsx"
):
    """
    Genera un archivo XLSX con reportes de averías de equipos de puerto realistas,
    incluyendo errores de tipeo y descripciones detalladas.

    Args:
        num_reports (int): Número de reportes a generar.
        output_filename (str): Nombre del archivo de salida XLSX.
    """

    # --- Listas de datos realistas ---
    equipos = [
        "Grúa Portainer QC1",
        "Grúa Portainer QC2",
        "Grúa RTG #3",
        "Grúa RTG #4",
        "Reach Stacker RS-A",
        "Reach Stacker RS-B",
        "Carretilla Elevadora #12",
        "Tractor de Terminal TT-5",
        "Generador Principal G1",
        "Compresor de Aire C2",
        "Bomba de Agua BW-A",
        "Sistema Eléctrico Muelle 3",
        "Cinta Transportadora L5",
        "Gate Automático Entrada Norte",
        "Báscula Camiones Sur",
    ]

    sistemas_afectados = [
        "Hidráulico",
        "Eléctrico",
        "Mecánico",
        "Electrónico",
        "Neumático",
        "Control de Motores",
        "Transmisión",
        "Combustible",
        "Frenos",
        "Estructura",
    ]

    buques = [
        "MSC Mediterranean",
        "Maersk Line",
        "CMA CGM",
        "Evergreen Marine",
        "COSCO Shipping",
        "ONE (Ocean Network Express)",
        "Hapag-Lloyd",
        "Yang Ming Marine Transport Corp.",
        "ZIM Integrated Shipping Services",
        "PIL (Pacific International Lines)",
    ]

    novedades_templates = [
        "Falla en el {sistema} del {equipo}. El operador reporta que se detuvo bruscamente. Posible problema en la {parte_especifica}.",
        "Problema {tipo_falla} en {equipo}. Se escuchó un ruido extraño y dejó de responder. Necesita revisión urgente. Demora aprox. de {horas_demora} horas.",
        "El {equipo} presenta un funcionamiento {irregular}. Se siente un {sintoma}. Posiblemente {causa_potencial}. Contactar a mantenimiento.",
        "Parada inesperada del {equipo} debido a {problema_general}. La alarma {alarma} se activó. Intentamos reiniciar pero sin éxito.",
        "Revisión de {equipo} por vibración excesiva en {componente}. El {operador} notó la situación durante su {turno_trabajo}.",
        "Se detectó una fuga en el sistema {sistema_afectado} del {equipo}. La {zona_fuga} está húmeda. Se procedió a {accion_tomada}. Pendiente de reparación mayor.",
        "Mantenimiento correctivo del {equipo}. El {componente} requiere reemplazo. Tuvimos que esperar por la pieza, lo que generó un retraso adicional de {horas_adicionales} horas.",
        "El {equipo} no enciende. Revisamos la {parte_electrica}, pero no encontramos nada obvio. Necesitamos un técnico eléctrico. Buque {buque_nombre} esperando.",
        "Informe de operador: 'El cable de la {parte_grua} de la {equipo} se deshilachó un poco, no me dio confianza seguir operando. Parece menor pero prefiero avisar. El buque es el {buque_nombre} y está en el muelle 2. Se detuvo a las 10:15 am'.",
        "Problema menor con la {parte_carretilla} de la {equipo}. A veces no responde bien. No es urgente pero para que lo miren en el próximo mantenimiento. Buque {buque_nombre} está a 50 metros.",
        "Ruido fuerte en el {equipo} (generador) del muelle 4. Vibra mucho. Posible {tipo_falla_mecanica}. Lo apagué por seguridad. El buque {buque_nombre} recién llegó.",
        "El sistema de {sistema_afectado} en la {equipo} está fallando intermitentemente. Los indicadores de presión no son estables. Operación comprometida. Necesita ser reparado urgentemente. La falla ocurrió alrededor de las 3:40 de la mañana.",
        "Se registró una paralización del {equipo} por una avería en su {componente}. La máquina estuvo fuera de servicio por aproximadamente 4 horas y 20 minutos mientras se esperaba al personal de mantenimiento. Esto retrasó la descarga del {buque_nombre}.",
    ]

    # Palabras para inyectar errores de tipeo
    letras_comunes = "aeioulnrst"
    errores_comunes = {
        "s": "ss",
        "es": "ess",
        "a": "aa",
        "o": "oo",
        "e": "ee",
        "c": "k",
        "q": "k",
        "v": "b",
        "z": "s",
        "n": "ñ",
        "m": "n",
    }

    def inyectar_error(text, error_rate=0.05):
        words = text.split()
        for i, word in enumerate(words):
            if random.random() < error_rate and len(word) > 3:
                # Elige un tipo de error
                error_type = random.choice(["typo", "dupe_char", "swap_char"])

                if error_type == "typo":
                    # Inyectar una letra incorrecta
                    idx = random.randint(0, len(word) - 1)
                    words[i] = (
                        word[:idx] + random.choice(letras_comunes) + word[idx + 1 :]
                    )
                elif error_type == "dupe_char":
                    # Duplicar una letra común
                    char_to_dupe = random.choice(
                        [c for c in word if c in letras_comunes]
                    )
                    if char_to_dupe:
                        words[i] = word.replace(char_to_dupe, char_to_dupe * 2, 1)
                elif error_type == "swap_char" and len(word) > 1:
                    # Intercambiar dos caracteres adyacentes
                    idx = random.randint(0, len(word) - 2)
                    char_list = list(word)
                    char_list[idx], char_list[idx + 1] = (
                        char_list[idx + 1],
                        char_list[idx],
                    )
                    words[i] = "".join(char_list)

                # Aplicar errores de ortografía comunes
                for common_error, replacement in errores_comunes.items():
                    if common_error in words[i]:
                        if (
                            random.random() < 0.3
                        ):  # 30% de probabilidad de aplicar el error específico
                            words[i] = words[i].replace(common_error, replacement)
        return " ".join(words)

    data = []
    start_date = datetime(2024, 1, 1, 8, 0, 0)

    for i in range(num_reports):
        equipo = random.choice(equipos)
        sistema_afectado = random.choice(sistemas_afectados)
        buque = random.choice(buques)

        # Generar tiempos de falla realistas
        # La duración de la falla varía entre 0.5 y 10 horas
        duracion_minutos = random.randint(30, 600)

        # Iniciar fallas en días recientes para que el dataset sea "actual"
        current_date_time = start_date + timedelta(
            days=random.randint(0, 150),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        inicio_falla = current_date_time
        fin_falla = inicio_falla + timedelta(minutes=duracion_minutos)

        # Seleccionar una plantilla de novedad y rellenar
        template = random.choice(novedades_templates)

        # Crear diccionario con todos los posibles parámetros
        format_params = {
            "sistema": sistema_afectado.lower(),
            "equipo": equipo.lower(),
            "parte_especifica": random.choice([
                "bomba",
                "motor",
                "sensor",
                "válvula",
                "cableado",
                "pistón",
                "eje",
                "tarjeta electrónica",
            ]),
            "tipo_falla": random.choice([
                "eléctrico",
                "mecánico",
                "hidráulico",
                "intermitente",
            ]),
            "horas_demora": round(duracion_minutos / 60, 1),
            "irregular": random.choice(["errático", "anormal", "lento", "débil"]),
            "sintoma": random.choice([
                "vibración",
                "ruido extraño",
                "olor a quemado",
                "calentamiento",
            ]),
            "causa_potencial": random.choice([
                "desgaste",
                "cortocircuito",
                "bloqueo",
                "falla de software",
            ]),
            "problema_general": random.choice([
                "sobrecarga",
                "falla eléctrica",
                "bloqueo mecánico",
                "error de sistema",
            ]),
            "alarma": random.choice([
                "ALARM-01",
                "ALM-SYS-23",
                "ERROR-C05",
                "Emergencia P-1",
            ]),
            "componente": random.choice([
                "rodamiento",
                "engranaje",
                "cadena",
                "motor",
                "brazo",
                "circuito",
            ]),
            "operador": random.choice(["Juan Pérez", "Maria Gómez", "Pedro López"]),
            "turno_trabajo": random.choice(["mañana", "tarde", "noche"]),
            "sistema_afectado": sistema_afectado.lower(),
            "zona_fuga": random.choice(["base", "unión", "tubo", "sellado"]),
            "accion_tomada": random.choice([
                "parada de emergencia",
                "aislamiento",
                "limpieza provisional",
                "apagar equipo",
            ]),
            "horas_adicionales": round(random.uniform(0.5, 3.0), 1),
            "parte_electrica": random.choice([
                "conexión",
                "fusible",
                "cableado",
                "panel de control",
            ]),
            "parte_grua": random.choice(["pluma", "troley", "gancho"]),
            "parte_carretilla": random.choice(["rueda", "horquilla", "dirección"]),
            "tipo_falla_mecanica": random.choice([
                "desgaste de piezas",
                "desalineación",
                "falla de rodamiento",
            ]),
            "buque_nombre": buque,
        }

        # Formatear el texto usando solo los parámetros que existen en el template
        try:
            novedad_text = template.format(**format_params)
        except KeyError as e:
            # Si falta algún parámetro, usar un texto genérico
            novedad_text = f"Falla en {equipo} - Sistema {sistema_afectado}. Requiere revisión técnica."

        # Inyectar errores de tipeo en un porcentaje de las descripciones
        if random.random() < 0.3:  # 30% de probabilidad de tener errores de tipeo
            novedad_text = inyectar_error(
                novedad_text, error_rate=0.08
            )  # Mayor tasa de error para simular "prisa"

        data.append({
            "Equipo": equipo,
            "Novedad": novedad_text,
            "Inicio Hora Falla": inicio_falla.strftime("%Y-%m-%d %H:%M"),
            "Hora Fin Falla": fin_falla.strftime("%Y-%m-%d %H:%M"),
            "Sistema Afectado": sistema_afectado,
            "Buque": buque,
        })

    df = pd.DataFrame(data)

    # Añadir algunos nulos intencionales
    num_nulos = random.randint(2, 5)  # 2 a 5 nulos
    for _ in range(num_nulos):
        row = random.randint(0, num_reports - 1)
        col = random.choice(["Equipo", "Novedad", "Sistema Afectado", "Buque"])
        df.at[row, col] = np.nan

    # Guardar en XLSX
    try:
        df.to_excel(output_filename, index=False)
        print(f"Archivo '{output_filename}' generado con éxito con {num_reports} reportes.")
        print(f"Ruta completa: {os.path.abspath(output_filename)}")
    except Exception as e:
        print(f"Error al guardar el archivo XLSX: {e}")


# --- Ejecutar la generación del archivo ---
if __name__ == "__main__":
    generate_realistic_epp_reports(num_reports=100)