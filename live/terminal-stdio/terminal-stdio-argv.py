import sys

print("\n"*8)
    
print(f"Salut à vous {' '.join(sys.argv[1:])}")



    # import asyncio
    # if sys.platform not in ('emscripten','wasi'):
    
    #     def patch_input():
    #         import builtins
    #         builtins_input = input
    #         async def async_input(prompt=""):
    #             return builtins_input(prompt)
    #         builtins.input = async_input
    
    #     patch_input()
    #     del patch_input

   
    # async def main():
    #     color = await input("\nwhat is your favorite colour ? ")
    #     print(f" {color=} ")
    
    # if __name__ == "__main__":
    #     asyncio.run(main())
