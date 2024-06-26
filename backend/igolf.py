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


class igolf:
    def get_par(self):
        self.driver = init_browser()
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, timeout=5)
        table = self.driver.find_elements(By.CSS_SELECTOR, ".sheet table")[0]
        tr = table.find_elements(By.TAG_NAME, "tr")
        td = tr[3].find_elements(By.TAG_NAME, "td")
        par = []
        for t in td:
            par.append(int(t.get_attribute("innerText")))

        par.pop(9)
        par.pop(18)
        return par

    def get_scores(self):
        self.driver = init_browser()
        # self.driver.set_window_size(950, 800)
        self.driver.get(self.url)
        WebDriverWait(self.driver, timeout=5)
        self.driver.get(self.url.replace("#/landscape-a", "/leaderboard"))
        WebDriverWait(self.driver, timeout=5)
        show_score_button = self.driver.find_elements(
            By.CSS_SELECTOR, ".show-score")
        show_score_button[0].click()
        WebDriverWait(self.driver, timeout=5)
        table = self.driver.find_elements(By.CSS_SELECTOR, ".ui-table-view")[0]

        basic_info = self.get_basic_info()
        par = self.get_par()

        tr = table.find_elements(By.TAG_NAME, "tr")
        num_player = len(tr)-2

        scores = {
            "course": basic_info["course"],
            "date": basic_info["date"],
            "par": sum(par),
            "scores": []
        }

        for i in range(0, num_player):
            tds = tr[i+2].find_elements(By.TAG_NAME, "td")
            score = []
            for td in tds:
                score.append(td.get_attribute(
                    "innerText").replace('\u3000', '').replace(' ', ''))
            score.pop(0)
            del score[1:6]
            score.pop(10)
            score.pop(10)
            score.pop(19)

            data = {
                "name": "",
                "score": []
            }
            name = ""

            for i, s in enumerate(score):
                if i == 0:
                    data["name"] = score[i]
                if i > 0 and i < 19:
                    data["score"].append({
                        "hole": i,
                        "score": int(score[i]),
                        "prize": prize(par[i-1], int(score[i]))
                    })
                if i == 19:
                    data["gross"] = int(score[i])

            scores["scores"].append(data)
        self.driver.quit()
        scores = self.after_filter(scores)
        return scores

    def get_basic_info(self):
        self.driver = init_browser()
        self.driver.get(self.url)
        WebDriverWait(self.driver, timeout=5)
        course = self.driver.find_elements(By.CSS_SELECTOR, ".cc-name")[
            0].get_attribute("innerText")
        import re
        course = re.sub("^【", "", course)
        course = re.sub("】$", "", course)

        date = self.driver.find_elements(By.CSS_SELECTOR, ".date")[
            0].get_attribute("innerText")

        # from dateutil.parser import parse
        from datetime import datetime
        date = datetime.strptime(date.replace(
            "プレー日: ", ""), "%Y年%m月%d日").strftime("%Y/%m/%d")

        import dateutil.parser
        date = dateutil.parser.parse(date)
        return {
            "course": course,
            "date": date,
        }
