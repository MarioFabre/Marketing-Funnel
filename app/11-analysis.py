import numpy as np
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# POSTGRES CONNECTION
conn = psycopg2.connect(
    "host=localhost dbname=postgres user=olist password=postgres")

## SQL to get all closed deal separated by week day
sql2017 =   """ 
                SELECT 
                    CASE EXTRACT( 'DOW' FROM CAST(DATE_WON as timestamp))
                        WHEN 0 THEN 'Domingo'
                        WHEN 1 THEN 'Segunda-Feira'
                        WHEN 2 THEN 'Terca-Feira'
                        WHEN 3 THEN 'Quarta-Feira'
                        WHEN 4 THEN 'Quinta-Feira'
                        WHEN 5 THEN 'Sexta-Feira'
                        WHEN 6 THEN 'Sabado'
                    END,
                    Count(*)
                FROM OLIST_DEALS
                GROUP BY 1
        """

res = conn.cursor()
res.execute(sql2017)
result = res.fetchall()

x_labels = list()
frequencies = list()

for i in range(0, len(result)):
    x_labels.append(result[i][0])
    frequencies.append(result[i][1])

freq_series = pd.Series(frequencies)

# Plot the figure.
plt.figure(figsize=(12, 8))
ax = freq_series.plot(kind='bar')
ax.set_title('Total closed deals per week day')
ax.set_xlabel('Week Day')
ax.set_ylabel('Quantity')
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