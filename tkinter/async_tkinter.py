import tkinter as tk
import asyncio

"""
버튼 눌렀을 때 async function 수행하는 예시
"""

class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())
        await self.window.show()

class Window(tk.Tk):
    def __init__(self, loop):
        # super().__init__()
        self.loop = loop
        self.root = tk.Tk()
        initial_width = 500
        initial_height = 300
        self.root.geometry(f"{initial_width}x{initial_height}")
        bt_test1 = tk.Button(text="async 테스트", command=lambda: self.loop.create_task(self.async_function_test()))
        bt_test1.pack()

    async def show(self):
        while True:
            self.root.update()
            await asyncio.sleep(.1)

    async def async_function_test(self):
        print("프린트1")
        await asyncio.sleep(3)
        print("프린트2")

asyncio.run(App().exec())
