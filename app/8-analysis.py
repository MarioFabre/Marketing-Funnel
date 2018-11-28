import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
import psycopg2

# POSTGRES CONNECTION
conn = psycopg2.connect(
    "host=localhost dbname=postgres user=olist password=postgres")

## SQL to cross best origin and all closed deals per origin
sqlOriginDeals =   """ 
            SELECT      L.ORIGIN, COUNT(D.ID_MQL)
            FROM        OLIST_DEALS D, OLIST_MQL L
            WHERE       L.ID_MQL = D.ID_MQL
            AND         L.ID_MQL IN
                        (            
                            SELECT      ID_MQL
                            FROM        OLIST_MQL
                            WHERE       ORIGIN IN
                                        (
                                            SELECT      ORIGIN
                                            FROM        OLIST_CONSOLIDATE
                                            GROUP BY    ORIGIN
                                            HAVING      COUNT(ORIGIN) > 50
                                        )
                        )
            GROUP BY    ORIGIN
            ORDER BY    2 DESC
        """

sqlOrigin =   """ 
            SELECT      ORIGIN, COUNT(ORIGIN)
            FROM        OLIST_CONSOLIDATE
            GROUP BY    ORIGIN
            HAVING      COUNT(ORIGIN) > 50
            ORDER BY    2 DESC
        """


resOriginDeals = conn.cursor()
resOriginDeals.execute(sqlOriginDeals)
resultOriginDeals = sorted(resOriginDeals.fetchall())

resOrigin = conn.cursor()
resOrigin.execute(sqlOrigin)
resultOrigin = sorted(resOrigin.fetchall())

x_labelsOriginDeals = list()
x_labelsOrigin = list()

frequenciesOriginDeals = list()
frequenciesOrigin = list()

for i in range(0, len(resultOriginDeals)):
    x_labelsOriginDeals.append(resultOriginDeals[i][0])
    frequenciesOriginDeals.append(resultOriginDeals[i][1])

for i in range(0, len(resultOrigin)):
    x_labelsOrigin.append(resultOrigin[i][0])
    frequenciesOrigin.append(resultOrigin[i][1])

fig, ax = plt.subplots(figsize=(14, 8))

index = np.arange(len(resultOriginDeals))
bar_width = 0.35

opacity = 0.9

rects1 = ax.bar(index, frequenciesOriginDeals, bar_width,
                alpha=opacity, color='gray',
                label='Closed Deals per Origin')

rects2 = ax.bar(index + bar_width, frequenciesOrigin, bar_width,
                alpha=opacity, color='blue',
                label='Top relevant Origin')

ax.set_xlabel('Origin')
ax.set_ylabel('Frequency')
ax.set_title('Best origin x Closed deals')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(x_labelsOriginDeals)
ax.set()
ax.legend()

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