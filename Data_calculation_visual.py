import mysql.connector
import pandas as pd

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="user",
    database="dhl_python"
)
cursor = conn.cursor()

# Fetch kilometers driven by fuel type
query_km_by_route = """
SELECT fuel_type, route, km_driven, report_month 
FROM monthly_km_by_fuel_type 
WHERE report_month >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
"""
km_by_route_df = pd.read_sql(query_km_by_route, conn)

# Close the database connection
cursor.close()
conn.close()

print(km_by_route_df)