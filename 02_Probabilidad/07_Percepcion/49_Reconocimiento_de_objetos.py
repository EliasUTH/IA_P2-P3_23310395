print("=== SISTEMA DE RECONOCIMIENTO DE OBJETOS ===\n")

# --- 1. BASE DE CONOCIMIENTOS (Plantillas de Objetos) ---
# Representamos formas simples como firmas de píxeles
plantillas = {
    "Cuadrado": [
        [255, 255, 255],
        [255, 0,   255],
        [255, 255, 255]
    ],
    "Cruz": [
        [0,   255, 0  ],
        [255, 255, 255],
        [0,   255, 0  ]
    ],
    "Triangulo": [
        [0,   255, 0  ],
        [255, 255, 255],
        [255, 0,   255]
    ]
}

# --- 2. OBJETO DESCONOCIDO (Capturado por la "Cámara") ---
# Nota: Tiene un poco de ruido o variación respecto a la plantilla
objeto_detectado = [
    [0,   250, 0  ],
    [255, 255, 250],
    [5,   255, 0  ]
]

# --- 3. ALGORITMO DE RECONOCIMIENTO (Distancia Euclidiana) ---
def reconocer_objeto(entrada, conocimiento):
    mejor_coincidencia = None
    menor_error = float('inf')

    for nombre, forma in conocimiento.items():
        error_acumulado = 0
        # Comparamos pixel a pixel
        for i in range(3):
            for j in range(3):
                # Calculamos la diferencia absoluta entre la entrada y la plantilla
                error_acumulado += abs(entrada[i][j] - forma[i][j])
        
        print(f"Comparando con {nombre}... Error: {error_acumulado}")
        
        if error_acumulado < menor_error:
            menor_error = error_acumulado
            mejor_coincidencia = nombre
            
    return mejor_coincidencia, menor_error

# --- 4. EJECUCIÓN ---
print("Iniciando escaneo de objeto...")
resultado, confianza = reconocer_objeto(objeto_detectado, plantillas)

print("-" * 40)
if confianza < 100: # Umbral de tolerancia
    print(f"OBJETO RECONOCIDO: Es una '{resultado}'")
    print(f"Nivel de error: {confianza} (Aceptable)")
else:
    print("Objeto no identificado en la base de datos.")

print("\n=== ANÁLISIS TÉCNICO ===")
print("1. El sistema usa 'Template Matching' para encontrar la menor diferencia.")
print("2. Es robusto ante pequeños ruidos (como el valor 250 en vez de 255).")
print("3. Este es el antecesor de los clasificadores modernos basados en descriptores.")