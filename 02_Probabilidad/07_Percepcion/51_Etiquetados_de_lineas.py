print("=== ALGORITMO DE ETIQUETADO DE COMPONENTES ===\n")

# --- 1. IMAGEN BINARIA (0: Fondo, 1: Objeto/Línea) ---
# Tenemos dos líneas separadas y un punto
imagen = [
    [0, 1, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0]
]

filas = len(imagen)
cols = len(imagen[0])

# --- 2. PROCESO DE ETIQUETADO (Primera Pasada Simplificada) ---
etiquetas = [[0 for _ in range(cols)] for _ in range(filas)]
siguiente_etiqueta = 1

for i in range(filas):
    for j in range(cols):
        if imagen[i][j] == 1:
            # Revisar vecino superior y vecino izquierdo
            vecino_sup = etiquetas[i-1][j] if i > 0 else 0
            vecino_izq = etiquetas[i][j-1] if j > 0 else 0
            
            if vecino_sup == 0 and vecino_izq == 0:
                # Es un objeto nuevo
                etiquetas[i][j] = siguiente_etiqueta
                siguiente_etiqueta += 1
            else:
                # Heredar etiqueta (priorizando superior)
                if vecino_sup != 0:
                    etiquetas[i][j] = vecino_sup
                else:
                    etiquetas[i][j] = vecino_izq

# --- 3. RESULTADOS ---
print("Imagen Original (Binaria):")
for f in imagen: print(f"  {f}")

print("\nImagen Etiquetada:")
for f in etiquetas: print(f"  {f}")

# Contar cuántos objetos distintos se encontraron
objetos_unicos = set()
for f in etiquetas:
    for p in f:
        if p != 0: objetos_unicos.add(p)

print(f"\nSe han detectado {len(objetos_unicos)} líneas/objetos independientes.")

print("\n=== ANÁLISIS TÉCNICO ===")
print("1. Conectividad: El algoritmo agrupa píxeles adyacentes bajo un mismo ID.")
print("2. Segmentación: Permite que la IA separe la 'Línea 1' de la 'Línea 3'.")
print("3. Aplicación: Es la base para contar células en medicina o piezas en una fábrica.")