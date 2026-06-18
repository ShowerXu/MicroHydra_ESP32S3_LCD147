import machine
import gc
import esp
import time
from machine import Pin

# ==========================================
# 1. 读取并打印内存与 Flash 硬件信息
# ==========================================
print("-" * 40)
print("🚀 ESP32-S3 MicroPython 固件运行成功！")
print("-" * 40)

# 读取并计算 RAM 大小
# gc.mem_free() 是当前可用 RAM，gc.mem_alloc() 是已用 RAM
total_ram = (gc.mem_free() + gc.mem_alloc()) / 1024
print(f"内存 (RAM) 总大小: {total_ram:.2f} KB")
print(f"当前剩余可用 RAM: {gc.mem_free() / 1024:.2f} KB")

# 读取并计算外部 Flash 大小
try:
    # esp.flash_size() 返回的是字节数(Bytes)
    flash_bytes = esp.flash_size()
    flash_mb = flash_bytes / (1024 * 1024)
    print(f"外挂 Flash 芯片大小: {flash_mb:.2f} MB ({flash_bytes} 字节)")
except Exception as e:
    print("读取 Flash 大小失败，请检查 SPI 引脚宏定义配置。")

print("-" * 40)

# ==========================================
# 2. GPIO 12 和 13 脚 LED 流水灯控制
# ==========================================
print("💡 正在启动 GPIO 12 & 13 流水灯测试...")

# 初始化引脚为输出模式
led1 = Pin(12, Pin.OUT)
led2 = Pin(13, Pin.OUT)

# 先让两个灯都熄灭
led1.value(0)
led2.value(0)

# 循环跑流水灯 20 次
for i in range(20):
    # 灯 1 亮，灯 2 灭
    led1.value(1)
    led2.value(0)
    time.sleep_ms(300) # 延时 300 毫秒
    
    # 灯 1 灭，灯 2 亮
    led1.value(0)
    led2.value(1)
    time.sleep_ms(300)

# 测试结束，熄灭所有 LED
led1.value(0)
led2.value(0)
print("🏁 测试完成！你的自定义引脚固件完美工作！")
print("-" * 40)