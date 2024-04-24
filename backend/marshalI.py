from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from datetime import date, datetime
from time import sleep
import pytest
import json
import os
import sys
import re
from database import *
from util import *
from base_score import *
"""
Run:

$ pip install -r requirements.e2e.txt
$ pytest -sv test.py # print()あり テスト項目表示あり
$ pytest -v test.py # print()なし テスト項目表示あり
$ pytest test.py # silent
"""


class marshalI(base_score):
    def init_browser(self):
        global driver
        options = webdriver.chrome.options.Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)

    def get_par(self, table):
        tr = table.find_elements(By.CSS_SELECTOR, "thead tr")[1]
        th = tr.find_elements(By.TAG_NAME, "th")
        return list(map(lambda e: int(e.get_attribute("innerText")), th))

    def get_scores(self):
        self.init_browser()
        driver.get(self.url)
        wait = WebDriverWait(driver, timeout=5)
        table = driver.find_element(
            By.CSS_SELECTOR, "table.holebyholeTable")
        tr = table.find_elements(By.CSS_SELECTOR, "tbody tr")

        d = driver.find_element(
            By.CSS_SELECTOR, ".panel-heading").get_attribute("innerText")
        m = re.match(r'((.|\s)*)プレー日：((.|\s)*)', d)
        course = m[1].strip()
        date = m[3].strip()
        par = self.get_par(table)
        from datetime import datetime
        import dateutil.parser
        date = datetime.strptime(date, "%Y年%m月%d日").strftime("%Y/%m/%d")
        date = dateutil.parser.parse(date)

        results = {
            "course": course,
            "date": date,
            "par": sum(par),
            "scores": []
        }
        num_player = len(tr)-1

        for i in range(0, num_player):
            name = tr[i].find_elements(By.TAG_NAME, "td")[
                1].get_attribute("innerText").replace('\u3000', '')
            td = tr[i].find_elements(By.TAG_NAME, "td")
            score = []
            for j in range(0, 20):
                score.append(
                    td[3+j].find_element(By.TAG_NAME, "span").get_attribute("data-par"))

            score.pop(9)
            score.pop(18)

            scores = {
                "name": name,
                "score": [],
                "gross": 0
            }
            for i, s in enumerate(score):
                if s == "":
                    continue
                sss = int(score[i])+int(par[i])
                ss = {
                    "hole": i+1,
                    "score": sss,
                    "prize": prize(par[i], int(sss))
                }
                scores["score"].append(ss)
                scores["gross"] += sss

            results["scores"].append(scores)

        driver.quit()
        results = self.after_filter(results)
        return results
