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


class scrapModel():
    def __init__(self):

        ''' Initialize parameters '''
        self.url = 'https://radius.unionrealtime.com/home'
        self.email = 'TuckerCapitalGroup@gmail.com'
        self.password = '2bstronger'
        self.coordinates = []
        self.total_out = []
        self.total_cnt = 0
        self.log_printer = log_printer()

        ''' Create Output XLSX file '''

        try:
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
            logTxt = "Success:\tCreated output XLSX file successfully."
            self.log_printer.print_log(logTxt)
        except:
            logTxt = "Error:\tFailed to create output XLSX file."
            self.log_printer.print_log(logTxt)
            exit(1)

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
        try:
            in_coor_name = 'Data/coordinates.xlsx'
            xfile_in = xlrd.open_workbook(in_coor_name)
            sheet_in = xfile_in.sheet_by_index(0)

            for i in range(sheet_in.nrows):
                if i == 0:
                    continue

                self.coordinates.append([sheet_in.row(i)[2].value, sheet_in.row(i)[3].value])
                #print([self.sheet_in.row(i)[2].value, self.sheet_in.row(i)[3].value])

            self.coordinates.reverse()

            logTxt = "Success:\tRead coordinates XLSX file successfully."
            self.log_printer.print_log(logTxt)

        except:
            logTxt = "Error:\tFailed to read coordinates XLSX file."
            self.log_printer.print_log(logTxt)
            exit(1)

    def pop_coordinate(self):
        try:
            coord = self.coordinates.pop()
            return coord
        except:
            logTxt = "Coordinates are empty."
            self.log_printer.print_log(logTxt)
            return None

    def add_coordinate(self, coord):
        try:
            self.coordinates = [coord] + self.coordinates
        except:
            logTxt = "Failed to add coordinate."
            self.log_printer.print_log(logTxt)

    def add_row_xlsx(self, row):

        try:
            self.total_cnt += 1

            for i, elm in enumerate(row):
                self.sheet.cell(row=self.total_cnt + 1, column=i + 1).value = elm

            self.xfile.save(self.output_name)
        except:
            logTxt = "Failed to add row to xlsx."
            self.log_printer.print_log(logTxt)

    def isRowExist(self, row):
        if row in self.total_out:
            return True
        else:
            return False

    def add_row(self, row):
        self.total_out.append(row)

class totalScraper():
    def __init__(self):
        self.scrapModel = scrapModel()
        self.log_printer = log_printer()

    def startScraping(self):
        self.max_threads = 1
        self.threads = []

        for i in range(self.max_threads):
            scraper = onescraper(self.scrapModel, self.log_printer)
            thread =  threading.Thread(target=scraper.one_scraping)
            thread.setDaemon(True)
            thread.start()
            self.threads.append(thread)
            time.sleep(1)

