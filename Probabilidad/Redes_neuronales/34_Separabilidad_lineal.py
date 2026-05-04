import random

print("=== PROBADOR DE SEPARABILIDAD LINEAL ===\n")

def comprobar_separabilidad(datos, etiquetas, max_intentos=1000):
    """
    Intenta encontrar un hiperplano separador. 
    Si lo logra antes de max_intentos, los datos son linealmente separables.
    """
    n_caracteristicas = len(datos[0])
    pesos = [0.0] * n_caracteristicas
    sesgo = 0.0
    tasa_aprendizaje = 0.1
    
    for intento in range(max_intentos):
        errores = 0
        for i in range(len(datos)):
            # Cálculo de la salida (neurona simple)
            suma_proyectada = sum(datos[i][j] * pesos[j] for j in range(n_caracteristicas)) + sesgo
            prediccion = 1 if suma_proyectada >= 0 else 0
            
            # Si hay error, ajustamos los pesos
            error = etiquetas[i] - prediccion
            if error != 0:
                for j in range(n_caracteristicas):
                    pesos[j] += tasa_aprendizaje * error * datos[i][j]
                sesgo += tasa_aprendizaje * error
                errores += 1
        
        # Si terminamos una época sin errores, es linealmente separable
        if errores == 0:
            return True, intento + 1, pesos, sesgo
            
    return False, max_intentos, pesos, sesgo

# --- CASO 1: DATOS SEPARABLES (Lógica AND) ---
X_separable = [[0,0], [0,1], [1,0], [1,1]]
y_separable = [0, 0, 0, 1]

# --- CASO 2: DATOS NO SEPARABLES (Lógica XOR) ---
X_no_separable = [[0,0], [0,1], [1,0], [1,1]]
y_no_separable = [0, 1, 1, 0]

# --- EJECUCIÓN ---
for nombre, X, y in [("AND (Separable)", X_separable, y_separable), 
                     ("XOR (No Separable)", X_no_separable, y_no_separable)]:
    
    es_separable, pasos, w, b = comprobar_separabilidad(X, y)
    
    print(f"Prueba con {nombre}:")
    if es_separable:
        print(f"  [✓] ¡Es Linealmente Separable! Encontrado en {pasos} iteraciones.")
        print(f"  Ecuación de la línea: {w[0]:.2f}x + {w[1]:.2f}y + {b:.2f} = 0")
    else:
        print(f"  [X] No es separable linealmente (falló tras {pasos} intentos).")
    print("-" * 50)

print("\n=== ANÁLISIS TÉCNICO ===")
print("1. El problema AND se separa con una línea porque los ceros y el uno están lejos.")
print("2. El problema XOR requiere una curva o dos líneas, por eso el Perceptrón falla.")
print("3. Para problemas no separables, usamos Redes Neuronales (Capa Oculta) o Kernels.")