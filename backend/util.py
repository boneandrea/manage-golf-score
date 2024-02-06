from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def prize(par, score):
    if score == 1:
        return "HOLEINONE"
    diff = score-par
    match diff:
        case -3:
            return "ALBATROSS"
        case -2:
            return "EAGLE"
        case -1:
            return "BIRDIE"
        case 0:
            return "PAR"
        case 1:
            return "BOGEY"
        case 2:
            return "DOUBLEBOGEY"
        case 3:
            return "TRIPLEBOGEY"
        case _:
            return ""


def init_browser():
    options = webdriver.chrome.options.Options()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)
