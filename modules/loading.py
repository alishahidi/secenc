import os
import time
import base64
import hashlib
import datetime
import random
from modules import cryptContent
import sys

packageLoad = True

try:
    from termcolor import colored
except:
    print("System error")
    print("Pleas install termcolor package (pip3 install termcolor)")
    packageLoad = False

try:
    from Crypto.Cipher import AES
    from Crypto import Random
except:
    print("System error")
    print("Pleas install pycryptodome package (pip3 install pycryptodome)")
    packageLoad = False

try:
    from key_generator.key_generator import generate
except:
    print("System error ")
    print("Pleas install key_generator package (pip3 install key_generator)")
    packageLoad = False

try:
    import jwt
except:
    print("System error ")
    print("Pleas install pyjwt package (pip3 install pyjwt)")
    packageLoad = False

try:
    import cv2
except:
    print("System error ")
    print("Pleas install opencv-python package (pip3 install opencv-python)")
    packageLoad = False

try:
    import numpy as np
except:
    print("System error ")
    print("Pleas install numpy package (pip3 install numpy)")
    packageLoad = False

try:
    from PIL import Image
except:
    print("System error ")
    print("Pleas install Pillow package (pip3 install Pillow)")
    packageLoad = False

if packageLoad == False:
    sys.exit()

colors = ("yellow", "blue", "red", "magenta", "cyan", "green")

def coloredBold(text, color):
    if color in colors:
       return colored(text, color = color, attrs = ["bold"])
    else:
        raise ValueError("color is not in exists color list")

def banner():
    with open(os.path.realpath("modules/banner"), "r") as banner:
        bannerText = banner.read()
    print(coloredBold("\n" + bannerText + "\n", "red"))

def loading():
    if os.name == "nt":
            print("Loading......")
            time.sleep(1)
            os.system("cls")
    elif os.name == "posix":
            print("Loading......")
            time.sleep(1)
            os.system("clear")
    banner()

def inputPlus(inputText):
    inputValue = input(f"{colored('[', 'red')}{inputText}{colored(']', 'red')}$ ")
    print("\n")
    return inputValue



def menu_creator(menuItems):
    menuContent = []
    count = 0
    for item in menuItems:
        content = f"{colored('[', 'red')}{count}{colored(']', 'red')} {colored(item, 'green', attrs = ['bold'])}"
        menuContent.append(content)
        count+=1
    return menuContent

def main_menu():
    print("\n")
    menus = menu_creator(["exit","encrypt", "decrypt"])
    for item in menus:
        print (item)
        time.sleep(.2)
    print("\n")

def check_dir():
    if os.path.exists("Temp") is not True:
        os.makedirs("Temp")
    if os.path.exists("result") is not True:
        os.makedirs("result")

def check_file():
    if not os.path.exists('message.txt'):
        with open('message.txt', 'w') as file:
            file.write("Type your message here.")

def delete_temp():
    if os.path.exists("Temp"):
        filesList = os.listdir("Temp")
        numReq = 0
        for file in filesList:
            path = f"Temp/{file}"
            if os.path.exists(path):
                os.remove(path)
                numReq = numReq + 1
    else:
        os.makedirs("Temp")

def run():
    check_dir()
    check_file()
    main_menu()
    state = inputPlus("Select option")
    if state == "0":
        return False
    elif state == "1":
        inputPlus("Type and save your message in message.txt file (enter if done)")
        exp = int(inputPlus("Activity time (minute)"))
        outname = inputPlus("Enter image outname")
        cryptContent.encrypt_message( exp, outname)
        delete_temp()
    elif state == "2":
        img = inputPlus("imagePath")
        key = inputPlus("key")
        cryptContent.decrypt_message(img, key)