

import asyncio
import sys
import time



import builtins

try:
    import aio
except:
    aio = None


sys.set_int_max_str_digits(0)


cache = {0: 0, 1: 1}

async def fibonacci_of(n):
    global cache

    if n in cache:  # déja calculé !
        return cache[n]

    if aio:
        if aio.delta()>0.010:await asyncio.sleep(0)

    # calcule et renvoie le nombre de Fibonacci
    cache[n] = await fibonacci_of(n - 1) + await fibonacci_of(n - 2)  # Recursive case
    return cache[n]


async def main():
    unsafe = 0

    try:
        value = int(sys.argv[-1])
    except:
        value = 210_000

    if unsafe and value>34:
        value = 34

    time_start = time.time()
    print("Calcul pour :", value)

    resultat = 0

    for x in range(5):
        for tmp in range(value+1):
            resultat = await fibonacci_of(tmp)


    print(f"fib(0..{tmp}), {len(str(resultat))} digits" )
    print("écoulé:", time.time() - time_start )




asyncio.run(main())

