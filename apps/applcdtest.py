"""MicroHydra App LCD Test.

Version: 1.0


This is a basic skeleton for a MicroHydra app, to get you started.

There is no specific requirement in the way a MicroHydra app must be organized or styled.
The choices made here are based entirely on my own preferences and stylistic whims;
please change anything you'd like to suit your needs
(or ignore this template entirely if you'd rather)

This template is not intended to enforce a specific style, or to give guidelines on best practices,
it is just intended to provide an easy starting point for learners,
or provide a quick start for anyone that just wants to whip something up.

Have fun!

TODO: replace the above description with your own!
"""
import random
import time
from lib import display, userinput
from lib.hydra import config, loader

# 初始化显示对象
DISPLAY = display.Display()
CONFIG = config.Config()
# object for reading keypresses (or other user input)
INPUT = userinput.UserInput()
def main_loop():    
    print("Starting display test app...")
    while True:
        # get list of newly pressed keys
        keys = INPUT.get_new_keys()

        if "ESC" in keys:  # ESC arrow
        # 使用系统的 loader 返回 launcher
            from lib.hydra import loader
            _LAUNCHER = const("/launcher/launcher")
            app = _LAUNCHER
            #launch_app('launcher') # 注意这里没有 .py
            loader.launch_app(_LAUNCHER)
    
        # 随机位置和颜色
        x = random.randint(0, 320 - 40)
        y = random.randint(0, 172 - 40)
        color = random.randint(0, 0xFFFF)
        
        # 绘制方块
        DISPLAY.fill_rect(x, y, 40, 40, color)
        
        # 写入显示
        DISPLAY.show()
        
        time.sleep_ms(100)

main_loop()