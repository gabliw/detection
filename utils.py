"""
HShake (https://github.com/gabliw)
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests

import os
import time
import csv
import datetime as dt
import shutil
import json


def tumblr_crawling(url):
    NotImplemented


def csv_loader(csv_dir):
    result = []
    with open(f'../Dataset/Raw_source/{csv_dir}', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            result.append(row[0])
    return result


def instagram_url_crawling(url_list):
    save_dir = '../Dataset/not_refine'
    options = webdriver.ChromeOptions()
    mobile_emulation = {
        "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19"
                     " (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome("/Users/noble/workspace/NaNet/Dataset/chromedriver", chrome_options=options)
    driver.implicitly_wait(5)

    img_list = []
    for i, target in enumerate(url_list):
        driver_dir = target
        driver.get(driver_dir)

        soup = BeautifulSoup(driver.page_source, 'html5lib')
        img = soup.select("img")
        print(f"URL: {target}")

        srcset = img[1].attrs['src']
        img_list.append(srcset)

    src_list = list(set(img_list))
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                 " Chrome/77.0.3865.120 Safari/537.36"
    session = requests.Session()
    session.headers.update({'User-agent': user_agent, 'referer': None})

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    for file_name, image_url in zip(url_list, src_list):
        path = f"{save_dir}/ {file_name.split('/')[-2]}.png"

        try:
            r = session.get(image_url, stream=True)
            if r.status_code != 200:
                raise Exception

            with open(path, 'wb') as f:
                f.write(r.raw.read())
                print(f"save completed : {path}")
        except:
            print(f"failed in {path}")
            continue


def instagram_unknown_crawling(target_keywords, isfeed):
    tnum = 0
    for num, target in enumerate(target_keywords):
        save_dir = '../Dataset/not_refine'
        options = webdriver.ChromeOptions()
        mobile_emulation = {
            "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19"
                         " (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        driver = webdriver.Chrome("/Users/noble/workspace/NaNet/Dataset/chromedriver", chrome_options=options)
        driver.implicitly_wait(5)

        if isfeed is True:
            driver_dir = f"https://www.instagram.com/{target}/feed"
            driver.get(driver_dir)
        else:
            driver_dir = f"https://www.instagram.com/explore/tags/{target}"
            driver.get(driver_dir)
        time.sleep(3)

        img_list = []
        time_count = 0
        exit_count = 0
        exit_point = 0
        previous_state = False
        while True:
            soup = BeautifulSoup(driver.page_source, 'html5lib')
            img = soup.select("img[srcset]")
            img_list += img
            img_list = list(set(img_list))
            time_count += 1
            if time_count == 50 and len(img_list) == 0:
                break
            if previous_state is False and len(img_list) != 0:
                previous_state = True
                exit_point = len(img_list)
            if exit_count == 50:
                break
            if exit_point == len(img_list):
                exit_count += 1
            else:
                exit_point = len(img_list)
                exit_count = 0
            print(f"[{target}]keyword, {time_count + 1} page: {len(img)} collect, {len(img_list)} collected, "
                  f"{driver_dir}")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        src_list = []
        for t in img_list:
            srcset = t.attrs['srcset']
            srcset_list = srcset.split(",")
            item = srcset_list[len(srcset_list) - 1]
            url = item[:item.find(" ")]
            src_list.append(url)

        src_list = list(set(src_list))
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                     " Chrome/77.0.3865.120 Safari/537.36"
        session = requests.Session()
        session.headers.update({'User-agent': user_agent, 'referer': None})

        count = 0
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        for image_url in src_list:
            count += 1
            path = f"{save_dir}/ {tnum + count}.png"

            try:
                r = session.get(image_url, stream=True)
                if r.status_code != 200:
                    raise Exception

                with open(path, 'wb') as f:
                    f.write(r.raw.read())
                    print(f"save completed : {path}")
            except:
                print(f"failed in {path}")
                continue

        tnum += count


# image file rename function
def rename(target_dir):
    from shutil import copy
    files = sorted([os.path.join(target_dir, file) for file in os.listdir(target_dir)])

    for idx, file in enumerate(files[1:]):
        file_name = f"{idx + 1:03d}.png"
        print(file_name)
        copy(file, os.path.join('../Dataset/target', file_name))


# Contributed with Winterchild
class _Dict(dict):

    def __init__(self, *args, **kwargs):
        super(_Dict, self).__init__(*args, **kwargs)
        for k, v in self.items():
            if type(v) is dict:
                self[k] = _Dict(v)

    def __getattr__(self, key):
        def __proxy__(_dict, key):
            for k, v in _dict.items():
                if k == key:
                    return v
                if isinstance(v, _Dict):
                    ret = __proxy__(v, key)
                    if ret is not None:
                        return ret
                    else:
                        continue

        try:
            return __proxy__(self, key)
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key, value):
        def __proxy__(_dict, key, value):
            for k in _dict.keys():
                if k == key:
                    _dict[k] = value
                    return True
                if isinstance(_dict[k], _Dict):
                    return __proxy__(_dict[k], key, value)

        if __proxy__(self, key, value):
            return
        self[key] = value

    def __delattr__(self, key):
        def __proxy__(_dict, key):
            for k in _dict.keys():
                if k == key:
                    del _dict[k]
                    return
                if isinstance(_dict[k], _Dict):
                    __proxy__(_dict[k], key)

        try:
            __proxy__(self, key)
        except KeyError as e:
            raise AttributeError(e)


class ConfigParser(_Dict):

    def __init__(self, filename):
        self.filename = os.path.abspath(filename)
        super(ConfigParser, self).__init__(self.read_configs())

    def read_configs(self):
        with open(self.filename) as f:
            configs = json.load(f)
        return configs

    def initialize_object(self, name, module, *args, **kwargs):
        module_name = self[name]['type']
        module_args = dict(self[name]['args'])
        assert all([k not in module_name for k in kwargs])
        module_args.update(kwargs)
        return getattr(module, module_name)(*args, **module_args)


def print_json(config, indent=''):
    for k, v in config.items():
        if type(config[k]) is _Dict:
            print(indent + f'{k}:')
            print_json(v, indent + '    ')
        else:
            print(indent + f'{k}: {v}')
