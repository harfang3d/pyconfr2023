
import asyncio
import sys

# required for nurses_2
import wcwidth, termios, numpy, cv2

if sys.platform in ('emscripten','wasi'):
    import aio.fetch
    import termios
    termios.set_raw_mode()

    # http://localhost:8000/live/tetris
    aio.fetch.FS("""
http://localhost:8000/live
├── color_scheme.py
├── __init__.py
├── loudypixelsky.png
├── __main__.py
├── matrix.py
├── modal_screen.py
├── piece.py
├── tetris.py
├── tetrominoes.py
└── wall_kicks.py
""", "tetris")

sys.path.append(".")

async def main():

    # copy from web
    if sys.platform in ('emscripten','wasi'):
        await aio.fetch.preload_fetch()

    import nurses_2
    import tetris.__main__

    while True:
        await asyncio.sleep(0.016)


asyncio.run(main())


