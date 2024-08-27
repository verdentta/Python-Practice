#import pandas for data manipulation
import json
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

#import Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 

from selenium.webdriver.common.by import By 4
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

import time


# Step 1: Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",    # Replace with your host
    user="root",    # Replace with your username
    password="user",    # Replace with your password
    database="dhl_python"    # Replace with your database name
)

cursor = conn.cursor()

# Step 2: Clear the existing data in the table
cursor.execute("TRUNCATE TABLE converted_fuel_rates")


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

#let's go to a website where we can extract something 
driver.get("http://localhost:3000/index.php")

time.sleep(10) 

# Locate the table using the updated syntax
table = driver.find_element(By.XPATH, '//table[@border="1"]')

# Extract the table rows
rows = table.find_elements(By.TAG_NAME, 'tr')

# Initialize lists to store table data
fuel_type = []
rate = []
month = []

# Loop through the rows, skipping the header
for row in rows[1:]:  # Skip the header row
    cells = row.find_elements(By.TAG_NAME, 'td')
    fuel_type.append(cells[0].text)
    rate.append(int(cells[1].text))
    month.append(cells[2].text)

# Close the browser
driver.quit()

# Create a DataFrame with the extracted data
df = pd.DataFrame({
    'Fuel Type': fuel_type,
    'Rate (cents per liter)': rate,
    'Month': month
})

# Step 1: Load the conversion rate from currency_rates.txt
with open('currency_rates.txt', 'r') as file:
    currency_rates = json.load(file)

cad_to_eur = currency_rates['CAD_to_EUR']

# Step 2: Convert the rates from Canadian cents to Euros
# Since the rates are in cents, first convert them to dollars (by dividing by 100) and then apply the conversion rate
df['Rate (cents per liter)'] = (df['Rate (cents per liter)'] / 100) * cad_to_eur

# Rename the column to reflect the change
df.rename(columns={'Rate (cents per liter)': 'Rate (Euros per liter)'}, inplace=True)

# Display the DataFrame
print(df)

# Step 3: Insert the new data into the table
insert_query = """
    INSERT INTO converted_fuel_rates (fuel_type, rate_in_euros, report_month)
    VALUES (%s, %s, %s)
"""

# Convert the DataFrame rows to tuples and insert them
for index, row in df.iterrows():
    cursor.execute(insert_query, (row['Fuel Type'], row['Rate (Euros per liter)'], row['Month']))

# Commit the transaction
conn.commit()
print("Data committed Succesfully")

# Close the connection
cursor.close()

# Step 2: Fetch data from the tables
query_monthly_km = "SELECT fuel_type, km_driven, report_month FROM monthly_km_by_fuel_type"
query_fuel_rates = "SELECT fuel_type, rate_in_euros, report_month FROM converted_fuel_rates"

df_km = pd.read_sql(query_monthly_km, conn)
df_rates = pd.read_sql(query_fuel_rates, conn)

# Step 3: Merge the data on fuel_type and report_month
df_merged = pd.merge(df_km, df_rates, on=['fuel_type', 'report_month'])

# Step 4: Calculate the total money spent for each fuel type per month
df_merged['money_spent'] = df_merged['km_driven'] * df_merged['rate_in_euros']

# Step 5: Create Donut Charts for the past 3 months
# Get the unique months
months = df_merged['report_month'].sort_values().unique()[-3:]  # Last 3 months

for month in months:
    df_month = df_merged[df_merged['report_month'] == month]
    fuel_types = df_month['fuel_type']
    money_spent = df_month['money_spent']

    # Define a function to format the labels
    def money_format(value):
        return f'€{value:.2f}'

    # Plotting the donut chart
    plt.figure(figsize=(6, 6))
    plt.pie(money_spent, labels=fuel_types, autopct=lambda p: money_format(p * sum(money_spent) / 100),
            startangle=140, wedgeprops=dict(width=0.3))
    plt.title(f"Total Money Spent by Fuel Type in Euros - {month.strftime('%B %Y')}")
    plt.gca().add_artist(plt.Circle((0, 0), 0.70, color='white'))
    plt.show()

# Step 6: Close the connection
conn.close()

