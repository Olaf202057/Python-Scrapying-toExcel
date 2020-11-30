from aifc import Error
from selenium import webdriver


class UrlsSpider:
    name = "urls_spider"

    def __init__(self, states):
        self.driver = webdriver.Chrome('./path/chromedriver.exe')
        self.states = states
        self.base_url = "https://enviro.epa.gov/enviro/sdw_query_v3.get_list?wsys_name=&fac_search=fac_beginning" \
                        "&fac_county=&fac_city=&pop_serv=500&pop_serv=3300&pop_serv=10000&pop_serv=100000&pop_serv" \
                        "=100001&sys_status=active&pop_serv=&wsys_id=&fac_state=%s&last_fac_name=&page=1" \
                        "&query_results=&total_rows_found= "
        self.sysType = ["Community Water Systems", "Non-Transient Non-Community Water Systems",
                        "Transient Non-Community Water Systems"]
        self.url = []

    def run(self):
        try:
            self.base_urls()
            self.driver.close()
            return self.url
        except Error as e:
            print(e)

    def base_urls(self):
        i = 0
        for val in self.states:
            url = self.base_url % val
            self.driver.get(url)
            self.driver.implicitly_wait(3)
            try:
                cancel = self.driver.find_element_by_xpath('//button[@id="fsrFocusFirst"]')
                cancel.click()
                self.driver.implicitly_wait(2)
            except:
                pass
            i += 1
            print("This is States loop")
            print(i)
            self.collect_urls()

    def collect_urls(self):
        divs = self.driver.find_elements_by_xpath('//div[@id="results2_wrapper"]')
        i = 0
        for div in divs:
            sysType = self.sysType[i]
            print(sysType)
            i += 1
            select = div.find_element_by_css_selector('div[class="bottom"] div[class="dataTables_length"] label select[name="results2_length"] option[value="100"]')
            select.click()
            self.driver.implicitly_wait(3)
            while True:
                try:
                    dataUrls = div.find_elements_by_css_selector('table[id="results2"] tbody tr td a')
                    self.store_urls(dataUrls, sysType)
                    btnNext = div.find_element_by_css_selector('div[class="bottom"] div[class="dataTables_paginate fg-buttonset ui-buttonset fg-buttonset-multi ui-buttonset-multi paging_full_numbers"] a[class="fg-button ui-button ui-state-default next"]')
                    btnNext.click()
                except:
                    break

    def store_urls(self, urls, sysType):
        for val in urls:
            val = val.get_attribute("href")
            self.url.append(val)

