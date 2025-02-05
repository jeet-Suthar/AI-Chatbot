import sqlite3

def update_manager(dept_id, emp_id):
    """
    Update the Manager_ID for a department in the Departments table.
    
    Args:
        dept_id (int): The ID of the department to update.
        emp_id (int): The ID of the employee to set as the manager.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()

        # Check if the employee exists
        cursor.execute("SELECT Emp_ID FROM Employees WHERE Emp_ID = ?", (emp_id,))
        if not cursor.fetchone():
            print(f"Error: Employee with ID {emp_id} does not exist.")
            return

        # Check if the department exists
        cursor.execute("SELECT Dept_ID FROM Departments WHERE Dept_ID = ?", (dept_id,))
        if not cursor.fetchone():
            print(f"Error: Department with ID {dept_id} does not exist.")
            return

        # Update the Manager_ID in the Departments table
        cursor.execute('''
            UPDATE Departments
            SET Manager_ID = ?
            WHERE Dept_ID = ?
        ''', (emp_id, dept_id))

        # Commit the changes
        conn.commit()
        print(f"Success: Manager for Department ID {dept_id} updated to Employee ID {emp_id}.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        # Close the connection
        conn.close()

#

