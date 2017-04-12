import time
import random

import multiprocessing
from queue import Queue

from threading import Thread

from selenium.webdriver import Chrome

import smtk.utils.logger as l


def random_js_scroll():
    scroll_size = random.randrange(6000, 100000)
    return "window.scrollTo(0, %s)" % (str(scroll_size))

def random_sleep():
    sleep_sec = random.randrange(2, 10)
    time.sleep(sleep_sec)


class GoogleImageKeywordCrawler():

    def __init__(self, keyword, scroll_max = 3):
        self.keyword = keyword
        self.scroll_max = scroll_max
        self.page_source = None

    @property
    def search_url_prefix(self):
        return "https://www.google.com.sg/search?q="

    @property
    def search_url_suffix(self):
        return ''.join(['&source=lnms&tbm=isch&sa=X',
                        '&ei=0eZEVbj3IJG5uATalICQAQ&ved=0CAcQ_AUoAQ',
                        '&biw=939&bih=591'])

    def on_start(self):
        pass

    def on_entry(self, entry):
        raise RuntimeError('on_entry must be implemented')

    def on_page_source(self):
        raise RuntimeError("on_page_source must be implemented")


    def build_search_url(self):
        return ''.join([
            self.search_url_prefix,
            self.keyword,
            self.search_url_suffix])

    def update_page_source(self):
        url = self.build_search_url()

        driver = Chrome()
        driver.get(url)


        num_scrolls = 0
        try:

            while num_scrolls < self.scroll_max:
                driver.execute_script(random_js_scroll())
                self.page_source = driver.page_source
                random_sleep()
                num_scrolls+=1

        except Exception as e:
            l.WARN(e)

        driver.close()

    def crawl_keyword(self):
        self.update_page_source()
        self.on_page_source()

    def crawl(self):
        self.on_start()
        self.crawl_keyword()


class GoogleImageCrawler():

    def __init__(self, task_cls, queue_data, **kwargs):
        self.task_cls = task_cls
        self.queue_data = queue_data
        self.queue = Queue()
        self.__dict__.update(kwargs)

    @property
    def num_cpus(self):
        return multiprocessing.cpu_count()

    def enqueue(self):
        for obj in self.queue_data:
            self.queue.put(obj)

    def worker(self):
        while not self.queue.empty():
            try:
                keyword = self.queue.get()

                (
                    self.task_cls(keyword=keyword,
                                  scroll_max=self.__dict__['scroll_max'])
                    .crawl()
                )

                self.queue.task_done()
            except Exception as e:
                l.ERROR(e)
                break

    def start(self):
        self.enqueue()

        for _ in range(self.num_cpus):
            t = Thread(target=self.worker)
            t.deamon = True
            t.start()

        self.queue.join()


