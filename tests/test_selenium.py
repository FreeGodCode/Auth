# -*- coding: utf-8  -*-
# @Author: ty
# @File name: tests.py 
# @IDE: PyCharm
# @Create time: 12/20/20 10:13 PM
import re
import threading
import unittest
from selenium import webdriver
from app import create_app, db


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls) -> None:
        # 启动浏览器
        try:
            cls.client = webdriver.Chrome()
        except:
            pass
        if cls.client:
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()
            db.create_all()
            threading.Thread(target=cls.app.run().start())

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.client:
            cls.client.get('http://127.0.0.1:5000/shutdown')
            cls.client.close()
            db.drop_all()
            db.session.remove()
            cls.app_context.pop()

    def setUp(self) -> None:
        if not self.client:
            self.skipTest('chrome is invailable')

    def tearDown(self) -> None:
        pass

    def test_home_page(self):
        self.client.get('http://127.0.0.1:5000/')
        self.assertTrue(re.search('Home', self.client.page_source))
