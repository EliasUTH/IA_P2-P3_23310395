print("=== PREPROCESADO DE IMÁGENES: FILTROS (CONVOLUCIÓN) ===\n")

# --- 1. SIMULACIÓN DE IMAGEN (Matriz 5x5) ---
# Valores de 0 (negro) a 255 (blanco)
imagen_original = [
    [10,  10,  10,  10,  10],
    [10,  255, 255, 255, 10],
    [10,  255, 10,  255, 10],
    [10,  255, 255, 255, 10],
    [10,  10,  10,  10,  10]
]

# --- 2. DEFINICIÓN DE KERNELS (Filtros) ---
# Filtro de Realce de Bordes (Laplaciano)
kernel_bordes = [
    [ 0, -1,  0],
    [-1,  4, -1],
    [ 0, -1,  0]
]

# Filtro de Suavizado (Media)
kernel_suave = [
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9]
]

# --- 3. FUNCIÓN DE CONVOLUCIÓN ---
def aplicar_filtro(imagen, kernel):
    filas = len(imagen)
    cols = len(imagen[0])
    # Creamos imagen de salida llena de ceros
    nueva_imagen = [[0 for _ in range(cols-2)] for _ in range(filas-2)]
    
    for i in range(1, filas - 1):
        for j in range(1, cols - 1):
            # Operación matemática de Convolución
            suma = 0
            for ki in range(3):
                for kj in range(3):
                    valor_pixel = imagen[i + ki - 1][j + kj - 1]
                    valor_kernel = kernel[ki][kj]
                    suma += valor_pixel * valor_kernel
            
            # Normalizar resultado (0-255)
            nueva_imagen[i-1][j-1] = max(0, min(255, int(suma)))
    
    return nueva_imagen

# --- 4. EJECUCIÓN Y COMPARACIÓN ---
resultado = aplicar_filtro(imagen_original, kernel_bordes)

print("Imagen Original (Fragmento):")
for fila in imagen_original:
    print(f"  {fila}")

print("\nImagen tras Filtro de Bordes (Laplaciano):")
for fila in resultado:
    print(f"  {fila}")

print("\n=== ANÁLISIS TÉCNICO ===")
print("1. El filtro detecta cambios bruscos de intensidad (bordes).")
print("2. Reducción de Dimensiones: Nota que la imagen resultante es 3x3")
print("   debido a que el kernel pierde los bordes (Padding).")
print("3. Este es el principio de las Redes Neuronales Convolucionales (CNN).")