import mysql.connector # type: ignore
from tkinter import Tk, Label, Entry, Button, messagebox
import hashlib

db__connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#Atchaya7",
    database="project"
)
cursor = db__connection.cursor()

def create_tables():
    # Create user_details table
    # Create user_details table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_details (
        user_id INT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(255) NOT NULL,
        height FLOAT,
        weight FLOAT,
        blood_pressure VARCHAR(10),
        sugar_level FLOAT,
        bmi FLOAT,
        water_intake FLOAT,
        diet_plan TEXT
    )
    """)


    # Create biological_details table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS biological_details (
        user_id INT,
        height FLOAT,
        weight FLOAT,
        blood_pressure VARCHAR(10),
        sugar_level FLOAT,
        bmi FLOAT,
        FOREIGN KEY (user_id) REFERENCES user_details(user_id) ON DELETE CASCADE
    )
    """)




    db__connection.commit()

# ... (other code remains unchanged)

def create_insert_trigger():
    # Drop the trigger if it exists
    cursor.execute("DROP TRIGGER IF EXISTS after_insert_user_details")
    
    # Create the insert trigger
    cursor.execute("""
    CREATE TRIGGER after_insert_user_details
    AFTER INSERT ON user_details
    FOR EACH ROW
    BEGIN
        INSERT INTO biological_details (user_id, height, weight, blood_pressure, sugar_level, bmi)
        VALUES (NEW.user_id, NEW.height, NEW.weight, NEW.blood_pressure, NEW.sugar_level, NEW.bmi);
    END
    """)

def create_delete_trigger():
    # Drop the trigger if it exists
    cursor.execute("DROP TRIGGER IF EXISTS after_delete_user_details")

    # Create the delete trigger with CASCADE option
    cursor.execute("""
    CREATE TRIGGER after_delete_user_details
    AFTER DELETE ON user_details
    FOR EACH ROW
    BEGIN
        DELETE FROM biological_details WHERE user_id = OLD.user_id;
    END
    """)





