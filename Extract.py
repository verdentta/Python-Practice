#import pandas for data manipulation
import json
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

#import Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 

from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

import time

# MySQL connection setup
connection = mysql.connector.connect(
    host="localhost",  # Your host, e.g., 'localhost'
    user="root",       # Your MySQL username
    password="user",   # Your MySQL password (you've set it to '1234')
    database="dhl_python"  # Your database name
)

cursor = connection.cursor()

# Clear the table (truncate to remove all existing data)
truncate_query = "TRUNCATE TABLE converted_fuel_rates;"
cursor.execute(truncate_query)
connection.commit()

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

#let's go to a website where we can extract something 
driver.get("http://localhost:3000/index.php")

time.sleep(10) 

# Locate the table by its border attribute (you can also locate it by other attributes if needed)
table = driver.find_element(By.XPATH, "//table[@border='1']")

# Get all the rows from the table
rows = table.find_elements(By.TAG_NAME, "tr")

# Initialize a list to store the table data
table_data = []

# Iterate over the rows and extract the data
for row in rows:
    # Get all the cells in the row
    cells = row.find_elements(By.TAG_NAME, "td")
    # If there are cells, extract the text content and store it
    if len(cells) > 0:
        row_data = [cell.text for cell in cells]
        table_data.append(row_data)

time.sleep(5) 
driver.quit()

# Create a pandas DataFrame from the extracted data
df = pd.DataFrame(table_data, columns=["Fuel Type", "Rate (cents per liter)", "Month"])

# Convert the "Rate (cents per liter)" column to numeric
df["Rate (cents per liter)"] = pd.to_numeric(df["Rate (cents per liter)"])

# Load the conversion rate from currency_rates.txt
with open('currency_rates.txt', 'r') as file:
    currency_rates = json.load(file)

# Get the CAD to EUR conversion rate
cad_to_eur = currency_rates["CAD_to_EUR"]

# Convert the fuel rate from cents to euros
df["Rate (euros per liter)"] = df["Rate (cents per liter)"] * cad_to_eur / 100

# Display the DataFrame
print(df)

# Insert DataFrame values into the table
for index, row in df.iterrows():
    insert_query = """
    INSERT INTO converted_fuel_rates (fuel_type, rate_in_euros, report_month)
    VALUES (%s, %s, %s);
    """
    cursor.execute(insert_query, (row["Fuel Type"], row["Rate (euros per liter)"], row["Month"]))

# Commit the transaction to save changes
connection.commit()

# Fetch data from monthly_km_by_fuel_type and converted_fuel_rates tables
query = """
SELECT m.fuel_type, m.km_driven, c.rate_in_euros, c.report_month
FROM monthly_km_by_fuel_type m
JOIN converted_fuel_rates c
ON m.fuel_type = c.fuel_type AND m.report_month = c.report_month
WHERE c.report_month >= (SELECT MAX(report_month) FROM converted_fuel_rates) - INTERVAL 2 MONTH
ORDER BY c.report_month;
"""

df = pd.read_sql(query, connection)
print(df.head())
# Close the cursor and connection
cursor.close()
connection.close()

print("Data inserted successfully.")

# Calculate the amount of money spent (kilometers_driven * rate_in_euros)
df['money_spent'] = df['km_driven'] * df['rate_in_euros']

# Get the unique months
months = df['report_month'].unique()

# Create donut charts for each month
for month in months:
    # Filter data for the current month
    month_data = df[df['report_month'] == month]
    
    # Prepare data for the chart
    labels = month_data['fuel_type']
    sizes = month_data['money_spent']
    
    # Format the labels to show actual amounts in euros
    labels_with_amounts = [f"{label}: €{amount:,.2f}" for label, amount in zip(labels, sizes)]
    
    # Create a donut chart
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels_with_amounts, startangle=140, wedgeprops=dict(width=0.4), autopct=None)
    plt.title(f"Money Spent by Fuel Type - {month.strftime('%B %Y')}")
    
    # Draw the circle in the middle to make it a donut chart
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    plt.gca().add_artist(centre_circle)
    
    # Display the chart
    plt.show()

