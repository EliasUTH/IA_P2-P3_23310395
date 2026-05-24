print("=== SISTEMA DE RECONOCIMIENTO DE ESCRITURA (OCR) ===\n")

# --- 1. BASE DE DATOS DE CONOCIMIENTO ---
# Representamos letras en una matriz de 5x5
# El valor 1 representa tinta, el 0 representa papel vacío
conocimiento = {
    "A": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1]
    ],
    "L": [
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1]
    ]
}

# --- 2. CARÁCTER MANUSCRITO (Captura con ruido/variaciones) ---
# Intentaremos reconocer una 'A' un poco deformada
entrada_usuario = [
    [0, 1, 1, 0, 0], # Un poco corrida a la izquierda
    [1, 0, 0, 1, 0],
    [1, 1, 1, 1, 0],
    [1, 0, 0, 1, 0],
    [1, 0, 0, 1, 0]
]

# --- 3. ALGORITMO DE CLASIFICACIÓN (Métrica de Similitud) ---
def reconocer_caracter(matriz_entrada, base_datos):
    mejor_letra = "?"
    max_similitud = -1

    for letra, patron in base_datos.items():
        coincidencias = 0
        total_puntos = 25 # 5x5
        
        for i in range(5):
            for j in range(5):
                # Si ambos tienen tinta en el mismo lugar, sumamos puntos
                if matriz_entrada[i][j] == 1 and patron[i][j] == 1:
                    coincidencias += 1
                # Si ambos están vacíos, también hay similitud
                elif matriz_entrada[i][j] == 0 and patron[i][j] == 0:
                    coincidencias += 0.5 # Menos peso al vacío
        
        # Calcular porcentaje de similitud
        porcentaje = (coincidencias / total_puntos) * 100
        print(f"Similitud con '{letra}': {porcentaje:.2f}%")
        
        if porcentaje > max_similitud:
            max_similitud = porcentaje
            mejor_letra = letra
            
    return mejor_letra, max_similitud

# --- 4. EJECUCIÓN ---
print("Analizando trazos manuscritos...")
letra_final, confianza = reconocer_caracter(entrada_usuario, conocimiento)

print("-" * 40)
print(f"RESULTADO: El carácter parece ser una '{letra_final}'")
print(f"CONFIANZA: {confianza:.2f}%")

print("\n=== ANÁLISIS DEL EXPERTO ===")
print("1. El sistema no busca una copia exacta, sino el patrón más cercano.")
print("2. Es la base de cómo funcionan los sistemas de lectura de cheques y códigos postales.")
print("3. Para mejorar esto, se usan 'Momentos de Invarianza' (reconocer la letra aunque esté rotada).")