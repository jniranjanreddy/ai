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

# Sample Dataset 2: Orders
# This DataFrame represents order details, linked by CustomerID
orders_data = {
    'OrderID': [101, 102, 103, 104, 105, 106],
    'CustomerID': [1, 2, 3, 2, 6, 3],  # Note: CustomerID 6 doesn't exist in customers for demonstrating outer joins
    'Product': ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse'],
    'Quantity': [1, 2, 1, 1, 3, 2],
    'Price': [1200, 800, 300, 200, 50, 30]
}
orders_df = pd.DataFrame(orders_data)

# Save to Excel file: orders.xlsx
orders_df.to_excel('orders.xlsx', index=False)
print("orders.xlsx generated successfully!")

# Sample Dataset 3: Products (for more complex joins)
# This can be joined with orders on Product, but we'll use it in practice code below
products_data = {
    'Product': ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse', 'Headphones'],
    'Category': ['Electronics', 'Electronics', 'Electronics', 'Accessories', 'Accessories', 'Accessories', 'Audio'],
    'Stock': [50, 100, 75, 200, 150, 300, 120]
}
products_df = pd.DataFrame(products_data)

# Save to a multi-sheet Excel file: inventory.xlsx
# Sheet 1: Products
# Sheet 2: Suppliers (another small dataset for practice)
suppliers_data = {
    'SupplierID': [1, 2, 3],
    'SupplierName': ['TechCorp', 'GadgetInc', 'AccessoryWorld'],
    'Product': ['Laptop', 'Phone', 'Keyboard']  # Links to products
}
suppliers_df = pd.DataFrame(suppliers_data)

with pd.ExcelWriter('inventory.xlsx') as writer:
    products_df.to_excel(writer, sheet_name='Products', index=False)
    suppliers_df.to_excel(writer, sheet_name='Suppliers', index=False)
print("inventory.xlsx generated successfully with multiple sheets!")