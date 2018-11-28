import numpy as np
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# POSTGRES CONNECTION
conn = psycopg2.connect(
    "host=localhost dbname=postgres user=olist password=postgres")

sqlLP =   """ 
            SELECT      ID_LANDING_PAGE, COUNT(*)
            FROM        OLIST_CONSOLIDATE
            GROUP BY    ID_LANDING_PAGE
            HAVING      COUNT(ID_LANDING_PAGE) > 100
            ORDER BY    2 DESC
        """

res = conn.cursor()
res.execute(sqlLP)
result = res.fetchall()

print("\n****************************")
print("*** TOP LANDING PAGE ****")
print("****************************\n")
print("\nInteresting to know what landing page are the best and why as well as how to invest more in it\n")
for i in range(0, len(result)):
    print(i+1,')', result[i][0], "Qtde:", result[i][1])

############

sqlOrigin =   """ 
            SELECT      ORIGIN, COUNT(ORIGIN)
            FROM        OLIST_CONSOLIDATE
            GROUP BY    ORIGIN
            HAVING      COUNT(ORIGIN) > 50
            ORDER BY    2 DESC
        """

res = conn.cursor()
res.execute(sqlOrigin)
result = res.fetchall()

print("\n****************************")
print("*** Best Origin ****")
print("****************************\n")

print('around "TOP LANDING PAGE", we can identify "organic_search" and "social media" as a good opportunity to invest.')
for i in range(0, len(result)):
    print(i, ')',result[i][0], '-',result[i][1]) if result[i][0] != 'nan' else ''

#######

sqlSdr =   """ 
            SELECT      ID_SDR, COUNT(*)
            FROM        OLIST_CONSOLIDATE
            WHERE       ID_SDR <> '00000000-0000-0000-0000-000000000000' 
            GROUP BY    ID_SDR
            ORDER BY    2 DESC
            LIMIT       10
        """

sqlSr =   """ 
            SELECT      ID_SR, COUNT(*)
            FROM        OLIST_CONSOLIDATE
            WHERE       ID_SR <> '00000000-0000-0000-0000-000000000000' 
            GROUP BY    ID_SR
            ORDER BY    2 DESC
            LIMIT       10
        """

res = conn.cursor()
res.execute(sqlSdr)
result = res.fetchall()

print("\n****************************")
print("*** TOP 10 SDR ****")
print("****************************\n")

for i in range(0, len(result)):
    print(i+1,')', result[i][0], '-', result[i][1])

res = conn.cursor()
res.execute(sqlSr)
result = res.fetchall()

print("\n****************************")
print("*** TOP 10 SR ****")
print("****************************\n")

for i in range(0, len(result)):
    print(i+1,')', result[i][0], '-', result[i][1])

#######

sqlBusiness =   """ 
            SELECT      BUSINESS_SEGMENT, COUNT(*)
            FROM        OLIST_CONSOLIDATE
            WHERE       BUSINESS_SEGMENT <> 'None' 
            AND         BUSINESS_SEGMENT <> '' 
            GROUP BY    BUSINESS_SEGMENT
            HAVING      COUNT(*) > 50
            ORDER BY    2 DESC
        """

res = conn.cursor()
res.execute(sqlBusiness)
result = res.fetchall()

print("\n****************************")
print("*** Best BUSINESS SEGMENT ****")
print("****************************\n")
print("ALL BUSINESS SEGMENT WITH MORE THAN 50 OCCURRENCES\n")

for i in range(0, len(result)):
    print(i+1,')', result[i][0], '-', result[i][1])

######
sqlConf =   """ 
            SELECT      DISTINCT(ID_MQL)
            FROM        OLIST_DEALS
            WHERE       ID_MQL NOT IN
                        (
                            SELECT      DISTINCT(ID_MQL)
                            FROM        OLIST_MQL
                        )
        """

res = conn.cursor()
res.execute(sqlConf)
result = res.fetchall()

print("\n****************************")
print("*** CONFERENCY REPORT ****")
print("****************************\n")
print("Just to know if any ID_MQL in contained in DEALS and not contained in MQL\n")

for i in range(0, len(result)):
    print(i+1,')', result[i][0])
