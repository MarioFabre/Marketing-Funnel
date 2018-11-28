import numpy as np
import matplotlib.pyplot as plt
import psycopg2

# POSTGRES CONNECTION
conn = psycopg2.connect(
    "host=localhost dbname=postgres user=olist password=postgres")

##SQL NOT USED
sql2017FirstC =   """ 
            SELECT      Extract('month' from CAST(DATE_FIRST_CONTACT as timestamp)), 
                        COUNT(Extract('month' from CAST(DATE_FIRST_CONTACT as timestamp))) 
            FROM        OLIST_MQL
            WHERE       Extract('YEAR' from CAST(DATE_FIRST_CONTACT as timestamp)) = 2017
            GROUP BY    Extract('month' from CAST(DATE_FIRST_CONTACT as timestamp))
            ORDER BY    1
        """

##SQL NOT USED
sql2017WonDeal =   """ 
            SELECT      Extract('month' from CAST(DATE_WON as timestamp)), 
                        COUNT(Extract('month' from CAST(DATE_WON as timestamp))) 
            FROM        OLIST_DEALS
            WHERE       Extract('YEAR' from CAST(DATE_WON as timestamp)) = 2017
            AND         Extract('month' from CAST(DATE_WON as timestamp)) <= 5
            GROUP BY    Extract('month' from CAST(DATE_WON as timestamp))
            ORDER BY    1
        """
## SQL TO GET ALL GENERATE QUALIFIED LEADS PER MONTH
sql2018FirstC =   """ 
            SELECT      Extract('month' from CAST(DATE_FIRST_CONTACT as timestamp)), 
                        COUNT(Extract('month' from CAST(DATE_FIRST_CONTACT as timestamp))) 
            FROM        OLIST_CONSOLIDATE
            WHERE       Extract('YEAR' from CAST(DATE_FIRST_CONTACT as timestamp)) = 2018
            GROUP BY    Extract('month' from CAST(DATE_FIRST_CONTACT as timestamp))
            ORDER BY    1
        """

## SQL TO GET ALL GENERATE CLOSED DEALS PER MONTH. IT WAS LIMITED FIRST 5 MONTHS DUE TO MQL REGISTRY JUST CONTAIN FIRST 5 MONTHS IN 2018
sql2018WonDeal =   """ 
            SELECT      Extract('month' from CAST(DATE_WON as timestamp)), 
                        COUNT(Extract('month' from CAST(DATE_WON as timestamp))) 
            FROM        OLIST_DEALS
            WHERE       Extract('YEAR' from CAST(DATE_WON as timestamp)) = 2018
            AND         Extract('month' from CAST(DATE_WON as timestamp)) <= 5
            GROUP BY    Extract('month' from CAST(DATE_WON as timestamp))
            ORDER BY    1
        """

resFirstC = conn.cursor()
resFirstC.execute(sql2018FirstC)
resultFirstC = resFirstC.fetchall()

resWonDeal = conn.cursor()
resWonDeal.execute(sql2018WonDeal)
resultWonDeal = resWonDeal.fetchall()

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

x_labelsFirstC = list()
x_labelsWonDeal = list()

frequenciesFirstC = list()
frequenciesWonDeal = list()

# lOAD SELECT RESULTS IN LIST VARIABLE
for i in range(0, len(resultFirstC)):
    x_labelsFirstC.append(resultFirstC[i][0])
    frequenciesFirstC.append(resultFirstC[i][1])

# lOAD SELECT RESULTS IN LIST VARIABLE
for i in range(0, len(resultWonDeal)):
    x_labelsWonDeal.append(resultWonDeal[i][0])
    frequenciesWonDeal.append(resultWonDeal[i][1])

fig, ax = plt.subplots(figsize=(14, 8))

index = np.arange(len(resultFirstC))
bar_width = 0.25

opacity = 0.9

rects1 = ax.bar(index, frequenciesFirstC, bar_width,
                alpha=opacity, color='blue',
                label='All Qualified Lead per Month')

rects2 = ax.bar(index + bar_width, frequenciesWonDeal, bar_width,
                alpha=opacity, color='grey',
                label='All Closed Deal per Month')

ax.set_xlabel('Months')
ax.set_ylabel('Frequency')
ax.set_title('Quantity Qualified Lead x Quantity Closed deals')
ax.set_xticks(index + bar_width / 2)

for i in range(0, len(x_labelsFirstC)):
    x_labelsFirstC[i] = switch_month(x_labelsFirstC[i])

ax.set_xticklabels(x_labelsFirstC)
ax.legend(loc='upper center', shadow=True)

rects = ax.patches

fig.tight_layout()

for rect in rects:
    # Get X and Y placement of label from rect.
    y_value = rect.get_height()
    x_value = rect.get_x() + rect.get_width() / 2

    # Use Y value as label and format number with one decimal place
    label = "{:.1f}".format(y_value)

    # Create annotation
    plt.annotate(label,(x_value, y_value),xytext=(0, 5),textcoords="offset points",ha='center',va='bottom') 
plt.show()