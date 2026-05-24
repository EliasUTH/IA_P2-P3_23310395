import math

print("=== GRÁFICOS: RENDERIZADO DE TEXTURAS Y SOMBRAS ===\n")

def generar_render():
    # Configuración de la "pantalla"
    ancho = 40
    alto = 20
    
    # Dirección de la luz (Vector unitario L)
    luz_x, luz_y, luz_z = 1.0, -1.0, 1.0
    mag_luz = math.sqrt(luz_x**2 + luz_y**2 + luz_z**2)
    luz_x, luz_y, luz_z = luz_x/mag_luz, luz_y/mag_luz, luz_z/mag_luz

    # Caracteres de "textura/sombra" por densidad
    rampa_textura = " .:-=+*#%@" # De más claro a más oscuro

    for y in range(alto):
        linea = ""
        for x in range(ancho):
            # Normalizar coordenadas de -1 a 1
            nx = (x / ancho) * 2 - 1
            ny = (y / alto) * 2 - 1
            
            # Ecuación de la esfera: x^2 + y^2 + z^2 = 1
            z2 = 1 - nx**2 - ny**2
            
            if z2 > 0:
                nz = math.sqrt(z2)
                
                # CÁLCULO DE SOMBRA (Producto punto entre Normal y Luz)
                # Intensidad = N · L (Lambertian Shading)
                intensidad = nx * luz_x + ny * luz_y + nz * luz_z
                
                # CÁLCULO DE TEXTURA (Patrón procedimental basado en coordenadas)
                # Creamos un patrón de cuadrícula (ajedrez)
                patron = (int(x * 0.5) + int(y * 0.5)) % 2
                
                # Combinar sombra y textura
                if intensidad < 0: intensidad = 0
                
                # Si el patrón es 1, oscurecemos un poco más la "textura"
                idx = int(intensidad * (len(rampa_textura) - 1))
                if patron == 0:
                    idx = max(0, idx - 2) # Aplicar textura visual
                
                linea += rampa_textura[idx]
            else:
                linea += " " # Fondo vacío
        print(linea)

# --- EJECUCIÓN ---
print("Renderizando objeto con sombreado de Lambert y textura de tablero...")
generar_render()

print("\n=== ANÁLISIS TÉCNICO ===")
print("1. SOMBRA: Se calcula con el producto punto. Si la superficie mira a la luz, es clara.")
print("2. TEXTURA: Se aplica matemáticamente sobre las coordenadas (x, y) antes de pintar.")
print("3. RASTERIZADO: Convertimos valores continuos (intensidad) en discretos (caracteres).")