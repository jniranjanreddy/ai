import pandas as pd

# Sample Dataset 1: Customers
# This DataFrame represents customer information
customers_data = {
    'CustomerID': [1, 2, 3, 4, 5],
    'Name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'David Lee', 'Eva Martinez'],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'Age': [28, 35, 42, 31, 29]
}
customers_df = pd.DataFrame(customers_data)

# Save to Excel file: customers.xlsx
customers_df.to_excel('customers.xlsx', index=False)
print("customers.xlsx generated successfully!")