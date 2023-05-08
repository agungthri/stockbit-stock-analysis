import pandas as pd

# Replace the URL with the HTML page you want to read
url = 'data/BBCA_cash_flow.html'

# Read the HTML page and get a list of tables
tables = pd.read_html(url)

# If the page contains multiple tables, you can access them by their index
my_table = tables[0]
my_table['In Million'] = my_table['In Million'].str.replace('&nbsp', '')
# Print the first few rows of the table
print(my_table.T)
