import turtle

print("=== GRÁFICOS POR COMPUTADOR: RECURSIÓN Y GEOMETRÍA ===\n")

def dibujar_arbol(longitud_rama, t):
    """Genera un árbol fractal mediante recursión."""
    if longitud_rama > 5:
        # Dibujar tronco/rama actual
        t.forward(longitud_rama)
        
        # Rama derecha
        t.right(20)
        dibujar_arbol(longitud_rama - 15, t)
        
        # Rama izquierda (regresamos y giramos al otro lado)
        t.left(40)
        dibujar_arbol(longitud_rama - 15, t)
        
        # Regresar a la posición original
        t.right(20)
        t.backward(longitud_rama)

def inicializar_graficos():
    try:
        ventana = turtle.Screen()
        ventana.bgcolor("white")
        ventana.title("Gráficos por Computador - Árbol Fractal")
        
        t = turtle.Turtle()
        t.left(90)
        t.up()
        t.backward(100)
        t.down()
        t.color("green")
        t.speed("fastest")
        
        print("Abriendo ventana de gráficos...")
        dibujar_arbol(75, t)
        print("Renderizado completo.")
        
        ventana.exitonclick()
    except Exception as e:
        print(f"Error al inicializar gráficos: {e}")
        print("Nota: Turtle requiere un entorno con interfaz gráfica (GUI).")

if __name__ == "__main__":
    inicializar_graficos()