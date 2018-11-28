from datetime import datetime
import csv
import fnmatch
import json
import locale
import os
import pandas as pd
import numpy as np
import sys
import fileinput
import zipfile
import psycopg2

def watchDog(sMsg):
    print(sMsg)
    return

appConfigFilePath = os.getcwd()+'/app.json'

# Load config files
watchDog('Open JSON Config File: '+appConfigFilePath)
with open(appConfigFilePath) as config_json_file:
    appConfig = json.load(config_json_file)

# CHANGE INCORRECT OR NULL GUID TO ZERO FORMAT
def config_id(guid):
    return '00000000-0000-0000-0000-000000000000' if (guid == None or len(guid) < 36) else guid.strip()

# CHANGE EMPTY VALUES TO ZERO FORMAT
def nan_values(number):
    return 0 if number == '' else number

# set parameters
appLocale = appConfig['locale']
# Set Locale
locale.setlocale(locale.LC_ALL, appLocale)

fileTargetPath = appConfig['dataFolder']

# LISTING ALL FILES
processFiles = os.listdir(fileTargetPath)
processFiles.sort()

# LOAD olist_marketing_qualified_leads_dataset.csv FROM Kaggle
for processFile in processFiles:
    if fnmatch.fnmatch(processFile, 'olist_marketing_qualified_leads_dataset.csv'):
        processFile1 = pd.read_csv(
            fileTargetPath+processFile, sep=',', header=0, encoding='latin-1', engine='python')

# LOAD olist_closed_deals_dataset.csv.csv FROM Kaggle
for processFile in processFiles:
    if fnmatch.fnmatch(processFile, 'olist_closed_deals_dataset.csv'):
        processFile2 = pd.read_csv(
            fileTargetPath+processFile, sep=',', header=0, encoding='latin-1', engine='python')

# POSTGRES CONNECTION CONFIGURATION
watchDog('Postgre connecting')
conn = psycopg2.connect(
    "host=localhost dbname=postgres user=olist password=postgres")

# INSERT DATA FROM olist_marketing_qualified_leads_dataset TO OLIST_MQL TABLE
watchDog('INSERTING DATA FROM CSV TO OLIST_MQL')
processFile2 = processFile2.replace(np.nan, '', regex=True)
for index, row in processFile1.iterrows():
    cur = conn.cursor()
    insert = """INSERT INTO OLIST_MQL 
                        (ID_MQL, DATE_FIRST_CONTACT, ID_LANDING_PAGE, ORIGIN)
                    VALUES ('%s', '%s', '%s', '%s')""" % (
        row[0],
        row[1],
        row[2],
        row[3])
    cur.execute(insert)

conn.commit()

# INSERT DATA FROM olist_closed_deals_dataset TO OLIST_DEALS TABLE
watchDog('INSERTING DATA FROM CSV TO OLIST_DEALS')
for index, row in processFile2.iterrows():
    cur = conn.cursor()
    insert = """INSERT INTO OLIST_DEALS 
                        (ID_MQL, ID_SELLER, ID_SDR, ID_SR, DATE_WON, BUSINESS_SEGMENT, 
                        TYPE_LEAD, LEAD_BEHAVIOUR_PROFILE, HAS_COMPANY, HAS_GTIN, AVERAGE_STOCK, 
                        TYPE_BUSINESS, DECLARED_PRODUCT_CATALOG_SIZE, DECLARED_MONTHLY_REVENUE)
                    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s)""" % (
        row[0],
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
        row[7],
        row[8],
        row[9],
        row[10],
        row[11],
        nan_values(row[12]),
        row[13])
    cur.execute(insert)

conn.commit()
conn.close()