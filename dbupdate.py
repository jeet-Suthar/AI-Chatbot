import sqlite3

def update_manager(dept_id, manager_id):
    """Updates the Manager_ID for a specific department."""
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()

    query = "UPDATE Departments SET Manager_ID = ? WHERE Dept_ID = ?"
    cursor.execute(query, (manager_id, dept_id))
    conn.commit()

    print(f"Updated Manager_ID for Department {dept_id} to {manager_id}.")
    conn.close()
update_manager(6,28)