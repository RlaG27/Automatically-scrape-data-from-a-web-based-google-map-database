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

        self.coordinates = {}
        ''' Read Coordinates XLSX file '''
        try:
            in_coor_name = 'Data/coordinates.xlsx'
            xfile_in = xlrd.open_workbook(in_coor_name)
            sheet_in = xfile_in.sheet_by_index(0)

            for i in range(sheet_in.nrows):
                if i == 0:
                    continue

                if sheet_in.row(i)[0].value not in self.coordinates:
                    self.coordinates[sheet_in.row(i)[0].value] = []

                self.coordinates[sheet_in.row(i)[0].value].append([sheet_in.row(i)[2].value, sheet_in.row(i)[3].value])

                #print([self.out_sheet_in.row(i)[2].value, self.out_sheet_in.row(i)[3].value])

            logTxt = "Success:\tRead coordinates XLSX file successfully."
            print(logTxt)

            ''' Create Coordinates XLSX file '''

            coord_header = ['Location', 'X', 'Y']
            coord_xfile = openpyxl.Workbook()
            coord_sheet = coord_xfile.worksheets[0]

            for i in range(len(coord_header)):
                coord_sheet.cell(row=1, column=i + 1).value = coord_header[i]

            coord_xfile_name = 'Data/coordinates_filtered.xlsx'
            coord_xfile.save(coord_xfile_name)

            row_cnt = 0
            import statistics
            for key in self.coordinates:
                row_cnt += 1
                print(key, statistics.median_low(self.coordinates[key]))
                [x,y] = statistics.median_low(self.coordinates[key])
                coord_sheet.cell(row=row_cnt+1, column=1).value = key
                coord_sheet.cell(row=row_cnt+1, column=2).value = x
                coord_sheet.cell(row=row_cnt+1, column=3).value = y
                coord_xfile.save(coord_xfile_name)

        except:
            logTxt = "Error:\tFailed to read coordinates XLSX file."
            print(logTxt)
            exit(1)


if __name__ == '__main__':
    #app = totalScraper()
    #app.startScraping()
    app = scrapModel()