def insert_user_details(user_id, username, password, height, weight, blood_pressure, sugar_level):
    bmi = calculate_bmi(height, weight)
    water_intake = suggest_water_intake(weight)
    diet_plan = suggest_diet_plan(bmi)

    query = """
    INSERT INTO user_details 
    (user_id, username, password, height, weight, blood_pressure, sugar_level, bmi, water_intake, diet_plan) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        user_id, username, hash_password(password), height, weight, blood_pressure, sugar_level, bmi, water_intake, diet_plan))
    db__connection.commit()

def view_details_button_clicked():
    user_id = int(user_id_entry.get())
    user_details = get_user_details_by_id(user_id)
    if user_details:
        bmi_status = "Normal" if 18.5 <= user_details[7] < 24.9 else "Not Normal"
        water_intake_status = "Optimum" if user_details[8] >= suggest_water_intake(user_details[4]) else "Not Optimum"
        blood_pressure_status = "Optimum" if check_optimum_blood_pressure(user_details[5]) else "Not Optimum"
        sugar_level_status = "Optimum" if 80 <= user_details[6] <= 140 else "Not Optimum"

        details_message = (
            f"User ID: {user_details[0]}\n"
            f"Username: {user_details[1]}\n"
            f"Height: {user_details[3]}\n"
            f"Weight: {user_details[4]}\n"
            f"BMI: {user_details[7]} ({bmi_status})\n"
            f"Water Intake: {user_details[8]} ({water_intake_status})\n"
            f"Diet Plan: {user_details[9]}\n"
            f"Blood Pressure: {user_details[5]} ({blood_pressure_status})\n"
            f"Sugar Level: {user_details[6]} ({sugar_level_status})"
        )

        messagebox.showinfo("User Details", details_message)
    else:
        messagebox.showinfo("User Details", "User not found.")

def check_optimum_blood_pressure(blood_pressure):
    # Split the blood pressure into systolic and diastolic values
    systolic, diastolic = map(int, blood_pressure.split('/'))
    # Check if both systolic and diastolic values are within the normal range
    return 90 <= systolic <= 120 and 60 <= diastolic <= 80


def calculate_bmi(height, weight):
    bmi = weight / (height ** 2)
    return round(bmi, 2)

def suggest_water_intake(weight):
    water_intake = weight * 0.033
    return round(water_intake, 2)

def suggest_diet_plan(bmi):
    if bmi < 18.5:
        return "Underweight - Increase calorie intake with balanced nutrition."
    elif 18.5 <= bmi < 24.9:
        return "Normal weight - Maintain a balanced diet and exercise regularly."
    elif 25 <= bmi < 29.9:
        return "Overweight - Focus on portion control and increase physical activity."
    else:
        return "Obese - Consult with a healthcare professional for personalized advice."

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_details_by_id(user_id):
    query = "SELECT * FROM user_details WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    user_details = cursor.fetchone()
    return user_details

def submit_button_clicked():
    user_id = int(user_id_entry.get())
    username = username_entry.get()
    password = password_entry.get()
    height = float(height_entry.get())
    weight = float(weight_entry.get())
    blood_pressure = blood_pressure_entry.get()
    sugar_level = float(sugar_level_entry.get())

    insert_user_details(user_id, username, password, height, weight, blood_pressure, sugar_level)
    messagebox.showinfo("Success", "User details successfully stored!")

def view_details_button_clicked():
    user_id = int(user_id_entry.get())
    user_details = get_user_details_by_id(user_id)
    if user_details:
        bmi_status = "Normal" if 18.5 <= user_details[7] < 24.9 else "Not Normal"
        water_intake_status = "Optimum" if user_details[8] >= suggest_water_intake(user_details[4]) else "Not Optimum"
        blood_pressure_status = "Optimum" if "120/80" in user_details[5] else "Not Optimum"
        sugar_level_status = "Optimum" if 80 <= user_details[6] <= 140 else "Not Optimum"

        details_message = (
            f"User ID: {user_details[0]}\n"
            f"Username: {user_details[1]}\n"
            f"Height: {user_details[3]}\n"
            f"Weight: {user_details[4]}\n"
            f"BMI: {user_details[7]} ({bmi_status})\n"
            f"Water Intake: {user_details[8]} ({water_intake_status})\n"
            f"Diet Plan: {user_details[9]}\n"
            f"Blood Pressure: {user_details[5]} ({blood_pressure_status})\n"
            f"Sugar Level: {user_details[6]} ({sugar_level_status})"
        )

        messagebox.showinfo("User Details", details_message)
    else:
        messagebox.showinfo("User Details", "User not found.")

def delete_user_by_id():
    user_id = int(user_id_entry.get())

    try:
        # Delete related records from biological_details
        delete_biological_query = "DELETE FROM biological_details WHERE user_id = %s"
        cursor.execute(delete_biological_query, (user_id,))
        
        # Delete the user from user_details
        delete_user_query = "DELETE FROM user_details WHERE user_id = %s"
        cursor.execute(delete_user_query, (user_id,))

        db__connection.commit()
        messagebox.showinfo("Success", "User deleted successfully!")
    except mysql.connector.Error as err:
        # Handle the error
        messagebox.showerror("Error", f"Error deleting user: {err}")



def view_my_details_button_clicked():
    user_id = int(user_id_entry.get())
    user_details = get_user_details_by_id(user_id)
    if user_details:
        bmi_status = "Normal" if 18.5 <= user_details[7] < 24.9 else "Not Normal"
        water_intake_status = "Optimum" if user_details[8] >= suggest_water_intake(user_details[4]) else "Not Optimum"
        blood_pressure_status = "Optimum" if "120/80" in user_details[5] else "Not Optimum"
        sugar_level_status = "Optimum" if 80 <= user_details[6] <= 140 else "Not Optimum"

        details_message = (
            f"User ID: {user_details[0]}\n"
            f"Username: {user_details[1]}\n"
            f"Height: {user_details[3]}\n"
            f"Weight: {user_details[4]}\n"
            f"BMI: {user_details[7]} ({bmi_status})\n"
            f"Water Intake: {user_details[8]} ({water_intake_status})\n"
            f"Diet Plan: {user_details[9]}\n"
            f"Blood Pressure: {user_details[5]} ({blood_pressure_status})\n"
            f"Sugar Level: {user_details[6]} ({sugar_level_status})"
        )

        messagebox.showinfo("My Details", details_message)
    else:
        messagebox.showinfo("My Details", "User not found.")

if __name__ == "__main__":
    create_tables()
    create_insert_trigger()
    create_delete_trigger()

    # Example: Insert an admin user with user_id 1, username "admin_username", password "admin_password", and action_status "active"

    root = Tk()
    root.title("Health Information System")

    user_id_label = Label(root, text="User ID:")
    username_label = Label(root, text="Username:")
    password_label = Label(root, text="Password:")
    height_label = Label(root, text="Height (meters):")
    weight_label = Label(root, text="Weight (kg):")
    blood_pressure_label = Label(root, text="Blood Pressure:")
    sugar_level_label = Label(root, text="Sugar Level:")

    user_id_entry = Entry(root)
    username_entry = Entry(root)
    password_entry = Entry(root, show="*")
    height_entry = Entry(root)
    weight_entry = Entry(root)
    blood_pressure_entry = Entry(root)
    sugar_level_entry = Entry(root)

    submit_button = Button(root, text="Submit", command=submit_button_clicked)
    view_details_button = Button(root, text="View Details", command=view_details_button_clicked)
    delete_button = Button(root, text="Delete User", command=delete_user_by_id)
    view_my_details_button = Button(root, text="View My Details", command=view_my_details_button_clicked)

    user_id_label.grid(row=0, column=0)
    user_id_entry.grid(row=0, column=1)
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1)
    height_label.grid(row=3, column=0)
    height_entry.grid(row=3, column=1)
    weight_label.grid(row=4, column=0)
    weight_entry.grid(row=4, column=1)
    blood_pressure_label.grid(row=5, column=0)
    blood_pressure_entry.grid(row=5, column=1)
    sugar_level_label.grid(row=6, column=0)
    sugar_level_entry.grid(row=6, column=1)

    submit_button.grid(row=7, column=0, columnspan=2, pady=10)
    view_details_button.grid(row=8, column=0, columnspan=2, pady=10)
    delete_button.grid(row=9, column=0, columnspan=2, pady=10)

    root.mainloop()

    cursor.close()
    db__connection.close()
    