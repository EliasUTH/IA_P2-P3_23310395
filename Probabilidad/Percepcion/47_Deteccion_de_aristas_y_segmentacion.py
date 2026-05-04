import math

print("=== PROCESAMIENTO DE IMÁGENES: ARISTAS Y SEGMENTACIÓN ===\n")

# --- 1. SIMULACIÓN DE IMAGEN (Grises: 0-255) ---
# Una forma geométrica simple con bordes definidos
imagen = [
    [50,  50,  50,  50,  50,  50,  50],
    [50,  200, 200, 200, 200, 200, 50],
    [50,  200, 200, 200, 200, 200, 50],
    [50,  200, 200, 10,  10,  200, 50], # Agujero oscuro en medio
    [50,  200, 200, 10,  10,  200, 50],
    [50,  200, 200, 200, 200, 200, 50],
    [50,  50,  50,  50,  50,  50,  50]
]

FILAS = len(imagen)
COLS = len(imagen[0])

# --- 2. OPERADOR SOBEL (Detección de Aristas) ---
# Kernels para detectar cambios horizontales (Gx) y verticales (Gy)
sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
sobel_y = [[ 1, 2, 1], [ 0, 0, 0], [-1,-2,-1]]

def detectar_aristas(img):
    """Aplica el operador Sobel para encontrar bordes."""
    # Imagen de salida (reducida 1px por lado por el kernel 3x3)
    aristas = [[0 for _ in range(COLS-2)] for _ in range(FILAS-2)]
    
    for i in range(1, FILAS - 1):
        for j in range(1, COLS - 1):
            gx = 0
            gy = 0
            # Convolución con ambos kernels
            for ki in range(3):
                for kj in range(3):
                    val = img[i + ki - 1][j + kj - 1]
                    gx += val * sobel_x[ki][kj]
                    gy += val * sobel_y[ki][kj]
            
            # Magnitud del gradiente (Pitagoras)
            magnitud = math.sqrt(gx**2 + gy**2)
            aristas[i-1][j-1] = min(255, int(magnitud))
            
    return aristas

# --- 3. SEGMENTACIÓN (Umbralización Básica) ---
def segmentar_imagen(img, umbral=128):
    """Convierte la imagen en binaria (blanco y negro)."""
    filas = len(img)
    cols = len(img[0])
    binaria = [[0 for _ in range(cols)] for _ in range(filas)]
    
    for i in range(filas):
        for j in range(cols):
            # Decisión basada en el umbral
            binaria[i][j] = 255 if img[i][j] >= umbral else 0
            
    return binaria

# --- 4. EJECUCIÓN Y VISUALIZACIÓN ---

print("1. Imagen Original:")
for fila in imagen: print(f"  {fila}")

# Proceso A: Detectar Aristas
aristas_res = detectar_aristas(imagen)
print("\n2. Mapa de Aristas (Sobel):")
for fila in aristas_res: print(f"  {fila}")

# Proceso B: Segmentación de la original
# Usamos un umbral alto para separar el cuadro brillante (200) del fondo (50)
segmentada_res = segmentar_imagen(imagen, umbral=150)
print("\n3. Imagen Segmentada (Umbral=150):")
print("   (Muestra la forma principal)")
for fila in segmentada_res: print(f"  {fila}")

print("\n=== ANÁLISIS DE RESULTADOS ===")
print("1. Aristas: Nota valores altos (ej. 255, 150) donde hay cambios bruscos.")
print("2. Segmentación: Convierte la forma en un bloque sólido de 255 (blanco).")
print("3. Estabilidad: Este código no requiere librerías externas complejas.")