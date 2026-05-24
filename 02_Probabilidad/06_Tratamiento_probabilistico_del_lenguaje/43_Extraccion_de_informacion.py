import re

print("=== SISTEMA DE EXTRACCIÓN DE INFORMACIÓN (IE) ===\n")

# --- 1. EL TEXTO FUENTE ---
texto_sucio = """
El científico Albert Einstein nació en Alemania. 
La investigadora Marie Curie trabajó en Francia. 
Isaac Newton vivió en Inglaterra y estudió física.
Guido van Rossum creó el lenguaje Python en los Países Bajos.
"""

# --- 2. DEFINICIÓN DE PATRONES (Ontología Simple) ---
# Buscamos la relación: [TÍTULO] + [NOMBRE] + [ACCIÓN] + [LUGAR]
patron_persona_lugar = r"(?P<titulo>El|La)\s+(?P<profesion>\w+)\s+(?P<nombre>[A-Z][\w\s]+)\s+(?P<accion>nació|trabajó|vivió|creó)\s+.*?en\s+(?P<lugar>[A-Z][\w\s]+?)(?=\.|\s+y)"

def extraer_datos(texto):
    base_de_datos = []
    
    # Buscamos coincidencias usando expresiones regulares avanzadas
    matches = re.finditer(patron_persona_lugar, texto)
    
    for m in matches:
        entidad = {
            "Sujeto": m.group("nombre").strip(),
            "Profesión": m.group("profesion").lower(),
            "Acción": m.group("accion"),
            "Ubicación": m.group("lugar").strip()
        }
        base_de_datos.append(entidad)
    
    return base_de_datos

# --- 3. EJECUCIÓN Y FORMATEO ---
informacion_estructurada = extraer_datos(texto_sucio)

print(f"{'SUJETO':<20} | {'PROFESIÓN':<12} | {'ACCIÓN':<10} | {'LUGAR'}")
print("-" * 65)

for info in informacion_estructurada:
    print(f"{info['Sujeto']:<20} | {info['Profesión']:<12} | {info['Acción']:<10} | {info['Ubicación']}")

print("\n=== ANÁLISIS DEL PROCESO ===")
print("1. El sistema convirtió texto libre en una tabla (Base de Datos).")
print("2. NER (Reconocimiento de Entidades): Identificó nombres y lugares por mayúsculas.")
print("3. Extracción de Relaciones: Vinculó a la persona con su ubicación mediante verbos clave.")