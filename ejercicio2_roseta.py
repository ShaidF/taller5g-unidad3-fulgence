from PIL import Image
import colorsys
import math


def bresenham(pixels, x0, y0, x1, y1, color, ancho, alto):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        if 0 <= x < ancho and 0 <= y < alto:
            pixels[x, y] = color
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


def generar_puntos_circulo(cx, cy, radio, n):
    puntos = []
    for i in range(n):
        angulo = 2 * math.pi * i / n
        x = cx + round(radio * math.cos(angulo))
        y = cy + round(radio * math.sin(angulo))
        puntos.append((x, y))
    return puntos


def color_por_distancia(p, q, cx, cy, radio):
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    t = min(math.hypot(mx - cx, my - cy) / radio, 1.0)
    tono = 0.83 - 0.66 * t
    r, g, b = colorsys.hsv_to_rgb(tono, 0.9, 1.0)
    return (round(r * 255), round(g * 255), round(b * 255))


def centro_y_radio(puntos):
    n = len(puntos)
    cx = sum(x for x, _ in puntos) / n
    cy = sum(y for _, y in puntos) / n
    radio = max(math.hypot(x - cx, y - cy) for x, y in puntos)
    return cx, cy, radio


def dibujar_roseta(pixels, puntos, ancho, alto):
    cx, cy, radio = centro_y_radio(puntos)
    n = len(puntos)

    pares = [(puntos[i], puntos[j]) for i in range(n) for j in range(i + 1, n)]
    pares.sort(key=lambda pq: -math.hypot((pq[0][0] + pq[1][0]) / 2 - cx,
                                          (pq[0][1] + pq[1][1]) / 2 - cy))

    for p, q in pares:
        color = color_por_distancia(p, q, cx, cy, radio)
        bresenham(pixels, p[0], p[1], q[0], q[1], color, ancho, alto)
    return len(pares)


def dibujar_roseta_salto(pixels, puntos, salto, ancho, alto):
    cx, cy, radio = centro_y_radio(puntos)
    n = len(puntos)
    for i in range(n):
        p, q = puntos[i], puntos[(i + salto) % n]
        r, g, b = colorsys.hsv_to_rgb(i / n, 0.85, 1.0)
        bresenham(pixels, p[0], p[1], q[0], q[1],
                  (round(r * 255), round(g * 255), round(b * 255)), ancho, alto)


def generar_animacion(nombre, ancho=700, alto=700):
    cuadros = []
    for n in range(5, 25):
        img = Image.new("RGB", (ancho, alto), (0, 0, 0))
        dibujar_roseta(img.load(), generar_puntos_circulo(ancho // 2, alto // 2, 300, n),
                       ancho, alto)
        cuadros.append(img)
    cuadros[0].save(nombre, save_all=True, append_images=cuadros[1:],
                    duration=300, loop=0)


ANCHO, ALTO = 700, 700
CX, CY, RADIO = 350, 350, 300
FONDO = (0, 0, 0)

for n in [12, 24, 36]:
    img = Image.new("RGB", (ANCHO, ALTO), FONDO)
    pixels = img.load()
    puntos = generar_puntos_circulo(CX, CY, RADIO, n)
    lineas = dibujar_roseta(pixels, puntos, ANCHO, ALTO)
    img.save(f"roseta_{n}.png")
    print(f"roseta_{n}.png generado ({lineas} lineas)")
    if n == 24:
        img.save("roseta.png")
        print("roseta.png generado (N = 24)")

img = Image.new("RGB", (ANCHO, ALTO), FONDO)
dibujar_roseta_salto(img.load(), generar_puntos_circulo(CX, CY, RADIO, 36), 13, ANCHO, ALTO)
img.save("roseta_salto13.png")
print("roseta_salto13.png generado")

generar_animacion("roseta_animada.gif", ANCHO, ALTO)
print("roseta_animada.gif generado")
