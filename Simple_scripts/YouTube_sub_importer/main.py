import xmltodict
import json
import xml.etree.ElementTree as ET
import pyautogui  # its use for keyboard inputs.
import time  # use for add delay in between inputs.
import subprocess  # to run the cmd command.
import re


def check():
    tree = ET.parse("subscription_manager.xml")
    tree2 = ET.parse("subscription_manager_maciek.xml")
    root = tree.getroot()
    root2 = tree2.getroot()

    aima = []
    mac = []
    roznica = []

    for child in root:
        for c2 in child:
            for c3 in c2:
                for item in c3.items():
                    if item[0] == "xmlUrl":
                        aima.append(re.findall('(?<==).*$', item[1])[0])
    for child in root2:
        for c2 in child:
            for c3 in c2:
                for item in c3.items():
                    if item[0] == "xmlUrl":
                        mac.append(re.findall('(?<==).*$', item[1])[0])

    for i in range(len(aima)):
        if aima[i] not in mac:
            roznica.append(aima[i])
            print(aima[i])
            # subBot(aima[i])

    print(len(roznica))


def subBot(chan_url):
    subButton = 'var SubForLogin = document.getElementsByClassName("style-scope ytd-subscribe-button-renderer");'
    # var SubForLogin = document.getElementsByClassName("style-scope ytd-button-renderer style-destructive size-default");
    subButtonClick = "SubForLogin[0].click();"
    # channel url

    url = chan_url
    # store command code list in order to perform.

    listOfBrowser = 'start Opera https://www.youtube.com/channel/' + url

    # next we have to store key to open console in list.s

    listOfCommand = ['j', 'i']

    # now perform command operation over cmd

    process = subprocess.Popen(
        listOfBrowser, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)\

    time.sleep(2)

    process.communicate()
    time.sleep(2)

    pyautogui.hotkey(
        'ctrl', 'shift', listOfCommand[1])

    time.sleep(2)

    pyautogui.typewrite(subButton)

    pyautogui.press('enter')
    time.sleep(1)

    pyautogui.typewrite(subButtonClick)

    pyautogui.press('enter')
    time.sleep(2)

    pyautogui.hotkey('ctrl', 'w')


if __name__ == "__main__":
    # importer()
    check()
