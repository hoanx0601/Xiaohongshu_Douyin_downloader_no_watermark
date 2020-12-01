import time, re, os, requests, urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if not os.path.exists('小红书'):
    os.makedirs('小红书')
if not os.path.exists('抖音'):
    os.makedirs('抖音')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')
driver.get("https://www.vnil.cn")
search_box = driver.find_elements_by_css_selector('input.inputor')
file1 = open('download.txt', 'r')
counts = []
links_prev = ''
dead = 0

for line in file1:
    line = line.rstrip()
    if re.search(r'小红书', line):
        url = re.sub(r'，复制.*', '', re.sub(r'.*http', 'http', line))
        username = re.sub(r'发布.*', '_', line)
        if dead:
            driver.get("https://www.vnil.cn")
            search_box = driver.find_elements_by_css_selector('input.inputor')
            dead = 0
        search_box[0].clear()
        search_box[0].send_keys(url)
        button = driver.find_elements_by_css_selector('div.buttonor')
        button[0].click()
        time.sleep(5)
        links = driver.find_elements_by_xpath('//span/a')
        tried = 0
        while (not dead and not links) or (not dead and links_prev and links and links_prev == links[0].text):
            print("Click Again!")
            time.sleep(2)
            if tried:
                driver.get(url)
                if driver.find_elements_by_xpath('/html/body/div/div/div/div[2]/div[1]/p'):
                    dead = 1
                    print('Dead!')
                    break
                driver.get("https://www.vnil.cn")
                search_box = driver.find_elements_by_css_selector('input.inputor')
                button = driver.find_elements_by_css_selector('div.buttonor')
            search_box[0].clear()
            search_box[0].send_keys(url)
            button[0].click()
            time.sleep(4)
            links = driver.find_elements_by_xpath('//span/a')
            tried = 1
        if not dead and links:
            links_prev = links[0].text
            if len(links) == 1:
                link = links[0]
                if re.search(r'video', link.text):
                    filename = re.sub(r'\?sign.*', '', re.sub(r'.*com/', '', link.text))
                    urllib.request.urlretrieve(link.text, os.path.join('./小红书', username + filename + '.mp4'))
                else:
                    image_url = re.sub(r'/2/.*/1', '/2/s/1', link.text)
                    filename = re.sub(r'\?image.*', '', re.sub(r'.*com/', '', link.text))
                    with open(os.path.join('./小红书', username + filename + '.jpg'), 'wb') as handle:
                        response = requests.get(image_url)
                        handle.write(response.content)

            else:
                for link in links:
                    image_url = re.sub(r'/2/.*/1', '/2/s/1', link.text)
                    filename = re.sub(r'\?image.*', '', re.sub(r'.*com/', '', link.text))
                    with open(os.path.join('./小红书', username + filename + '.jpg'), 'wb') as handle:
                        response = requests.get(image_url)
                        handle.write(response.content)

    if re.search(r'抖音', line):
        url = re.sub(r' 复制.*', '', re.sub(r'.*http', 'http', line))
        filename = re.sub(r'  http.*', '', line)

        driver.get(url)
        time.sleep(0.5)
        print(driver.page_source)
        time.sleep(0.5)
        if not driver.find_elements_by_css_selector('xg-enter[class="xgplayer-enter"]'):
            links = []
            print("Dead!")
            time.sleep(1)
        
        else:
            username = driver.find_elements_by_css_selector('p.name.nowrap')[0].text
            userid = driver.find_elements_by_css_selector('p.uid.nowrap')[0].text
            time.sleep(0.5)

            driver.get("https://www.vnil.cn")
            search_box = driver.find_elements_by_css_selector('input.inputor')
            search_box[0].clear()
            search_box[0].send_keys(url)
            button = driver.find_elements_by_css_selector('div.buttonor')
            button[0].click()
            time.sleep(4)
            links = driver.find_elements_by_xpath('//span/a')
            while not links or (links_prev and links_prev == links[0].text):
                print("Click Again!")
                time.sleep(2)
                driver.get("https://www.vnil.cn")
                search_box = driver.find_elements_by_css_selector('input.inputor')
                search_box[0].clear()
                search_box[0].send_keys(url)
                button = driver.find_elements_by_css_selector('div.buttonor')
                button[0].click()
                time.sleep(4)
                links = driver.find_elements_by_xpath('//span/a')
            links_prev = links[0].text
            urllib.request.urlretrieve(links[0].text, os.path.join('./抖音', username + '_' + userid + '_' + filename + '.mp4'))
    
    counts.append(len(links))

with open('log.txt', 'w') as f:
    for count in counts:
        f.write("%s\n" % count)

driver.quit()