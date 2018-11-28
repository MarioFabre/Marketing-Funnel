import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# POSTGRES CONNECTION
conn = psycopg2.connect(
    "host=localhost dbname=postgres user=olist password=postgres")

sqlOrigin =   """ 
            SELECT      ORIGIN, COUNT(ORIGIN)
            FROM        OLIST_CONSOLIDATE
            GROUP BY    ORIGIN
            HAVING      COUNT(ORIGIN) < 200
            ORDER BY    2
        """

res = conn.cursor()
res.execute(sqlOrigin)
result = res.fetchall()

print("\n****************************")
print("*** Poor Origin ****")
print("****************************\n")

for i in range(0, len(result)):
    print(i+1, ')',result[i][0], '-', result[i][1])

#######

sqlSdr =   """ 
            SELECT      ID_SDR, COUNT(*)
            FROM        OLIST_CONSOLIDATE
            WHERE       ID_SDR <> '00000000-0000-0000-0000-000000000000' 
            GROUP BY    ID_SDR
            ORDER BY    2
            LIMIT       10
        """

sqlSr =   """ 
            SELECT      ID_SR, COUNT(*)
            FROM        OLIST_CONSOLIDATE
            WHERE       ID_SR <> '00000000-0000-0000-0000-000000000000' 
            GROUP BY    ID_SR
            ORDER BY    2
            LIMIT       10
        """

res = conn.cursor()
res.execute(sqlSdr)
result = res.fetchall()

print("\n****************************")
print("*** SDR poor frequency ****")
print("****************************\n")

for i in range(0, len(result)):
    print(i+1,')', result[i][0], '-', result[i][1])

res = conn.cursor()
res.execute(sqlSr)
result = res.fetchall()

print("\n****************************")
print("*** SR poor frequency****")
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
            HAVING      COUNT(*) < 50
            ORDER BY    2
        """

res = conn.cursor()
res.execute(sqlBusiness)
result = res.fetchall()

print("\n****************************")
print("*** Poor BUSINESS SEGMENT ****")
print("****************************\n")
print("ALL BUSINESS SEGMENT WITH MORE THAN 50 OCCURRENCES\n")

for i in range(0, len(result)):
    print(i+1,')', result[i][0], '-', result[i][1])

#########
sqlLPDown =   """ 
            SELECT      ID_LANDING_PAGE, COUNT(ID_LANDING_PAGE)
            FROM        OLIST_CONSOLIDATE
            GROUP BY    ID_LANDING_PAGE
            HAVING      COUNT(ID_LANDING_PAGE) < 10
            ORDER BY    2
        """

res = conn.cursor()
res.execute(sqlLPDown)
result = res.fetchall()

print("\n****************************")
print("*** Poor LANDING PAGE ****")
print("****************************\n")
print("That Landing pages listed below close deals below 10. So, it's important to know why and how much Olist is investing to keep it online. Is it worth?\n")

for i in range(0, len(result)):
    print(i+1,')', result[i][0], "-", result[i][1])

###########

sqlLandingPage =   """ 
            SELECT      DISTINCT(ID_LANDING_PAGE)
            FROM        OLIST_CONSOLIDATE
            WHERE       ID_LANDING_PAGE NOT IN  
                        (
                            SELECT      ID_LANDING_PAGE
                            FROM        OLIST_CONSOLIDATE
                            WHERE       ID_SELLER <> '00000000-0000-0000-0000-000000000000'
                        )
            ORDER BY    1
        """

sqlLandingCount =   """ 
            SELECT      COUNT(DISTINCT(ID_LANDING_PAGE))
            FROM        OLIST_CONSOLIDATE
            WHERE       ID_LANDING_PAGE NOT IN  
                        (
                            SELECT      ID_LANDING_PAGE
                            FROM        OLIST_CONSOLIDATE
                            WHERE       ID_SELLER <> '00000000-0000-0000-0000-000000000000'
                        )
            ORDER BY    1
        """

res = conn.cursor()
res.execute(sqlLandingCount)
result = res.fetchall()

print("\n****************************")
print("*** LANDING PAGE REPORT ****")
print("****************************")
print('\nIt is', result[0][0], 'landing Pages never used to close a deal. follow below:\n')

res = conn.cursor()
res.execute(sqlLandingPage)
result = res.fetchall()

for i in range(0, len(result)):
    print(i+1,')',result[i][0])
