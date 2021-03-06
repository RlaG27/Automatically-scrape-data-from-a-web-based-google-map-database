############################## prerequisite #############################
#
#   website:    https://radius.unionrealtime.com/home
#   email:      TuckerCapitalGroup@gmail.com
#   password:   2bstronger
#
#########################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import threading, time, csv, xlrd, os, sys, platform, openpyxl
from datetime import date, datetime


class scrapRadius():
    def __init__(self):
        self.url = 'https://radius.unionrealtime.com/home'
        self.email = 'TuckerCapitalGroup@gmail.com'
        self.password = '2bstronger'
        self.coordinates = []
        self.overflow_msg = []
        self.marker_msg = []
        self.total_out = []
        self.total_cnt = 0
        self.total_coor_cnt = 0

        ''' Create Output XLSX file '''

        header = [
            'Type', 'Name of facility', 'Address', 'City', 'State', 'Zip', 'Climate Gross Sqft', 'Climate Net Sqft',
            'Non-Climate Gross Sqft', 'Non-Climate Net Sqft', 'Gross Sqft', 'Net Sqft', '5x5 Climate',
            '5x5 Non-Climate',
            '5x10 Climate', '5x10 Non-Climate', '10x10 Climate', '10x10 Non-Climate', '10x15 Climate',
            '10x15 Non-Climate',
            '10x20 Climate', '10x20 Non-Climate'
        ]

        self.xfile = openpyxl.Workbook()
        self.sheet = self.xfile.worksheets[0]

        for i in range(len(header)):
            self.sheet.cell(row=1, column=i + 1).value = header[i]

        self.output_name = 'Result/result.xlsx'
        self.xfile.save(self.output_name)

        ''' Create Coordinates XLSX file '''

        '''
        header_coor = ['Location', 'Population', 'X', 'Y']
        self.xfile_coor = openpyxl.Workbook()
        self.sheet_coor = self.xfile_coor.worksheets[0]

        for i in range(len(header_coor)):
            self.sheet_coor.cell(row=1, column=i + 1).value = header_coor[i]

        self.output_coor_name = 'Result/coordinates.xlsx'
        self.xfile_coor.save(self.output_coor_name)
        '''

        ''' Read Coordinates XLSX file '''

        self.in_coor_name = 'Result/coordinates.xlsx'
        self.xfile_in = xlrd.open_workbook(self.in_coor_name)

        self.sheet_in = self.xfile_in.sheet_by_index(0)

        for i in range(self.sheet_in.nrows):
            if i==0:
                continue

            self.coordinates.append([self.sheet_in.row(i)[2].value, self.sheet_in.row(i)[3].value])
            print([self.sheet_in.row(i)[2].value, self.sheet_in.row(i)[3].value])

    def passLogin(self):

        self.driver = webdriver.Chrome(executable_path=os.getcwd() + '/WebDriver/chromedriver.exe')
        self.driver.maximize_window()
        self.driver.get(self.url)

        print("Go to 'https://radius.unionrealtime.com/home'.")

        signin_btns = WebDriverWait(self.driver, 500).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.btn.btn-clear.btn-lg"))
        )
        signin_btns[1].click()

        print("Clicked 'SIGN IN'.")

        # print(self.driver.page_source)

        time.sleep(5)

        WebDriverWait(self.driver, 500).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.auth0-lock-cred-pane.auth0-lock-quiet"))
        )

        time.sleep(5)

        email_in = WebDriverWait(self.driver, 500).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.auth0-lock-input-email > div > input"))
        )

        action_chain = ActionChains(self.driver)
        action_chain.click(email_in).send_keys(self.email).perform()

        time.sleep(5)
        print("Put email.")

        pass_in = WebDriverWait(self.driver, 500).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.auth0-lock-input-password > div > input"))
        )

        action_chain = ActionChains(self.driver)
        action_chain.click(pass_in).send_keys(self.password).perform()

        time.sleep(3)
        print("Put password.")

        login_btn = WebDriverWait(self.driver, 500).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button.auth0-lock-submit"))
        )

        login_btn.click()

        print("Clicked login button.")

        time.sleep(10)

    def search_coordinates(self):

        self.radius_link = WebDriverWait(self.driver, 50).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "li#radius-link"))
        )

        for x_i in range(11, 122):
            x = x_i * 10
            for y_i in range(70):
                y = y_i * 10

                if [x, y] not in self.coordinate:
                    self.check_polygones(x, y)

    def check_polygones(self, x, y):

        self.driver.delete_all_cookies()
        minus_btn = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@src='/assets/images/zo.png']"))
        )
        minus_btn.click()

        action_chain = ActionChains(self.driver)
        action_chain.move_to_element(self.radius_link).move_by_offset(x, y).perform()
        print('Moved to : ({}, {})'.format(x, y))

        try:
            overflow_msg = WebDriverWait(self.driver, 1).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "gm-style-iw"))
            )

            overflow_msg_txt = overflow_msg.text.strip().split('\n')
            location = overflow_msg_txt[0]
            population = overflow_msg_txt[1]

            if location not in self.overflow_msg:
                self.overflow_msg.append(location)
                self.total_coor_cnt += 1
                logTxt = "\tOverflow Text:\t{}\n\tLocation:\t({}, {})\n".format(overflow_msg_txt, x, y)
                print(logTxt)

                self.sheet_coor.cell(row=self.total_coor_cnt + 1, column=1).value = location
                self.sheet_coor.cell(row=self.total_coor_cnt + 1, column=2).value = population
                self.sheet_coor.cell(row=self.total_coor_cnt + 1, column=3).value = x
                self.sheet_coor.cell(row=self.total_coor_cnt + 1, column=4).value = y

                self.xfile_coor.save(self.output_coor_name)

        except:
            pass

    def navigate(self):

        # 1920**1080
        for coord in self.coordinates:
            self.navigate_offset(coord[0], coord[1])

    def navigate_offset(self, x, y):

        self.driver.delete_all_cookies()

        print(
            '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        minus_btn = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@src='/assets/images/zo.png']"))
        )
        minus_btn.click()

        radius_link = WebDriverWait(self.driver, 50).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "li#radius-link"))
        )
        action_chain = ActionChains(self.driver)
        action_chain.move_to_element(radius_link).move_by_offset(x, y).click().perform()

        print('Moved to : ({}, {}).'.format(x, y))

        time.sleep(3)

        favorite_btn = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa.fa-building.text-white"))
        )

        favorite_btn.click()
        time.sleep(2)

        fullscreen_btn = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='gm-style']/button"))
        )

        fullscreen_btn.click()
        time.sleep(2)

        self.marker_search('red')
        self.marker_search('blue')

        fullscreen_btn = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='gm-style']/button"))
        )

        fullscreen_btn.click()

        radius_link = WebDriverWait(self.driver, 50).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "li#radius-link"))
        )
        radius_link.click()


        time.sleep(2)

    def marker_search(self, _type):

        try:
            strange_markers = new_markers = WebDriverWait(self.driver, 50).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//*[@src='//cdn.rawgit.com/mahnunchik/markerclustererplus/master/images/m3.png']"))
            )

            if len(strange_markers) >= 1:
                return

        except:
            pass

        try:
            strange_markers = new_markers = WebDriverWait(self.driver, 50).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//*[@src='//cdn.rawgit.com/mahnunchik/markerclustererplus/master/images/m1.png']"))
            )

            if len(strange_markers) >= 1:
                return

        except:
            pass

        new_markers = WebDriverWait(self.driver, 50).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@src='/assets/images/dot_{}.png']".format(_type)))
        )

        if len(new_markers) is 1:
            return

        for marker in new_markers:

            parent_of_marker = marker.find_element_by_xpath('..').text.strip()

            if 'Current Supply' in parent_of_marker or 'New Supply' in parent_of_marker or 'Selected' in parent_of_marker:
                continue

            action_chain = ActionChains(self.driver)
            action_chain.move_to_element(marker).move_by_offset(0, -20).click(marker).perform()
            time.sleep(2)

            facility_panels = WebDriverWait(self.driver, 50).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.value.editable.unselectable.ng-binding"))
            )

            if _type is 'red':
                type = 'Current'
            else:
                type = 'New'

            try:
                name_of_facility = facility_panels[0].text.strip()
            except:
                name_of_facility = ''

            try:
                address = facility_panels[1].text.strip() + '\n' + facility_panels[2].text.strip()
            except:
                address = ''

            try:
                city = facility_panels[3].text.strip()
            except:
                city = ''

            try:
                state = facility_panels[4].text.strip()
            except:
                state = ''

            try:
                zip = facility_panels[5].text.strip()
            except:
                zip = ''

            try:
                climate_gross_sqft = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[1]/tbody/tr[1]/td[2]").text.strip()
            except:
                climate_gross_sqft = ''

            try:
                climate_net_sqft = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[1]/tbody/tr[1]/td[3]").text.strip()
            except:
                climate_net_sqft = ''

            try:
                non_climate_gross_sqft = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[1]/tbody/tr[2]/td[2]").text.strip()
            except:
                non_climate_gross_sqft = ''

            try:
                non_climate_net_sqft = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[1]/tbody/tr[2]/td[3]").text.strip()
            except:
                non_climate_net_sqft = ''

            try:
                gross_sqft = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[1]/tbody/tr[3]/td[2]").text.strip()
            except:
                gross_sqft = ''

            try:
                net_sqft = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[1]/tbody/tr[3]/td[3]").text.strip()
            except:
                net_sqft = ''

            try:
                climate_5_5 = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[2]/tbody/tr[1]/td[2]").text.strip()
            except:
                climate_5_5 = ''

            try:
                non_climate_5_5 = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[2]/tbody/tr[1]/td[3]").text.strip()
            except:
                non_climate_5_5 = ''

            try:
                climate_5_10 = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[2]/tbody/tr[2]/td[2]").text.strip()
            except:
                climate_5_10 = ''

            try:
                non_climate_5_10 = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[2]/tbody/tr[2]/td[3]").text.strip()
            except:
                non_climate_5_10 = ''

            try:
                climate_10_10 = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[2]/tbody/tr[3]/td[2]").text.strip()
            except:
                climate_10_10 = ''

            try:
                non_climate_10_10 = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[2]/tbody/tr[3]/td[3]").text.strip()
            except:
                non_climate_10_10 = ''

            try:
                climate_10_15 = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[2]/tbody/tr[4]/td[2]").text.strip()
            except:
                climate_10_15 = ''

            try:
                non_climate_10_15 = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[2]/tbody/tr[4]/td[3]").text.strip()
            except:
                non_climate_10_15 = ''

            try:
                climate_10_20 = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[2]/tbody/tr[5]/td[2]").text.strip()
            except:
                climate_10_20 = ''

            try:
                non_climate_10_20 = self.driver.find_element_by_xpath(
                    "//div[@class='iw']/table[2]/tbody/tr[5]/td[3]").text.strip()
            except:
                non_climate_10_20 = ''

            if [
                type, name_of_facility, address, city, state, zip, climate_gross_sqft, climate_net_sqft,
                non_climate_gross_sqft, non_climate_net_sqft, gross_sqft, net_sqft, climate_5_5,
                non_climate_5_5, climate_5_10, non_climate_5_10, climate_10_10, non_climate_10_10,
                climate_10_15, non_climate_10_15, climate_10_20, non_climate_10_20
            ] not in self.total_out:
                self.total_out.append(
                    [
                        type, name_of_facility, address, city, state, zip, climate_gross_sqft,
                        climate_net_sqft,
                        non_climate_gross_sqft, non_climate_net_sqft, gross_sqft, net_sqft, climate_5_5,
                        non_climate_5_5, climate_5_10, non_climate_5_10, climate_10_10,
                        non_climate_10_10,
                        climate_10_15, non_climate_10_15, climate_10_20, non_climate_10_20
                    ]
                )

                self.total_cnt += 1

                '''
                self.writer.writerow(
                    [
                        type, name_of_facility, address, city, state, zip, climate_gross_sqft,
                        climate_net_sqft,
                        non_climate_gross_sqft, non_climate_net_sqft, gross_sqft, net_sqft, climate_5_5,
                        non_climate_5_5, climate_5_10, non_climate_5_10, climate_10_10,
                        non_climate_10_10,
                        climate_10_15, non_climate_10_15, climate_10_20, non_climate_10_20
                    ]
                )
                '''

                for i, elm in enumerate([
                    type, name_of_facility, address, city, state, zip, climate_gross_sqft,
                    climate_net_sqft,
                    non_climate_gross_sqft, non_climate_net_sqft, gross_sqft, net_sqft, climate_5_5,
                    non_climate_5_5, climate_5_10, non_climate_5_10, climate_10_10,
                    non_climate_10_10,
                    climate_10_15, non_climate_10_15, climate_10_20, non_climate_10_20
                ]):
                    self.sheet.cell(row=self.total_cnt + 1, column=i + 1).value = elm

                self.xfile.save(self.output_name)

                logTxt = '\t{0}\n\t{1}\n\t{2}\n\t{3}\n\t{4}\n\t{5}\n\t{6}\n\t{7}\n\t{8}\n\t{9}\n\t{10}\n' \
                         '\t{11}\n\t{12}\n\t{13}\n\t{14}\n\t{15}\n\t{16}\n\t{17}\n\t{18}\n\t{19}\n\t{20}\n' \
                         '\t{21}\n'.format(
                    type, name_of_facility, address, city, state, zip, climate_gross_sqft,
                    climate_net_sqft,
                    non_climate_gross_sqft, non_climate_net_sqft, gross_sqft, net_sqft, climate_5_5,
                    non_climate_5_5, climate_5_10, non_climate_5_10, climate_10_10,
                    non_climate_10_10,
                    climate_10_15, non_climate_10_15, climate_10_20, non_climate_10_20
                )

                print(logTxt)

                logTxt = '\tTotal Count: {}\n'.format(self.total_cnt)
                print(logTxt)

                close_btn = self.driver.find_element_by_xpath(
                    "//*[@id='page-wrapper']/div[2]/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div[1]/div[4]/div[4]/div[2]/div[3]")
                close_btn.click()

if __name__ == '__main__':
    app = scrapRadius()
    app.passLogin()
    app.navigate()
