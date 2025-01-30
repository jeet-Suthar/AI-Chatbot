import sqlite3

conn = sqlite3.connect('company.db')
cursor = conn.cursor()

# Create Employees table
cursor.execute('''
  CREATE TABLE IF NOT EXISTS Employees (
      ID INTEGER PRIMARY KEY,
      Name TEXT,
      Department TEXT,
      Salary INTEGER,
      Hire_Date DATE
  )
''')

# Create Departments table
cursor.execute('''
  CREATE TABLE IF NOT EXISTS Departments (
      ID INTEGER PRIMARY KEY,
      Name TEXT,
      Manager TEXT
  )
''')

# Insert sample data
employees = [
    ('Alice', 'Sales', 50000, '2021-01-15'),
    ('Bob', 'Engineering', 70000, '2020-06-10'),
    ('Charlie', 'Marketing', 60000, '2022-03-20')
]
cursor.executemany('INSERT INTO Employees (Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?)', employees)

departments = [
    ('Sales', 'Alice'),
    ('Engineering', 'Bob'),
    ('Marketing', 'Charlie')
]
cursor.executemany('INSERT INTO Departments (Name, Manager) VALUES (?, ?)', departments)

conn.commit()
conn.close()
