import psycopg2

conn = psycopg2.connect(
    "host=localhost dbname=postgres user=olist password=postgres")

# CREATE EXTENSION TO GENERATE NEW GUID
cur = conn.cursor() 
cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

# DROP TABLE BEFORE CREATING IT
cur = conn.cursor() 
cur.execute('DROP TABLE IF EXISTS OLIST_DEALS;')

# DROP TABLE BEFORE CREATING IT
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS OLIST_MQL;')

# DROP TABLE BEFORE CREATING IT
cur = conn.cursor() 
cur.execute('DROP TABLE IF EXISTS OLIST_CONSOLIDATE;')

# CREATE TABLE TO STORE ALL INFORMATION FROM olist_marketing_qualified_leads_dataset.csv WITHOUT ANY TRANSFORMATION
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS OLIST_MQL
            (
                CODE_MQL UUID DEFAULT uuid_generate_v1() PRIMARY KEY,
                ID_MQL UUID NOT NULL, 
                DATE_FIRST_CONTACT VARCHAR (10) NOT NULL, 
                ID_LANDING_PAGE UUID NOT NULL, 
                ORIGIN VARCHAR (100) NOT NULL, 
                INSERTED_DATE timestamp default current_timestamp
            );""")

# CREATE TABLE TO STORE ALL INFORMATION FROM olist_closed_deals_dataset.csv WITHOUT ANY TRANSFORMATION
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS OLIST_DEALS
            (
                CODE_DEALS UUID DEFAULT uuid_generate_v1() PRIMARY KEY,
                ID_MQL UUID NOT NULL, 
                ID_SELLER UUID NOT NULL, 
                ID_SDR UUID NOT NULL, 
                ID_SR UUID NOT NULL, 
                DATE_WON VARCHAR (20) NOT NULL,
                BUSINESS_SEGMENT VARCHAR (100) NOT NULL,
                TYPE_LEAD VARCHAR (50) NULL,
                LEAD_BEHAVIOUR_PROFILE VARCHAR (20) NULL,
                HAS_COMPANY VARCHAR (8) NULL,
                HAS_GTIN VARCHAR (8) NULL,
                AVERAGE_STOCK VARCHAR (10) NULL,
                TYPE_BUSINESS VARCHAR (20) NULL,
                DECLARED_PRODUCT_CATALOG_SIZE INT NULL,
                DECLARED_MONTHLY_REVENUE INT NULL,
                INSERTED_DATE timestamp default current_timestamp
            );""")
conn.commit()

# CREATE TABLE TO LINK ALL INFORMATION FROM olist_marketing_qualified_leads_dataset.csv AND olist_closed_deals_dataset.csv
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS OLIST_CONSOLIDATE
            (
                CODE_CONSOLIDATE UUID DEFAULT uuid_generate_v1() PRIMARY KEY,
                ID_MQL UUID NOT NULL, 
                DATE_FIRST_CONTACT VARCHAR (10) NOT NULL, 
                ID_LANDING_PAGE UUID NOT NULL, 
                ORIGIN VARCHAR (100) NOT NULL, 
                ID_SELLER UUID NOT NULL, 
                ID_SDR UUID NOT NULL, 
                ID_SR UUID NOT NULL, 
                DATE_WON VARCHAR (20) NOT NULL,
                BUSINESS_SEGMENT VARCHAR (100) NOT NULL,
                TYPE_LEAD VARCHAR (50) NULL,
                LEAD_BEHAVIOUR_PROFILE VARCHAR (20) NULL,
                HAS_COMPANY VARCHAR (8) NULL,
                HAS_GTIN VARCHAR (8) NULL,
                AVERAGE_STOCK VARCHAR (10) NULL,
                TYPE_BUSINESS VARCHAR (20) NULL,
                DECLARED_PRODUCT_CATALOG_SIZE INT NULL,
                DECLARED_MONTHLY_REVENUE INT NULL,
                INSERTED_DATE timestamp default current_timestamp
            );""")
conn.commit()

conn.close()
