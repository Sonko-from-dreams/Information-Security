from math import pow, pi, sqrt

# Коефіцієнти для варіанту №1
m = pow(2, 11)-1
a = pow(3, 5)
c = 1
x_0 = 4

#  функція для обчислення найбільшого спільного дільника двох цілих чисел
#  за допомогою алгоритму Евкліда
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# функція для генерації послідовності пвч
# визначеної довжини n
def generate_rand_num (n, m = m, a = a, c = c, x0 = x_0) :
    xi = x_0
    random_num = []

    for i in range(n):
        xn = int((int(a) * xi + c) % m)
        random_num.append(xn)
        xi = xn

    return random_num

# Аналіз генерації чисел за допомогою теореми Ернеста Чезаро
def analyze (n, rand_num) :
    is_gcd_1 = 0

    for i in range(1, n):
        if gcd(rand_num[i-1], rand_num[i]) == 1:
            is_gcd_1 += 1

    found_pi = sqrt(6*n/is_gcd_1)
    error = abs(found_pi - pi)

    return found_pi, error

# Знаходження періоду
def get_period() :
    xi = x_0
    period = 1
    found = False

    while not found:
        xn = int((int(a) * xi + c) % m)
        xi = xn
        if xn != x_0 and found == False:
            period += 1
        else:
            found = True

    return period