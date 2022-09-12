#!/usr/bin/env python3

# Para importar el modulo Arcade Python
import arcade

# Crear la ventana, mínimo se tiene que entregar el ancho, alto y el título de la ventana, en ese orden
arcade.open_window(600, 600, "Learning Example")

# Para dar un color de fondo
arcade.set_background_color(arcade.csscolor.SKY_BLUE)

# Comenzar a dibujar
arcade.start_render()

# ... Aqui va el codigo para dibujar en pantalla

# Dibujar un rectangulo relleno de color indicando coordenadas de los bordes
# Toma los parametros en el orden: izquierda, derecha, superior, inferior, color
arcade.draw_lrtb_rectangle_filled(0, 599, 300, 0, arcade.csscolor.GREEN)  # draw left-right-top-bottom rectangle

# Dibujar un rectangulo relleno indicando coordenadas del centro eje x e y
# Toma los parametros en el orden: x, y, ancho, alto, color
arcade.draw_rectangle_filled(100, 320, 20, 60, arcade.csscolor.SIENNA)

# Dibujar un circulo relleno indicando coordenadas del centro de eje x e y
# Toma los parametros en el orden x, y, radio, color
arcade.draw_circle_filled(100, 350, 30, arcade.csscolor.DARK_GREEN)

##### DIBUJO PARA ENTENDER LA RECLACION ENTRE RECTANGULO Y ELIPSE #####
# Dibujar una elipse indicando las coordenadas del centro de eje x e y
# Toma los parametros en el orden x, y, ancho, alto, color y opcionalmente la inclinacion
# arcade.draw_ellipse_outline(300, 300, 350, 200, arcade.csscolor.BLACK, 3)
# arcade.draw_rectangle_outline(300,300,350,200, arcade.csscolor.RED, 3)
########################################################################

# Dibujar un arbol usando rectangulo y elipse
arcade.draw_rectangle_filled(200, 320, 20, 60, arcade.csscolor.SIENNA)
arcade.draw_ellipse_filled(200, 370, 60, 80, arcade.csscolor.DARK_GREEN)

# Dibujar un arbol con rectangulo y un arco
arcade.draw_rectangle_filled(300, 320, 20, 60, arcade.csscolor.SIENNA)
# Dibujar un arco relleno indicando coordenadas del centro eje x e y
# Toma los parametros en el orden x, y, ancho, alto, color, angulo inicial, angulo final
arcade.draw_arc_filled(300, 340, 60, 100, arcade.csscolor.DARK_GREEN, 0, 180)

# Dibujar un arbol con rectangulo y un triangulo
arcade.draw_rectangle_filled(400, 320, 20, 60, arcade.csscolor.SIENNA)
# Dibujar un triangulo relleno indicando coordenadas de cada punto
# Toma los parametros en el orden x1, y1, x2, y2, x3, y3, color
arcade.draw_triangle_filled(400, 400, 370, 320, 430, 320, arcade.csscolor.DARK_GREEN)

# Dibujar un arbol con rectangulo y un poligono
arcade.draw_rectangle_filled(500, 320, 20, 60, arcade.csscolor.SIENNA)
# Dibujar un poligono relleno con una lista de coordenadas de cada punto
# Toma los parametros en el orden (lista de puntos), color
arcade.draw_polygon_filled(((500, 400), (480, 360), (470, 320), (530, 320), (520, 360)), arcade.csscolor.DARK_GREEN)

#### EJEMPLO DIBUJAR SOL CON RAYOS DESDE SI ####
# Dibujar el sol
arcade.draw_circle_filled(500, 550, 40, arcade.color.YELLOW)
# Rayos hacia izquierda, derecha, arriba, abajo
# Dibujar linea indicando las coordenadas de inicio y las coordenadas finales
# Toma los parametros en el orden x1, y1, x2, y2, color, opcional ancho de linea
arcade.draw_line(500, 550, 400, 550, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 600, 550, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 500, 450, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 500, 650, arcade.color.YELLOW, 3)
# Rayos en diagonal

arcade.draw_line(500, 550, 550, 600, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 550, 500, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 450, 600, arcade.color.YELLOW, 3)
arcade.draw_line(500, 550, 450, 500, arcade.color.YELLOW, 3)

# Dibujar Texto
# Toma los parametros en el orden texto a dibujar, x, y, color, tamaño de fuente
arcade.draw_text("Plantate uno!", 150, 230, arcade.color.BLACK, 24)

# Terminar de dibujar
arcade.finish_render()



# Mantener la ventana abierta hasta recibir la orden de cerrar
arcade.run()
