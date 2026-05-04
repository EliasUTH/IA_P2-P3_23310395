import time
import os

print("=== SIMULACIÓN DE MOVIMIENTO FÍSICO ===\n")

# --- 1. CONFIGURACIÓN DEL ENTORNO ---
ANCHO = 40
ALTO = 15
caracter_objeto = "●"

# --- 2. VARIABLES DE ESTADO (Vectores) ---
pos_x, pos_y = 1, 1      # Posición inicial
vel_x, vel_y = 1, 0      # Velocidad inicial
gravedad = 0.5           # Aceleración hacia abajo
friccion = 0.8           # Pérdida de energía al rebotar

def limpiar_pantalla():
    # Limpia la consola dependiendo del sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')

def renderizar(px, py):
    """Dibuja el objeto en una rejilla de texto."""
    for y in range(ALTO):
        linea = ""
        for x in range(ANCHO):
            if x == int(px) and y == int(py):
                linea += caracter_objeto
            elif y == ALTO - 1:
                linea += "_" # Suelo
            else:
                linea += " "
        print(linea)

# --- 3. BUCLE DE ANIMACIÓN ---
print("Iniciando simulación... Presiona Ctrl+C para detener.")
time.sleep(1)

try:
    for _ in range(50): # 50 cuadros de animación
        limpiar_pantalla()
        
        # APLICAR FÍSICA
        vel_y += gravedad    # La gravedad aumenta la velocidad vertical
        pos_x += vel_x       # La posición cambia según la velocidad
        pos_y += vel_y
        
        # DETECCIÓN DE COLISIÓN (REBOTE)
        # Rebote en el suelo
        if pos_y >= ALTO - 1:
            pos_y = ALTO - 2
            vel_y *= -friccion # Rebota y pierde fuerza
            
        # Rebote en paredes
        if pos_x >= ANCHO - 1 or pos_x <= 0:
            vel_x *= -1
            
        renderizar(pos_x, pos_y)
        time.sleep(0.1) # Control de velocidad de fotogramas (FPS)

except KeyboardInterrupt:
    print("\nSimulación detenida por el usuario.")

print("\n=== ANÁLISIS TÉCNICO ===")
print("1. Vectores: El movimiento se descompone en ejes X e Y independientes.")
print("2. Frame Rate: Usamos 'time.sleep' para sincronizar el tiempo de la CPU con el ojo humano.")
print("3. Euler Integration: Calculamos la nueva posición sumando la velocidad paso a paso.")