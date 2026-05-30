print("=== INGENIERÍA DEL CONOCIMIENTO: DOMINIO GENEALÓGICO ===\n")
# --- FASE 1: DEFINICIÓN DEL VOCABULARIO (ONTOLOGÍA) ---
# Decidimos cómo representar nuestro mundo. 
# Usaremos tuplas para representar relaciones lógicas: (Predicado, Sujeto, Objeto)
# Ejemplo: ("progenitor", "Homero", "Bart") significa Progenitor(Homero, Bart)



class BaseConocimiento:
    def __init__(self):
        # Almacena los "Hechos" (Ground Atoms en Lógica de 1er Orden)
        self.hechos = set()
    def declarar_hecho(self, relacion, sujeto, objeto=None):
        """Registra una verdad fundamental en el sistema."""
        if objeto:
            hecho = (relacion, sujeto, objeto)
            print(f"[Hecho] {relacion}({sujeto}, {objeto})")
        else:
            # Para propiedades de un solo argumento, ej: Hombre(Homero)
            hecho = (relacion, sujeto)
            print(f"[Hecho] {relacion}({sujeto})")
        self.hechos.add(hecho)



# --- FASE 2: CODIFICACIÓN DE REGLAS (AXIOMAS DEL DOMINIO) ---
# Traducimos el sentido común humano a lógica ejecutable.
def inferir_abuelos(kb):
    """
    REGLA: ∀x,y,z (Progenitor(x, z) ∧ Progenitor(z, y) ⇒ Abuelo(x, y))
    "Si X es progenitor de Z, y Z es progenitor de Y, entonces X es abuelo de Y."
    """
    nuevos_hechos = set()
    # Buscamos pares de relaciones "progenitor" que se conecten
    for hecho1 in kb.hechos:
        if hecho1[0] == "progenitor":
            x, z = hecho1[1], hecho1[2]
            for hecho2 in kb.hechos:
                if hecho2[0] == "progenitor":
                    z_potencial, y = hecho2[1], hecho2[2]
                    # Si el hijo del primero es el padre del segundo (conexión 'z')
                    if z == z_potencial:
                        nuevo_hecho = ("abuelo", x, y)
                        if nuevo_hecho not in kb.hechos:
                            nuevos_hechos.add(nuevo_hecho)
                            print(f"[Deducción] abuelo({x}, {y})")
    kb.hechos.update(nuevos_hechos)
    return len(nuevos_hechos) > 0



def inferir_hermanos(kb):
    """
    REGLA: ∀x,y,z (Progenitor(z, x) ∧ Progenitor(z, y) ∧ x ≠ y ⇒ Hermano(x, y))
    "Si Z es progenitor de X, y Z también es progenitor de Y, y X no es Y, son hermanos."
    """
    nuevos_hechos = set()
    for h1 in kb.hechos:
        if h1[0] == "progenitor":
            z1, x = h1[1], h1[2]
            for h2 in kb.hechos:
                if h2[0] == "progenitor":
                    z2, y = h2[1], h2[2]
                    # Comparten progenitor y no son la misma persona
                    if z1 == z2 and x != y:
                        # Ordenamos alfabéticamente para evitar duplicados (Hermano(A,B) vs Hermano(B,A))
                        h_par = tuple(sorted([x, y]))
                        nuevo_hecho = ("hermano", h_par[0], h_par[1])
                        if nuevo_hecho not in kb.hechos:
                            nuevos_hechos.add(nuevo_hecho)
                            print(f"[Deducción] hermano({h_par[0]}, {h_par[1]})")
    kb.hechos.update(nuevos_hechos)
    return len(nuevos_hechos) > 0



# --- FASE 3: INSTANCIACIÓN DEL PROBLEMA (ALIMENTAR LA KB) ---
print("--- FASE 1 & 3: Alimentando Hechos Base ---")
mi_kb = BaseConocimiento()
mi_kb.declarar_hecho("progenitor", "Abe", "Homero")
mi_kb.declarar_hecho("progenitor", "Mona", "Homero")
mi_kb.declarar_hecho("progenitor", "Homero", "Bart")
mi_kb.declarar_hecho("progenitor", "Homero", "Lisa")
mi_kb.declarar_hecho("progenitor", "Homero", "Maggie")
mi_kb.declarar_hecho("progenitor", "Marge", "Bart")
mi_kb.declarar_hecho("progenitor", "Marge", "Lisa")
mi_kb.declarar_hecho("progenitor", "Marge", "Maggie")



# --- FASE 4: EJECUCIÓN DE INFERENCIA ---
print("\n--- FASE 2 & 4: Aplicando Axiomas (Generación de Conocimiento) ---")
# Ejecutamos las reglas hasta que ya no se generen nuevos hechos
hubo_cambios = True
while hubo_cambios:
    cambio_abuelos = inferir_abuelos(mi_kb)
    cambio_hermanos = inferir_hermanos(mi_kb)
    hubo_cambios = cambio_abuelos or cambio_hermanos



# --- FASE 5: CONSULTAS (QUERIES) ---
def consultar_relacion(kb, relacion, sujeto):
    """Busca todos los objetos que cumplen una relación con un sujeto dado."""
    resultados = [h[2] for h in kb.hechos if h[0] == relacion and h[1] == sujeto]
    # En el caso de "hermano", la relación es simétrica, revisamos ambos lados
    resultados += [h[1] for h in kb.hechos if h[0] == relacion and h[2] == sujeto]
    return list(set(resultados))



print("\n--- FASE 5: Consultas a la Base de Conocimiento ---")
print(f"¿Quiénes son los abuelos de Bart? -> {consultar_relacion(mi_kb, 'abuelo', 'Bart')}")
print(f"¿Quiénes son los hermanos de Lisa? -> {consultar_relacion(mi_kb, 'hermano', 'Lisa')}")
print("\n=== ANÁLISIS TÉCNICO ===")
print("1. Vocabulario Uniforme: Al definir que todo se basa en el predicado 'progenitor', reducimos la complejidad.")
print("2. Desacoplamiento: Los hechos (datos) están separados de las reglas (lógica). Podemos cambiar de familia sin reescribir las reglas.")
print("3. Cierre Transitivo: El bucle 'while hubo_cambios' asegura que el sistema derive TODAS las verdades posibles antes de detenerse.")