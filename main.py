import os, gc, time, machine
from machine import UART, Pin, I2C, ADC, freq
import ssd1306
import cube3d
import time
import math

from button import Button
from menu import MenuSystem, MenuPage, MenuItem
from icon import Icon
from wifi import Wifi

SSID = "PiedPiper"
PASSWORD = "ErlichBachmanIsAFat"

# --- Setup Display ---
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400_000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
# --- Boot Logo ---
logo = Icon("logo")  # 32x32
oled.fill(0)
text = "Booting"
x = (128 - len(text) * 8) // 2
y = 64 - 8
oled.text(text, x, y)
oled.blit(logo.fb, 64 - 16, 32 - 16)
oled.show()
# --- Start Wifi ---
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
wifi = Wifi(uart)
# --- Setup Buttons ---
btn_select = Button(12, "SELECT")
btn_back = Button(13, "BACK")
btn_down = Button(14, "DOWN")
btn_up = Button(15, "UP")
buttons = [btn_select, btn_back, btn_down, btn_up]

# --- Define Actions (Callbacks) ---
def reboot():
    oled.fill(0)
    text = "Restarting..."
    x = (128 - len(text) * 8) // 2
    oled.text(text , x, 32)
    oled.show()
    machine.reset()

def cube():
    FPS = 60
    dt = 1 / FPS
    angle = 0.0
    dz = 1.2
    dz_dir = 1

    last = time.ticks_ms()
    fps = 0

    go_back = True
    while go_back:
        if btn_back.is_pressed():
            go_back = False
            menu.draw()
            continue

        start = time.ticks_ms()

        angle += math.pi * dt
        dz += dz_dir * dt
        if dz > 1.25 or dz < 0.5:
            dz_dir *= -1

        oled.fill(0)

        cube3d.draw_cube(oled, angle, dz)

        now = time.ticks_ms()
        frame_ms = time.ticks_diff(now, last)
        last = now
        if frame_ms > 0:
            fps = int(1000 / frame_ms)

        oled.text("FPS:%d" % fps, 0, 0)
        oled.text("<-Back", 0, 56)

        oled.show()

        sleep_ms = int(max(0, (dt * 1000) - time.ticks_diff(time.ticks_ms(), start)))
        time.sleep_ms(sleep_ms)


def connect_wifi():
    oled.fill(0)
    oled.text("Initializing...", 0, 0)
    oled.show()
    if wifi.connected_ip:
        oled.fill(0)
        oled.text("IP:", 0, 0)
        oled.text(wifi.connected_ip, 0, 15)
    else:
        oled.fill(0)
        oled.text("Connecting...", 0, 0)
        oled.show()
        wifi.connect(SSID, PASSWORD)
        oled.fill(0)
        oled.text("IP:", 0, 0)
        oled.text(wifi.connected_ip, 0, 15)
    oled.text("<-Back", 0, 64 - 8)
    oled.show()
    go_back = True
    while go_back:
        if btn_back.is_pressed():
            go_back = False
            menu.back()


def scan_wifi():
    oled.fill(0)
    oled.text("Scanning...", 0, 0)
    oled.show()
    networks = wifi.scan()
    oled.fill(0)
    for i, n in enumerate(networks):
        oled.text(n, 0, i * 8)
    oled.text("<-Back", 0, 64 - 8)
    oled.show()
    go_back = True
    while go_back:
        if btn_back.is_pressed():
            go_back = False
            menu.back()


def system_info():
    oled.fill(0)
    u = os.uname()
    gc.collect()
    # Board
    oled.text(u.machine, 0, 8)
    # Memory
    oled.text(f"Free: {gc.mem_free()//1024}KB", 0, 16)
    # CPU
    oled.text(f"CPU: {freq()//1_000_000}MHz", 0, 24)

    # Temperature
    adc = ADC(4)
    v = adc.read_u16() * 3.3 / 65535
    temp = int(27 - (v - 0.706) / 0.001721)
    oled.text(f"Temp: {temp}C", 0, 32)
    # Uptime
    oled.text(f"Up: {time.ticks_ms()//1000}s", 0, 40)
    oled.text("<-Back", 0, 64 - 8)
    oled.show()
    go_back = True
    while go_back:
        if btn_back.is_pressed():
            go_back = False
            menu.draw()


# --- Build the Menu Tree ---
wifi_items = [
    MenuItem("Scan", action=scan_wifi, icon_name="wifi"),
    MenuItem("Connect", action=connect_wifi, icon_name="up"),
]
wifi_page = MenuPage("WiFi", wifi_items)

# 1. Create a Submenu first
settings_items = [MenuItem("WiFi", submenu=wifi_page, icon_name="wifi")]
settings_page = MenuPage("Settings", settings_items)

# 2. Create Main Menu
main_items = [
    MenuItem("3D Cube", action=cube, icon_name="cube"),
    MenuItem("Settings", submenu=settings_page, icon_name="settings"),
    MenuItem("Sys Info", action=system_info, icon_name="info"),
    MenuItem("Restart", action=reboot, icon_name="reboot"),
]
root_page = MenuPage("Main Menu", main_items)

# --- Initialize System ---
menu = MenuSystem(oled)
menu.set_root_page(root_page)

# --- Main Loop ---
while True:
    # Check buttons
    if btn_up.is_pressed():
        menu.navigate_up()

    if btn_down.is_pressed():
        menu.navigate_down()

    if btn_select.is_pressed():
        menu.select()

    if btn_back.is_pressed():
        menu.back()

    time.sleep(0.01)  # Short delay to prevent CPU hogging

