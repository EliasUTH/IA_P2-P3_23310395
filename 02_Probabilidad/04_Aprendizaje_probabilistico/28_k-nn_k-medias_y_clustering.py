import random

print("=== CLUSTERING CON K-MEANS ===\n")

# Datos: Puntos en 1D (ej. estaturas o ingresos)
datos = [2, 4, 10, 12, 11, 3, 30, 31, 33, 35, 5, 32]
k = 2  # Queremos separar en 2 grupos

def k_means(data, k_clusters):
    # Inicialización: centros al azar
    centros = random.sample(data, k_clusters)
    
    for i in range(5): # 5 iteraciones suelen bastar para este ejemplo
        clusters = [[] for _ in range(k_clusters)]
        
        # Asignación
        for x in data:
            distancias = [abs(x - c) for c in centros]
            indice = distancias.index(min(distancias))
            clusters[indice].append(x)
        
        # Actualización de centros
        centros = [sum(c)/len(c) if c else 0 for c in clusters]
        print(f"Iteración {i+1}: Centros en {centros}")
    
    return centros, clusters

centros, grupos = k_means(datos, k)
print(f"\nResultado final: Grupo 1 {grupos[0]} | Grupo 2 {grupos[1]}")