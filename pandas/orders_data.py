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