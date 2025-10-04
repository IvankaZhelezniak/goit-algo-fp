# Рекурсія. Створення фрактала “дерево Піфагора” за допомогою рекурсії.

# Програма, яка використовує  рекурсію для створення фрактала “дерево Піфагора”. 
# Програма візуалізує фрактал “дерево Піфагора”, і користувач може вказати рівень рекурсії.


import numpy as np
import matplotlib.pyplot as plt

def draw_square(ax, pts):
    # Малює квадрат, заданий 4 вершинами (комплексні числа) проти год.стрілки.
    xs = [z.real for z in pts] + [pts[0].real]
    ys = [z.imag for z in pts] + [pts[0].imag]
    ax.plot(xs, ys, linewidth=1, color="#8B3A3A")  # колір гілок

def pythagoras(ax, p, v, level, alpha=np.pi/4):
    """
    Рекурсивне малювання дерева Піфагора.

    p     — комплексне число: нижня-ліва вершина поточного квадрата.
    v     — комплексний вектор уздовж нижнього ребра (довжина = сторона квадрата).
    level — глибина рекурсії (0 означає лише поточний квадрат).
    alpha — кут трикутника над квадратом (рад). 45° дає симетричне дерево.
    """
    if level < 0:
        return

    # Вектор, перпендикулярний v (поворот на +90°): множення на 1j у комплексній площині.
    w = v * 1j

    # Поточний квадрат: p -> p+v -> p+v+w -> p+w
    square = (p, p + v, p + v + w, p + w)
    draw_square(ax, square)

    if level == 0:
        return

    # ТУТ "пересклеюю" посилання (геометрію) до нащадків
    # Обчислюю сторони дочірніх квадратів як вектори:
    # vL і vR — це проєкції по катетах прямокутного трикутника під кутом alpha.
    vL =  v * np.cos(alpha) - w * np.sin(alpha)    # лівий дочірній квадрат
    vR =  v * np.sin(alpha) + w * np.cos(alpha)    # правий дочірній квадрат

    # Тепер визначаю їх нові "батьківські" точки (аналог зміни посилань):
    # Лівий квадрат «починається» в верхньо-лівій вершині батька.
    pL = p + v
    # Правий квадрат «починається» у верхньо-правій, але зміщений на власний вектор vR.
    pR = p + v + w - vR

    # Рекурсивно малюю обидва піддерева (щораз менші квадрати й нові «посилання»).
    pythagoras(ax, pL, vL, level - 1, alpha)
    pythagoras(ax, pR, vR, level - 1, alpha)

def draw_pythagoras_tree(level=8, angle_deg=45, size=1.0):
    """Точка входу: малює дерево з заданою глибиною й кутом гілок."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    ax.axis("off")

    alpha = np.deg2rad(angle_deg)
    base_left = complex(-size/2, 0.0)     # нижня-ліва точка базового квадрата
    base_vec  = complex(size, 0.0)        # вектор уздовж нижнього ребра

    pythagoras(ax, base_left, base_vec, level, alpha)
    plt.show()

if __name__ == "__main__":
    try:
        n = int(input("Вкажіть рівень рекурсії (0–12): "))
    except Exception:
        n = 8
    draw_pythagoras_tree(level=n, angle_deg=45)
