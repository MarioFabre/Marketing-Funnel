import psycopg2
import matplotlib.pyplot as plt
import pandas as pd

# POSTGRES CONNECTION
conn = psycopg2.connect(
    "host=localhost dbname=postgres user=olist password=postgres")

# SELECT ORIGIN AND YOUR RESPECTIVE QUANTITY
resOrigin = conn.cursor()
resOrigin.execute("SELECT ORIGIN, COUNT(ORIGIN) FROM OLIST_CONSOLIDATE GROUP BY ORIGIN ORDER BY 2 DESC;")
resultOrigin = resOrigin.fetchall()

# SELECT JUST TO COUNT ALL DIFERENT TYPE OF ORIGIN
resCount = conn.cursor()
resCount.execute("SELECT COUNT(DISTINCT(ORIGIN)) FROM OLIST_CONSOLIDATE;")
resultCount = resCount.fetchall()
count_origin_type = resultCount[0][0]

x_labels = list()
frequencies = list()

# lOAD SELECT RESULTS IN LIST VARIABLE
for i in range(0, count_origin_type):
    x_labels.append(resultOrigin[i][0])
    frequencies.append(resultOrigin[i][1])

freq_series = pd.Series(frequencies)

# Plot the figure.
plt.figure(figsize=(12, 8))
ax = freq_series.plot(kind='bar')
ax.set_title('All origin and respective quantity')
ax.set_xlabel('Origin')
ax.set_ylabel('Quantity')
ax.set_xticklabels(x_labels, rotation=10)

rects = ax.patches

# For each bar: Place a label
for rect in rects:
    # Get X and Y placement of label from rect.
    y_value = rect.get_height()
    x_value = rect.get_x() + rect.get_width() / 2

    # Use Y value as label and format number with one decimal place
    label = "{:.1f}".format(y_value)

    # Create annotation
    plt.annotate(label, (x_value, y_value), xytext=(0, 5), textcoords="offset points",ha='center', va='bottom')

plt.show()
conn.close()