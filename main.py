# Вариант 13
# Усовершенствованный метод Эйлера && Милна

import numpy as np
from sympy import Symbol
import sympy
from tabulate import tabulate
import matplotlib.pyplot as plt

x = Symbol("x")
y = Symbol("y")
C = Symbol("C")

mn_min = -100
mx_max = 100
step_min = 0
step_max = 10


class Function:
    def __init__(self, func, text, real, const):
        self.real = real
        self.func = func
        self.text = text
        self.const = const


class Method:
    def __init__(self, func, text):
        self.func = func
        self.text = text


functions = [Function(y + (1 + x) * y ** 2, "y' = y + (1 + x)y^2", - sympy.exp(x) / (x * sympy.exp(x) + C),
                      - sympy.exp(x) / y - x * sympy.exp(x))]


def graph(data, real_func, left, right):
    plt.figure()
    # plt.grid(True)
    plt.title = "Графики"
    x_lines = np.linspace(left, right, 100)
    y_lines = []
    for xx in x_lines:
        y_lines.append(real_func.subs(x, xx))
    plt.plot(x_lines, y_lines, zorder=3, label="Реальный график")
    i = 0
    for arr in data:
        x_arr, y_arr, text = arr
        plt.plot(x_arr, y_arr, zorder=5 + i, label=text)
        i += 1
    plt.legend(fontsize='x-small')
    plt.show()


def advanced_eler(function, y0, step, left, right, isPrint=True):
    count = int((right - left) / step)
    x_array = np.linspace(left, right, count + 1)
    y_array = [y0]
    for i in range(1, len(x_array)):
        x_found_func = function.func.subs(x, x_array[i - 1])
        y_array.append(y_array[-1] + step / 2 * (x_found_func.subs(y, y_array[-1]) +
                                                 function.func.subs(x, x_array[i]).subs(y, y_array[
                                                     -1] + step * x_found_func.subs(y, y_array[-1]))))
    if isPrint:
        print("Полученная таблица Усовершенствованным методом Эйлера:")
        print(tabulate([x_array, y_array], tablefmt="grid", floatfmt="3.3f"))
    return x_array, y_array


def milan(function, y0, step, left, right):
    count = int((right - left) / step)
    new_r = (count - 2) * step + left
    x_array, y_array = advanced_eler(function, y0, step, left, new_r, False)
    x_array = np.linspace(left, right, count + 1)
    y_prog_list = []
    for i in range(4, len(x_array)):
        f_3 = function.func.subs(x, x_array[i - 3]).subs(y, y_array[i - 3])
        f_2 = function.func.subs(x, x_array[i - 2]).subs(y, y_array[i - 2])
        f_1 = function.func.subs(x, x_array[i - 1]).subs(y, y_array[i - 1])
        y_prog = y_array[i - 4] + 4 * step / 3 * (2 * f_3 - f_2 + 2 * f_1)
        f_prog = function.func.subs(x, x_array[i]).subs(y, y_prog)
        y_cor = y_array[i - 2] + step / 3 * (f_2 + 4 * f_1 + f_prog)
        y_prog_list.append(y_prog)
        y_array.append(y_cor)
    print("Полученная таблица Многомерным методом Милна:")
    print(tabulate([x_array, y_prog_list, y_array], tablefmt="grid", floatfmt="3.3f"))
    return x_array, y_array


methods = [Method(advanced_eler, "Усовершенствованный метод Эйлера"), Method(milan, "Многомерный метод Милна")]


def read_int(text, mn, mx, error_msg):
    while True:
        try:
            val = int(input(text))
            if mn <= val <= mx:
                return val
            else:
                raise ValueError
        except ValueError:
            print(error_msg)


def read_float(text, mn, mx, error_msg) -> float:
    while True:
        try:
            val = float(input(text))
            if mn <= val <= mx:
                return val
            else:
                raise ValueError
        except ValueError:
            print(error_msg)


def read_interval():
    while True:
        left = read_float(f"Введите левую границу из интервала ({mn_min};{mx_max}): ", mn_min, mx_max,
                          "Введено неправильное значение левой границы!")
        right = read_float(f"Введите левую границу из интервала ({'{:.3f}'.format(left)};{mx_max}): ", mn_min, mx_max,
                           "Введено неправильное значение правой границы!")
        if left >= right:
            print("Левая граница больше или равна правой, ошибочка, давай по новой, все фигня")
            continue
        else:
            return left, right


def main():
    func_index = read_int(
        "Выберите функцию: \n" + "\n".join([f'{i + 1}. {functions[i].text}' for i in range(len(functions))]) + "\n",
        1, len(functions), "Неправильный выбор, еще раз!") - 1
    left, right = read_interval()
    # x0 = read_float(f"Введите x0 начального условия [{'{:.3f}'.format(left)};{'{:.3f}'.format(right)}]: ", left, right,
    #                "Неправильно введеные данные")
    y0 = read_float(f"Введите y0 начального условия [{mn_min};{mx_max}]: ", mn_min, mx_max,
                    "Неправильно введеные данные")
    step = read_float(f"Введите шаг хода [{step_min};{step_max}]: ", step_min, step_max,
                      "Неправильно введеные данные")
    data = []
    for method in methods:
        x_array, y_array = method.func(functions[func_index], y0, step, left, right)
        data.append([x_array, y_array, method.text])
    graph(data, functions[func_index].real.subs(C, functions[func_index].const.subs(y, y0).subs(x, left)), left, right)


if __name__ == '__main__':
    main()
