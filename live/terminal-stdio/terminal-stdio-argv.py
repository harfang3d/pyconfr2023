#!python

import asyncio
import sys

if sys.platform not in ('emscripten','wasi'):

    def patch_input():
        import builtins
        builtins_input = input
        async def async_input(prompt=""):
            return builtins_input(prompt)
        builtins.input = async_input

    patch_input()
    del patch_input


async def main():
    
    print("\n"*8)
    
    with open("/data/data/org.python/assets/cpython.six","r") as f:
        print(f.read())
        
       
    print(f"Salut à vous {' '.join(sys.argv[1:])}")
    
    
    color = await input("\nwhat is your favorite colour ? ")
    print(f"\n\n {color=} \n\n")

if __name__ == "__main__":
    asyncio.run(main())
