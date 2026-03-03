from modules.database import run_query

data = run_query("SELECT * FROM sales LIMIT 1;")

print("Column Names:")
print(data.columns)

print("\nSample Row:")
print(data)