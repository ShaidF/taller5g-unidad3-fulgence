from PIL import Image
import math


def dda(pixels, x0, y0, x1, y1, color, ancho, alto):
    dx, dy = x1 - x0, y1 - y0
    pasos = max(abs(dx), abs(dy))
    if pasos == 0:
        return
    x_inc, y_inc = dx / pasos, dy / pasos
    x, y = x0, y0
    for _ in range(int(pasos) + 1):
        px, py = round(x), round(y)
        if 0 <= px < ancho and 0 <= py < alto:
            pixels[px, py] = color
        x += x_inc
        y += y_inc


def dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto):
    dda(pixels, x0, y0, x1, y0, color, ancho, alto)
    dda(pixels, x1, y0, x1, y1, color, ancho, alto)
    dda(pixels, x1, y1, x0, y1, color, ancho, alto)
    dda(pixels, x0, y1, x0, y0, color, ancho, alto)


def dibujar_triangulo(pixels, p1, p2, p3, color, ancho, alto):
    dda(pixels, p1[0], p1[1], p2[0], p2[1], color, ancho, alto)
    dda(pixels, p2[0], p2[1], p3[0], p3[1], color, ancho, alto)
    dda(pixels, p3[0], p3[1], p1[0], p1[1], color, ancho, alto)


def dibujar_cuerpo_casa(pixels, x0, y0, x1, y1, color, ancho, alto):
    dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto)


def dibujar_techo(pixels, izq, cima, der, color, ancho, alto):
    dibujar_triangulo(pixels, izq, cima, der, color, ancho, alto)


def dibujar_puerta(pixels, x0, y0, x1, y1, color, ancho, alto):
    dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto)
    px, py = x1 - 8, (y0 + y1) // 2
    dda(pixels, px - 2, py, px + 2, py, color, ancho, alto)
    dda(pixels, px, py - 2, px, py + 2, color, ancho, alto)


def dibujar_ventana(pixels, x, y, lado, color, ancho, alto):
    dibujar_rectangulo(pixels, x, y, x + lado, y + lado, color, ancho, alto)
    medio = lado // 2
    dda(pixels, x + medio, y, x + medio, y + lado, color, ancho, alto)
    dda(pixels, x, y + medio, x + lado, y + medio, color, ancho, alto)


def dibujar_sol(pixels, cx, cy, radio, n_rayos, color, ancho, alto):
    for i in range(n_rayos):
        angulo = 2 * math.pi * i / n_rayos
        x = cx + round(radio * math.cos(angulo))
        y = cy + round(radio * math.sin(angulo))
        dda(pixels, cx, cy, x, y, color, ancho, alto)


def dibujar_piso(pixels, y, color, ancho, alto):
    dda(pixels, 0, y, ancho - 1, y, color, ancho, alto)


def dibujar_cesped(pixels, y_inicio, color_arriba, color_abajo, ancho, alto):
    filas = alto - y_inicio
    for k in range(filas):
        t = k / max(filas - 1, 1)
        color = tuple(round(a + (b - a) * t) for a, b in zip(color_arriba, color_abajo))
        dda(pixels, 0, y_inicio + k, ancho - 1, y_inicio + k, color, ancho, alto)


def dibujar_arbol(pixels, x_centro, y_base, color_tronco, color_copa, ancho, alto):
    dibujar_rectangulo(pixels, x_centro - 10, y_base - 60, x_centro + 10, y_base,
                       color_tronco, ancho, alto)
    dibujar_triangulo(pixels, (x_centro - 45, y_base - 60), (x_centro, y_base - 150),
                      (x_centro + 45, y_base - 60), color_copa, ancho, alto)


def dibujar_nube(pixels, cx, cy, color, ancho, alto):
    bultos = [(-30, 0, 22), (0, -10, 28), (32, 0, 20)]
    segmentos = 12
    for dx, dy, r in bultos:
        bx, by = cx + dx, cy + dy
        for s in range(segmentos):
            a0 = math.pi + math.pi * s / segmentos
            a1 = math.pi + math.pi * (s + 1) / segmentos
            dda(pixels,
                bx + round(r * math.cos(a0)), by + round(r * math.sin(a0)),
                bx + round(r * math.cos(a1)), by + round(r * math.sin(a1)),
                color, ancho, alto)
    dda(pixels, cx - 52, cy, cx + 52, cy, color, ancho, alto)


def dibujar_chimenea_con_humo(pixels, x0, x1, y_tope, techo_cima, techo_der,
                              color_chimenea, color_humo, ancho, alto):
    def y_techo(x):
        (xc, yc), (xd, yd) = techo_cima, techo_der
        return round(yc + (yd - yc) * (x - xc) / (xd - xc))

    dda(pixels, x0, y_tope, x0, y_techo(x0), color_chimenea, ancho, alto)
    dda(pixels, x1, y_tope, x1, y_techo(x1), color_chimenea, ancho, alto)
    dda(pixels, x0, y_tope, x1, y_tope, color_chimenea, ancho, alto)

    x, y = (x0 + x1) // 2, y_tope - 6
    for paso in range(8):
        nx = x + (10 if paso % 2 == 0 else -6) + paso
        ny = y - 12
        dda(pixels, x, y, nx, ny, color_humo, ancho, alto)
        x, y = nx, ny


ancho, alto = 600, 500
imagen = Image.new("RGB", (ancho, alto), (200, 230, 255))
pixels = imagen.load()

MARRON_CASA = (120, 70, 30)
ROJO_TECHO = (200, 30, 30)
VERDE_PUERTA = (20, 110, 60)
AZUL_VENTANA = (30, 60, 180)
AMARILLO_SOL = (240, 170, 0)
NEGRO_PISO = (0, 0, 0)
GRIS_CHIMENEA = (90, 90, 90)
GRIS_HUMO = (150, 150, 160)
BLANCO_NUBE = (255, 255, 255)
VERDE_COPA = (30, 140, 40)
MARRON_TRONCO = (100, 60, 20)

Y_PISO = 420

dibujar_cesped(pixels, Y_PISO + 1, (110, 190, 80), (40, 100, 30), ancho, alto)

dibujar_piso(pixels, Y_PISO, NEGRO_PISO, ancho, alto)
dibujar_cuerpo_casa(pixels, 180, 250, 420, Y_PISO, MARRON_CASA, ancho, alto)

techo_izq, techo_cima, techo_der = (160, 250), (300, 130), (440, 250)
dibujar_techo(pixels, techo_izq, techo_cima, techo_der, ROJO_TECHO, ancho, alto)

dibujar_puerta(pixels, 275, 330, 325, Y_PISO, VERDE_PUERTA, ancho, alto)
dibujar_ventana(pixels, 205, 280, 50, AZUL_VENTANA, ancho, alto)
dibujar_ventana(pixels, 345, 280, 50, AZUL_VENTANA, ancho, alto)
dibujar_sol(pixels, 525, 75, 50, 16, AMARILLO_SOL, ancho, alto)

dibujar_chimenea_con_humo(pixels, 360, 385, 150, techo_cima, techo_der,
                          GRIS_CHIMENEA, GRIS_HUMO, ancho, alto)
dibujar_arbol(pixels, 80, Y_PISO, MARRON_TRONCO, VERDE_COPA, ancho, alto)
dibujar_arbol(pixels, 515, Y_PISO, MARRON_TRONCO, VERDE_COPA, ancho, alto)
dibujar_nube(pixels, 110, 80, BLANCO_NUBE, ancho, alto)
dibujar_nube(pixels, 300, 55, BLANCO_NUBE, ancho, alto)

imagen.save("casa.png")
print("Imagen generada: casa.png")