class onescraper():
    def __init__(self, scrapModel, log_printer):
        self.url = 'https://radius.unionrealtime.com/home'
        self.email = 'TuckerCapitalGroup@gmail.com'
        self.password = '2bstronger'
        self.total_out = []
        self.scrapModel = scrapModel
        self.log_printer = log_printer

    def one_scraping(self):
        self.passLogin()

        while(self.scrapModel.coordinates):
            [x, y] = self.scrapModel.pop()
            self.navigate_offset(x,y)

    def passLogin(self):

        try:
            self.driver = webdriver.Chrome(executable_path=os.getcwd() + '/WebDriver/chromedriver.exe')
            self.driver.maximize_window()
            self.driver.get(self.url)
            logTxt = "Success:\tGo to 'https://radius.unionrealtime.com/home'."
            self.log_printer.print_log(logTxt)
        except:
            logTxt = "Error:\tFailed to access to the website."
            self.log_printer.print_log(logTxt)
            exit(1)

        try:
            signin_btns = WebDriverWait(self.driver, 200).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.btn.btn-clear.btn-lg"))
            )
            signin_btns[1].click()
            time.sleep(5)
            logTxt = "Success:\tClicked SIGN IN button."
            self.log_printer.print_log(logTxt)
        except:
            logTxt = "Error:\tFailed to click SIGN IN button."
            self.log_printer.print_log(logTxt)
            exit(1)

        try:
            WebDriverWait(self.driver, 200).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.auth0-lock-cred-pane.auth0-lock-quiet"))
            )

            time.sleep(5)

            email_in = WebDriverWait(self.driver, 200).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.auth0-lock-input-email > div > input"))
            )

            action_chain = ActionChains(self.driver)
            action_chain.click(email_in).send_keys(self.email).perform()

            time.sleep(5)

            logTxt = "Success:\tPut email."
            self.log_printer.print_log(logTxt)

            pass_in = WebDriverWait(self.driver, 500).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.auth0-lock-input-password > div > input"))
            )

            action_chain = ActionChains(self.driver)
            action_chain.click(pass_in).send_keys(self.password).perform()

            time.sleep(3)

            logTxt = "Success:\tPut password."
            self.log_printer.print_log(logTxt)

            login_btn = WebDriverWait(self.driver, 200).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "button.auth0-lock-submit"))
            )

            login_btn.click()

            logTxt = "Success:\tClicked login button."
            self.log_printer.print_log(logTxt)
            time.sleep(10)

        except:
            logTxt = "Error:\tFailed to log in."
            self.log_printer.print_log(logTxt)
            exit(1)

    def navigate_offset(self, x, y):

        logTxt = '\n###########################################################################################################################################################\n'
        self.log_printer.print_log(logTxt)

        try:
            # self.driver.delete_all_cookies()
            minus_btn = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@src='/assets/images/zo.png']"))
            )
            minus_btn.click()
            time.sleep(2)

            logTxt = 'Success:\tClicked minus button successfully.'
            self.log_printer.print_log(logTxt)

        except:
            logTxt = 'Error:\tFailed to click minus button successfully.'
            self.log_printer.print_log(logTxt)
            self.scrapModel.add_coordinate([x,y])
            return


        try:
            radius_link = WebDriverWait(self.driver, 50).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "li#radius-link"))
            )

            # radius_link.click()

            action_chain = ActionChains(self.driver)
            action_chain.move_to_element(radius_link).move_by_offset(x, y).click().perform()
            time.sleep(2)

            logTxt = 'Success:\tClicked ({}, {}).'.format(x,y)
            self.log_printer.print_log(logTxt)

        except:
            logTxt = 'Error:\tFailed to click ({}, {}).'.format(x, y)
            self.log_printer.print_log(logTxt)
            self.scrapModel.add_coordinate([x, y])
            return


        '''
        favorite_btn = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa.fa-building.text-white"))
        )

        favorite_btn.click()

        time.sleep(1)
        '''

        try:
            fullscreen_btn = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='gm-style']/button"))
            )

            fullscreen_btn.click()
            time.sleep(2)

            logTxt = 'Success:\tClicked fullscreen button(1).'
            self.log_printer.print_log(logTxt)

        except:
            logTxt = 'Error:\tFailed to click fullscreen button(1).'
            self.log_printer.print_log(logTxt)
            self.scrapModel.add_coordinate([x, y])
            return

        self.marker_search('red')
        self.marker_search('blue')

        try:
            fullscreen_btn = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='gm-style']/button"))
            )

            fullscreen_btn.click()
            time.sleep(2)

            logTxt = 'Success:\tClicked fullscreen button(2).'
            self.log_printer.print_log(logTxt)

        except:
            logTxt = 'Error:\tFailed to click fullscreen button(2).'
            self.log_printer.print_log(logTxt)
            self.scrapModel.add_coordinate([x, y])
            return

    def marker_search(self, _type):

        try:
            strange_markers = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//img[@src='//cdn.rawgit.com/mahnunchik/markerclustererplus/master/images/m3.png']"))
            )

            return

        except:
            pass

        try:
            strange_markers = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//img[@src='//cdn.rawgit.com/mahnunchik/markerclustererplus/master/images/m1.png']"))
            )

            return

        except:
            pass

        try:
            new_markers = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//img[@src='/assets/images/dot_{}.png']".format(_type)))
            )

            logTxt = '\tSuccess:\t{} markers are found.'.format(len(new_markers))
            self.log_printer.print_log(logTxt)

        except:
            logTxt = '\tError:\t{} No markers are found.'.format(len(new_markers))
            self.log_printer.print_log(logTxt)
            return

        if len(new_markers) is 1:
            logTxt = '\tOnly 1 marker is found, so skipped.'
            self.log_printer.print_log(logTxt)
            return

        for marker in new_markers:

            logTxt = '\t-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n'
            self.log_printer.print_log(logTxt)

            try:
                parent_of_marker = marker.find_element_by_xpath('..')
                parent_of_marker_txt = parent_of_marker.text.strip()
                if 'Current Supply' in parent_of_marker_txt or 'New Supply' in parent_of_marker_txt or 'Selected' in parent_of_marker_txt:
                    logTxt = "\t\tThis is 'Current' or 'New Supply', 'Selected' marker"
                    self.log_printer.print_log(logTxt)
                    continue

                style_txt = parent_of_marker.get_attribute('style')
                import re
                regex = r"left: ([\d-]+)px; top: ([\d-]+)px"
                match = re.findall(regex, style_txt)

                left_px = float(list(match[0])[0])
                top_px = float(list(match[0])[1])

                if left_px < 0 or left_px > 1920 or top_px < 0 or top_px > 1080:
                    logTxt = "\t\tThis is marker out of screen."
                    self.log_printer.print_log(logTxt)
                    continue
            except:
                logTxt = '\t\tError: Error happened in validating marker.'
                self.log_printer.print_log(logTxt)
                continue

            try:
                action_chain = ActionChains(self.driver)
                action_chain.move_to_element(marker).click(marker).perform()
                logTxt = "\t\tSuccess:\tMarker is clicked."
                self.log_printer.print_log(logTxt)
            except:
                logTxt = "\t\tError:\tMarker is unable to be clicked."
                self.log_printer.print_log(logTxt)
                continue

            try:
                WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "div.iw"))
                )
                logTxt = "\t\tSucess:\tMarker overflow message is found."
                self.log_printer.print_log(logTxt)

            except:
                logTxt = "\t\tError:\tMarker overflow message is not found."
                self.log_printer.print_log(logTxt)
                continue

            try:
                if _type is 'red':
                    type = 'Current'
                else:
                    type = 'New'

                try:
                    # name_of_facility = facility_panels[0].text.strip()
                    name_of_facility = self.driver.find_element_by_xpath(
                        "//div[@class='iw']/h4").text.strip()
                except:
                    name_of_facility = ''

                try:
                    # address = facility_panels[1].text.strip() + '\n' + facility_panels[2].text.strip()
                    address_city_state_zip = self.driver.find_element_by_xpath(
                        "//div[@class='iw']/p").text.strip().split('\n')
                    try:
                        address = address_city_state_zip[0]
                    except:
                        address = ''

                    try:
                        city = address_city_state_zip[1]
                    except:
                        city = ''

                    try:
                        state = address_city_state_zip[2]
                    except:
                        state = ''

                    try:
                        zip = address_city_state_zip[3]
                    except:
                        zip = ''

                except:
                    pass

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

                close_btn = self.driver.find_element_by_xpath(
                    "//*[@id='page-wrapper']/div[2]/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div[1]/div[4]/div[4]/div[2]/div[3]")
                close_btn.click()

                logTxt = "\t\tSucess:\tScraped data from marker overflow message."
                self.log_printer.print_log(logTxt)

            except:
                logTxt = "\t\tError:\tCan't scrape data from marker overflow message."
                self.log_printer.print_log(logTxt)
                continue

            if self.scrapModel.isRowExist([type, name_of_facility, address, city, state, zip]) is False:
                self.scrapModel.add_row([type, name_of_facility, address, city, state, zip])
                self.scrapModel.add_row_xlsx([
                    type, name_of_facility, address, city, state, zip, climate_gross_sqft,
                    climate_net_sqft,
                    non_climate_gross_sqft, non_climate_net_sqft, gross_sqft, net_sqft, climate_5_5,
                    non_climate_5_5, climate_5_10, non_climate_5_10, climate_10_10,
                    non_climate_10_10,
                    climate_10_15, non_climate_10_15, climate_10_20, non_climate_10_20
                ])

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

                self.log_printer.print_log(logTxt)

                logTxt = '\tTotal Count: {}'.format(self.scrapModel.total_cnt)
                self.log_printer.print_log(logTxt)

            else:
                logTxt = '\tThis marker was found before'
                self.log_printer.print_log(logTxt)

class log_printer():
    def __init__(self):
        curTime = time.strftime("%d-%m-%Y_%H.%M.%S")
        self.logFile_name = "Log_File_" + curTime + ".txt"
        try:
            self.logFile = open(self.logFile_name, "w+")
            logTxt = "Log file created successfully!!!\n"
            print(logTxt)
        except:
            logTxt = "It failed to create log file\n"
            print(logTxt)
            exit(1)

    def print_log(self, logTxt):
        self.logFile.write(logTxt + '\n')
        self.logFile.flush()
        print(logTxt + '\n')

    def close_log(self):
        self.logFile.close()

def date2str(dt, deliminter, order=0):
    dt = str(dt).split(' ')[0].split('-')
    if order == 0:
        dateStr = dt[0] + deliminter + dt[1] + deliminter + dt[2]
    else:
        dateStr = dt[2] + deliminter + dt[1] + deliminter + dt[0]

    return dateStr

if __name__ == '__main__':
    app = totalScraper()
    app.startScraping()
