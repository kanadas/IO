import numpy as np
import csv
import json
import random

class Distribution:
    def __init__(self, devices, op_sys, op_sys_ver, browsers, browser_ver):
        self.devices = devices
        self.op_sys = op_sys
        self.op_sys_ver = op_sys_ver
        self.browsers = browsers
        self.browser_ver = browser_ver
    

## Loads statistical data from files and returns it in format acceptable by generate_user_agents
def load_statistics():
    devices = []
    with open('../data/devices.csv', 'r', encoding='utf-8') as f:
        freader = csv.reader(f, dialect='excel', delimiter=',')
        devices = [(row[0].replace('"', '').lower(), float(row[1])) for row in freader]
    op_sys = {}
    op_sys_ver = {}
    browsers = {}
    browser_ver = {}
    for dev in devices[:][0]:
        with open('../data/os-' + dev, 'r', encoding='utf-8') as f:
            freader = csv.reader(f, dialect='excel', delimeter=',')
            op_sys[dev] = np.array([[row[0].strip().replace('"', '').lower(), float(row[1])] for row in freader])
        op_sys_ver[dev] = {}
        for os in op_sys[dev].items()[:,0]:
            with open('../data/' + os + '-version-' + dev, 'r', encoding='utf-8') as f:
                freader = csv.reader(f, dialect='excel', delimeter=',')
                op_sys_ver[dev][os] = np.array([[row[0].strip().replace('"', '').lower(), float(row[1])] for row in freader])
        with open('../data/browser-' + dev, 'r', encoding='utf-8') as f:
            freader = csv.reader(f, dialect='excel', delimeter=',')
            browsers[dev] = np.array([[row[0].strip().replace('"', '').lower(), float(row[1])] for row in freader])
    with open('../data/browser-version.csv', 'r', encoding='utf-8') as f:
        freader = csv.reader(r, dialect='excel', dilimeter=',')
        for row in freader:
            name = row[0].strip().replace('"', '').lower()
            brow = name[:name.rfind(' ') - 1]
            ver = name[name.rfind(' ') + 1:]
            if not browser_ver.has_key(brow): browser_ver[brow] = []
            browser_ver[brow].append((ver, float(row[1])))

    #counting prefix sums of propabilities - helps in generating
    devices = np.cumsum(devices[key], axis = [0, 1])
    for key in op_sys:
        op_sys[key] = np.cumsum(op_sys[key], axis = [0, 1])
    for key in op_sys_ver:
        for key2 in op_sys_ver[key]:
            op_sys_ver[key][key2] = np.cumsum(op_sys_ver[key][key2], axis = [0, 1])
    for key in browsers:
        browsers[key] = np.cumsum(browsers[key], axis = [0, 1])
    for key in browser_ver:
        browser_ver[key] = np.cumsum(browser_ver[key], axis = [0, 1])

    return Distribution(devices, op_sys, op_sys_ver, browsers, browser_ver)
    

## Generates specified number of user agents as (for now not) numpy array of strings.
#  Generated data follow specified distribution
#  @param dist - desired distribution of user agents
#  @param n - number of results
#  @result - numpy array of n random user agents
def generate_user_agents(dist, n):
    random.seed()
    agents = []
    for i in range(n):
        r = random.uniform(0, dist.devices[-1][1])
        dev = dist.devices[np.searchsorted(dist.devices[:,1], r)][0]
        systems = dist.op_sys[dev][:,1]
        r = random.uniform(0, systems[-1])
        sys = dist.op_sys[dev][np.searchsorted(systems, r)][0]
        versions = dist.op_sys_ver[dev][sys][:,1]
        r = random.uniform(0, versions[-1])
        sys_ver = dist.op_sys_ver[dev][sys][np.searchsorted(versions, r)][0]
        browsers = dist.browsers[dev][:,1]
        r = random.uniform(0, browsers[-1])
        browser = dist.browsers[dev][np.searchsorted(browsers, r)][0]
        browser_versions = dist.browser_ver[browser][:,1]
        r = random.uniform(0, browser_versions[-1])
        brow_ver = dist.browser_ver[browser][np.searchsorted(browser_versions, r)][0]
        
        ua = 'Mozilla/5.0 '
        if device == 'desktop':
            if sys == 'windows':
                ua = ua + '(Windows NT '
                if sys_ver == 'win10': ua = ua + '10.0'
                elif sys_ver == 'win8.1': ua = ua + '6.3'
                elif sys_ver == 'win8': ua = ua + '6.2'
                elif sys_ver == 'win7': ua = ua + '6.1'
                elif sys_ver == 'winxp': ua = ua + '5.1'
                if browser in ['chrome', 'firefox', 'opera', 'edge']:
                    #I dont have statistics for this 0.5 - just guessing
                    if random.random() > 0.5: ua = ua + '; Win64; x64'
                    else: ua = ua + '; WOW64'
            elif sys == "macos":
                ua = ua + '(Macintosh;'
                #I dont have statistics for this 0.2 - just guessing
                if random.random > 0.2: ua = ua + ' Intel '
                else: ua = ua + ' PPC '
                ua = ua + 'Mac OS X '
                if sys_ver == 'macos sierra': ua = ua + '10.12'
                elif sys_ver == 'macos high sierra': ua = ua + '10.13'
                elif sys_ver == 'os x el capitan': ua = ua + '10.11'
            elif sys == 'linux':
                ua = ua + 'X11; Linux '
                if sys_ver == 'x86_64':
                    #I dont have statistics for this 0.2 - just guessing
                    if random.random > 0.2: ua = ua + 'x86_64'
                    else: ua = ua + 'i686 on x86_64'
                else: ua = ua + 'i686'
            #i treat all IE's as IE 11, because earlier versions are very rare, and very different
            if browser == 'ie': ua = ua + '; Trident/7.0; rv:11.0) like Gecko'
            elif browser == 'firefox': ua = ua + '; rv:' + brow_ver + ') Gecko/20100101 Firefox/' + brow_ver
            else:
                ua = ua + ') AppleWebKit/537.36 (KHTML, like Gecko) '
                if browser == 'chrome': ua = ua + 'Chrome/' + brow_ver + '.0.0 Safari/537.36'
                elif browser == 'opera': ua = ua + 'Chrome/56.0.2924.87 Safari/537.36 OPR/' + brow_ver + '.0.0'
                elif browser == 'edge': ua = ua + 'Chrome/56.0.2924.87 Safari/537.36 Edge/' + brow_ver + '.0'
        elif device == 'mobile' or device == 'tablet':
            if sys == 'android':
                ua = ua + '(Linux; Android ' + sys_ver[0:2] + ')'
            elif sys == 'ios':
                if device == 'mobile': ua = ua + '(iPhone; '
                else: ua = ua + '(iPad; '
                ua = ua + 'CPU iPhone OS ' + sys_ver[4:] + ' like Mac OS X)'
            ua = ua + 'AppleWebKit/537.36 (KHTML, like Gecko) '
            if browser == 'samsung internet': ua = ua + 'SamsungBrowser/' + brow_ver + ' Chrome/56.0.2924.87'
            if browser == 'chrome':
                if sys == 'ios': ua = ua + ' CriOS'
                else: ua = ua + ' Chrome'
                ua = ua + '/' + brow_ver + '.0.0'
            elif browser == 'safari' or browser == 'android': ua = ua + ' Version/' + brow_ver
            if device == 'mobile': ua = ua + ' Mobile'
            ua = ua + ' Safari/537.36'
            if browser == 'opera': ua = ua + ' OPR/' + brow_ver + '.0.0'

        agents.append(ua)
    return agents

generate_user_agents(load_statistics(), 100)
