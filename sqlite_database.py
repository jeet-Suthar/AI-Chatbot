import sqlite3
from datetime import date
import random
import uuid

# Fix for Python 3.12 date handling
def adapt_date_iso(val):
    return val.isoformat()
sqlite3.register_adapter(date, adapt_date_iso)

def convert_date_iso(val):
    return date.fromisoformat(val.decode())
sqlite3.register_converter("DATE", convert_date_iso)

# Create database connection with type detection
conn = sqlite3.connect('company.db', detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()

# Create Departments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Departments (
        Dept_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Dept_Name TEXT NOT NULL UNIQUE,
        Manager_ID INTEGER,
        Budget REAL,
        Location TEXT,
        Established_Date DATE
    )
''')

# Create Employees table with proper constraints
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        Emp_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        First_Name TEXT NOT NULL,
        Last_Name TEXT NOT NULL,
        Dept_ID INTEGER,
        Position TEXT,
        Salary REAL,
        Hire_Date DATE,
        Email TEXT UNIQUE,
        Phone TEXT,
        FOREIGN KEY (Dept_ID) 
            REFERENCES Departments(Dept_ID) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE
    )
''')

# Insert Departments
departments = [
    ('Human Resources', 500000, 'New York', date(2015, 5, 1),),
    ('Sales', 1200000, 'Chicago', date(2010, 3, 15)),
    ('Engineering', 2500000, 'San Francisco', date(2012, 8, 1)),
    ('Marketing', 800000, 'Los Angeles', date(2018, 2, 10)),
    ('Finance', 1500000, 'Boston', date(2009, 11, 1)),
    ('IT', 900000, 'Austin', date(2016, 7, 1))
]

cursor.executemany('''
    INSERT INTO Departments (Dept_Name, Budget, Location, Established_Date)
    VALUES (?, ?, ?, ?)
''', departments)

# Generate unique emails
def generate_unique_email(first, last, existing_emails):
    base_email = f"{first[0].lower()}{last.lower()}"
    email = f"{base_email}@company.com"
    counter = 1
    
    while email in existing_emails:
        email = f"{base_email}{counter}@company.com"
        counter += 1
    
    return email

# Generate sample employees
first_names = ['James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 
              'Michael', 'Linda', 'David', 'Elizabeth', 'William', 'Barbara']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
             'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez']
positions = ['Manager', 'Developer', 'Analyst', 'Specialist', 'Coordinator',
            'Director', 'Engineer', 'Representative', 'Consultant', 'Associate']

def generate_employees(num):
    employees = []
    existing_emails = set()
    
    for _ in range(num):
        first = random.choice(first_names)
        last = random.choice(last_names)
        dept = random.randint(1, 6)
        position = random.choice(positions)
        salary = round(random.uniform(45000, 150000), 2)
        hire_date = date(random.randint(2015, 2023), random.randint(1,12), random.randint(1,28))
        email = generate_unique_email(first, last, existing_emails)
        existing_emails.add(email)
        phone = f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"
        
        employees.append((
            first, last, dept, position, salary,
            hire_date, email, phone
        ))
    return employees

# Insert employees with error handling
try:
    employees = generate_employees(30)
    cursor.executemany('''
        INSERT INTO Employees (
            First_Name, Last_Name, Dept_ID, Position,
            Salary, Hire_Date, Email, Phone
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', employees)
    conn.commit()
except sqlite3.Error as e:
    print(f"Database error: {e}")
finally:
    conn.close()

print("Database created successfully with 6 departments and 30 employees!")