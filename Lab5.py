'''
Задана рекуррентная функция. 
Область определения функции – натуральные числа. 
Написать программу сравнительного вычисления данной функции рекурсивно и итерационно. 
Определить границы применимости рекурсивного и итерационного подхода. 
Результаты сравнительного исследования времени вычисления представить в табличной форме. 
Обязательное требование – минимизация времени выполнения и объема памяти
15.	F(0) = 1, F(1) = 1, F(n) = (-1)n*(2*F(n–1)/n! + F(n-2)), при n > 1
'''
import timeit
import math

def F_recursive(n):
    if n == 0 or n == 1:
        return 1
    sign = -1 if n % 2 else 1
    return sign * (2 * F_recursive(n - 1) / math.factorial(n) + F_recursive(n - 2))

def F_iterative(n):
    if n == 0 or n == 1:
        return 1  
    p2 = 1
    p1 = 1
    fn = 1  
    for i in range(2, n + 1):
        fn *= i
        sign = -1 if i % 2 else 1
        cur = sign * (2 * p1 / fn + p2)
        p2, p1 = p1, cur
    
    return p1
n = int(input("Введите натуральное число n: "))
res_rec = F_recursive(n)
res_it = F_iterative(n)
rec_time = timeit.timeit(lambda: F_recursive(n), number=1000)
iter_time = timeit.timeit(lambda: F_iterative(n), number=1000)
print(f"n = {n}")
print(f"Рекурсия: {res_rec}\nВремя: {rec_time}")
print(f"Итерация: {res_it}\nВремя: {iter_time}")
