import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# POSTGRES CONNECTION
conn = psycopg2.connect(
    "host=localhost dbname=postgres user=olist password=postgres")

# SELECT TOTAL QUALIFIED LEADS PER MONTH (NOT USED)
sql2017 =   """ 
            SELECT      Extract('month' from CAST(DATE_FIRST_CONTACT as timestamp)), 
                        COUNT(Extract('month' from CAST(DATE_FIRST_CONTACT as timestamp))) 
            FROM        OLIST_MQL
            WHERE       Extract('YEAR' from CAST(DATE_FIRST_CONTACT as timestamp)) = 2017
            GROUP BY    Extract('month' from CAST(DATE_FIRST_CONTACT as timestamp))
            ORDER BY    1
        """

# SELECT TOTAL QUALIFIED LEADS PER MONTH
sql2018 =   """ 
            SELECT      Extract('month' from CAST(DATE_FIRST_CONTACT as timestamp)), 
                        COUNT(Extract('month' from CAST(DATE_FIRST_CONTACT as timestamp))) 
            FROM        OLIST_MQL
            WHERE       Extract('YEAR' from CAST(DATE_FIRST_CONTACT as timestamp)) = 2018
            GROUP BY    Extract('month' from CAST(DATE_FIRST_CONTACT as timestamp))
            ORDER BY    1
        """

res = conn.cursor()
res.execute(sql2018)
result = res.fetchall()

def switch_month(argument):
    switcher = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return switcher.get(argument, "Invalid month")

x_labels = list()
frequencies = list()

# lOAD SELECT RESULTS IN LIST VARIABLE
for i in range(0, len(result)):
    x_labels.append(result[i][0])
    frequencies.append(result[i][1])

freq_series = pd.Series(frequencies)

# Plot the figure.
plt.figure(figsize=(12, 8))
ax = freq_series.plot(kind='bar')
ax.set_title('Qualified Leads per Month - 2018')
ax.set_xlabel('Month')
ax.set_ylabel('Quantity')

## REPLACE NUMBERS TO STRING
for i in range(0, len(x_labels)):
    x_labels[i] = switch_month(x_labels[i])

ax.set_xticklabels(x_labels, rotation=0)

rects = ax.patches

# For each bar: Place a label
for rect in rects:
    # Get X and Y placement of label from rect.
    y_value = rect.get_height()
    x_value = rect.get_x() + rect.get_width() / 2

    # Use Y value as label and format number with one decimal place
    label = "{:.1f}".format(y_value)

    # Create annotation
    plt.annotate(label,(x_value, y_value),xytext=(0, 5),textcoords="offset points",ha='center',va='bottom') 

plt.show()