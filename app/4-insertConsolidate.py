import psycopg2

def watchDog(sMsg):
    print(sMsg)
    return

# REPLACE MISSING NUMBERS FROM NONE TO 0(ZERO)
def nan_values(number):
    return 0 if number == None or number == '' else number

# REPLACE MISSING GUIDs FROM NONE TO 0(ZERO)
def nan_guid(guid):
    return '00000000-0000-0000-0000-000000000000' if (guid == None or len(guid) < 36) else guid.strip()

# POSTGRES CONNECTION
watchDog('Postgres connecting')
conn = psycopg2.connect(
    "host=localhost dbname=postgres user=olist password=postgres")

# SQL TO LINK ALL INFORMATION FROM DEALS AND MQL
watchDog('SQL to link all information from closed deals and MQL')
res = conn.cursor()
res.execute("""SELECT       M.ID_MQL, M.DATE_FIRST_CONTACT, M.ID_LANDING_PAGE, M.ORIGIN,
                            D.ID_SELLER, D.ID_SDR, D.ID_SR, D.DATE_WON, D.BUSINESS_SEGMENT, 
                            D.TYPE_LEAD, D.LEAD_BEHAVIOUR_PROFILE, D.HAS_COMPANY, D.HAS_GTIN, D.AVERAGE_STOCK, 
                            D.TYPE_BUSINESS, D.DECLARED_PRODUCT_CATALOG_SIZE, D.DECLARED_MONTHLY_REVENUE
                FROM        OLIST_MQL M 
                LEFT JOIN   OLIST_DEALS D ON (M.ID_MQL = D.ID_MQL)
            ;""")
result = res.fetchall()

# INSERT LINKED DATA FROM OLIST_CONSOLIDATE TABLE
watchDog('Insert linked data from olist_consolidate table')
for row in result:
    cur = conn.cursor()
    
    insert = """INSERT INTO OLIST_CONSOLIDATE
                        (ID_MQL, DATE_FIRST_CONTACT, ID_LANDING_PAGE, ORIGIN, 
                        ID_SELLER, ID_SDR, ID_SR, DATE_WON, BUSINESS_SEGMENT, 
                        TYPE_LEAD, LEAD_BEHAVIOUR_PROFILE, HAS_COMPANY, HAS_GTIN, AVERAGE_STOCK, 
                        TYPE_BUSINESS, DECLARED_PRODUCT_CATALOG_SIZE, DECLARED_MONTHLY_REVENUE)
                    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s)""" % (
        row[0],
        row[1],
        row[2],
        row[3],
        nan_guid(row[4]),
        nan_guid(row[5]),
        nan_guid(row[6]),
        row[7],
        row[8],
        row[9],
        row[10],
        row[11],
        row[12],
        row[13],
        row[14],
        nan_values(row[15]),
        nan_values(row[16]))
    cur.execute(insert)

conn.commit()
conn.close()