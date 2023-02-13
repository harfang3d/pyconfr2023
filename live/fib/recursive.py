
import sys
import time

"""
recursive-nocache
35 : 5.1
36 : 8.7
37 : 13.8

"""


if 1:
    unsafe = 1
    def fibonacci_of(n):
        if n in {0, 1}:  # Base case
            return n
        return fibonacci_of(n - 1) + fibonacci_of(n - 2)  # Recursive case


if 0:
    unsafe = 0

    cache = {0: 0, 1: 1}

    def fibonacci_of(n):
        global cache

        if n in cache:  # déja calculé !
            return cache[n]
        # calcule et renvoie le nombre de Fibonacci
        cache[n] = fibonacci_of(n - 1) + fibonacci_of(n - 2)  # Recursive case
        return cache[n]





try:
    value = int(sys.argv[-1])
except:
    value = 450_000

if unsafe and value>34:
    value = 34


sys.set_int_max_str_digits(0)

def main():

    time_start = time.time()
    print("Calcul pour :", value)

    resultat = 0

    for tmp in range(value+1):
        resultat = fibonacci_of(tmp)

    print(f"fib(0..{tmp}), {len(str(resultat))} digits" )
    print("écoulé:", time.time() - time_start )



main()
