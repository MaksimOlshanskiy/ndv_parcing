import hashlib
import random
import time
from functools import wraps
from queue import Empty
import string
from subprocess import PIPE, run
import json
import httpx

from curl_cffi import requests
from curl_cffi.curl import lib, ffi
from billiard import current_process
from celery import current_app as app
from celery.worker.control import revoke
from celery.utils.log import get_task_logger
from urllib3 import connectionpool, poolmanager
from urllib3.util import connection

from services.redirect import fast_connect, get_hostname
from services.tools import search_cookies
from services.pw_class import PlaywrightDriverManager
from worker_utils.redirect import Redirect

def get_cookies():
    """
    Декоратор для получения cookies
    """

    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):
            global all_cookies
            cookies = all_cookies.get("cookies", None)
            LIST_COOKIES = [
                "_ym_d",
                "_ym_uid",
                "PHPSESSID",
            ]

            if cookies is None:
                cookies = {}

                try:
                    try:
                        proxy_list = connect_manager.get_proxy()
                        driver_manager = PlaywrightDriverManager(proxy_list)
                        page = driver_manager.create_driver()
                    except Exception as e:
                        logger.error(e)

                    if not page:
                        raise Exception("Не удалось создать драйвер Playwright")

                    page.goto(url="https://dixy.ru/", wait_until="domcontentloaded")

                    if not search_cookies(page, 20, LIST_COOKIES):
                        logger.error("Куки не найдены для выполнения запросов")
                        self.retry(countdown=10, kwargs=kwargs)

                    time.sleep(random.uniform(1, 2))

                    requests_cookies = {}

                    playwright_cookies = driver_manager.get_cookies()

                    for cookie in playwright_cookies:
                        name = cookie.get("name")
                        value = cookie.get("value")

                        if name and value is not None:
                            requests_cookies[name] = value

                    all_cookies["cookies"] = requests_cookies

                except Exception as e:
                    if kwargs.get("cookies", None):
                        del kwargs["cookies"]
                    if all_cookies.get("cookies", None):
                        del all_cookies["cookies"]
                    self.retry(countdown=1, kwargs=kwargs)

                finally:
                    driver_manager.close_driver()

            else:
                kwargs["cookies"] = all_cookies["cookies"]

            return func(self, *args, **kwargs)

        return function

    return decorator_func