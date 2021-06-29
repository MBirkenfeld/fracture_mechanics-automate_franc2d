import subprocess
import numpy as np
import pyautogui
import time

# PIL has to be installed for picture recognition

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


def click_button(rank):
    point_x = 1426
    point_y0 = 40
    space = 50
    pyautogui.click(point_x, point_y0 + rank * space)


def click_num(num):
    click_button(0)
    pyautogui.click()
    pyautogui.typewrite(str(num))
    pyautogui.press('enter')


def start_franc():
    # centering mouse on screen, so franc2d Window opens in right spot:
    x, y = pyautogui.size()
    pyautogui.moveTo(x/2, y/2)

    # opening franc2d:
    subprocess.Popen(["C:\\MS64\\franc2d.exe"])
    time.sleep(1)

    # entering RAM-size for franc2d:
    pyautogui.press('tab')
    pyautogui.typewrite('4000')
    pyautogui.press('tab')
    pyautogui.typewrite('4000')
    pyautogui.press('tab', 3)
    pyautogui.press('enter')
    time.sleep(2)

    # importing file:
    # choosing file path to pre defined model with mesh and loading
    # (this may will vary depending on your file structure)
    # try locating the correct position to click with pyautogui.position():

    pyautogui.click(x=981, y=347)
    pyautogui.moveTo(x=870, y=375)
    pyautogui.hscroll(200)
    time.sleep(1)
    pyautogui.click()
    pyautogui.doubleClick(x=655, y=588)
    time.sleep(1)
    pyautogui.doubleClick(x=676, y=563)
    time.sleep(1)


def analyse():
    click_button(2)
    click_button(0)
    click_button(0)
    time.sleep(12)
    click_button(18)


def get_sif(suffix='_', name=0):
    click_button(3)
    click_button(1)
    click_button(2)

    # you will probably have to change these coordinates:
    pyautogui.click(x=1485, y=168)

    pyautogui.press('tab', 12)
    pyautogui.write(str(suffix) + str(int(round(name, 0))) + '_result')
    pyautogui.press(['tab', 'enter', 'enter'])

    # you will probably have to change these coordinates:
    pyautogui.click(x=1598, y=112)

    click_button(18)
    click_button(18)


def close_franc():
    click_button(18)
    click_button(17)


class Crack:
    def __init__(self, x, y, a, alpha=0):
        self.x = x
        self.y = y
        self.a = a
        self.alpha = alpha / 360 * 2 * np.pi

    def make_crack(self, crack_acc=10):
        click_button(1)
        click_button(3)
        click_button(0)
        click_button(1)

        click_num(self.x)
        click_num(self.y)
        pyautogui.click()

        # defining actual cracks:
        click_num(self.x + 2 * self.a * np.cos(self.alpha))
        click_num(self.y + 2 * self.a * np.sin(self.alpha))

        click_num(crack_acc)
        time.sleep(2)
        pyautogui.click()
        click_button(18)
        time.sleep(2)


'''
# example: script execution of a single rotated crack:
crack_rotated = Crack(100, 100, 10, alpha=40)
start_franc()
crack_rotated.make_crack(crack_acc=15)
analyse()
get_sif(suffix='rotated', name=1)
close_franc()
'''

# script execution for my actual cracks:
# here you define your parameters:
# number of steps:
n = 20

# crack length:
a = 10

# max distance:
dist_max = 50

# min distance:
dist_min = 1


for del_y in np.linspace(dist_max, dist_min, n):

    crack_left = Crack(100 - (2 * a), 100 - del_y/2, a)
    crack_right = Crack(100, 100 + del_y/2, a)

    start_franc()
    crack_left.make_crack(crack_acc=15)
    crack_right.make_crack(crack_acc=15)
    analyse()
    get_sif('del_y_', del_y)
    close_franc()
