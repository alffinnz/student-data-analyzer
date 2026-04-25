import sqlite3
import csv

# connect database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    maths INTEGER,
    science INTEGER,
    english INTEGER
)
""")
conn.commit()


# 🔹 Load CSV into DB
def load_csv():
    file_name = input("Enter CSV file name (with .csv): ")

    try:
        cursor.execute("DELETE FROM students")

        with open(file_name, "r") as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                name = row[0]
                maths = int(row[1])
                science = int(row[2])
                english = int(row[3])

                cursor.execute(
                    "INSERT INTO students (name, maths, science, english) VALUES (?, ?, ?, ?)",
                    (name, maths, science, english)
                )

        conn.commit()
        print("Data loaded successfully!")

    except FileNotFoundError:
        print("File not found.")


# 🔹 Show all students
def show_all():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    if not rows:
        print("\nNo data. Load CSV first.")
        return

    print("\n--- ALL STUDENTS ---")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Marks: {row[2]}, {row[3]}, {row[4]}")


# 🔹 Top student
def top_student():
    cursor.execute("""
    SELECT name, (maths + science + english) AS total
    FROM students
    ORDER BY total DESC
    LIMIT 1
    """)

    top = cursor.fetchone()

    if not top:
        print("\nNo data. Load CSV first.")
        return

    print("\nTop Student:", top)


# 🔹 Failed students
def failed_students():
    cursor.execute("""
    SELECT name
    FROM students
    WHERE (maths + science + english)/3.0 < 50
    """)

    failed = cursor.fetchall()

    print("\nFailed Students:")
    for f in failed:
        print(f[0])


# 🔹 Class average
def class_average():
    cursor.execute("""
    SELECT AVG((maths + science + english)/3.0)
    FROM students
    """)

    avg = cursor.fetchone()

    if not avg or avg[0] is None:
        print("\nNo data. Load CSV first.")
        return

    print("\nClass Average:", round(avg[0], 2))


# 🔹 Menu
def main():
    while True:
        print("\n--- MENU ---")
        print("1. Load CSV into Database")
        print("2. Show All Students")
        print("3. Show Top Student")
        print("4. Show Failed Students")
        print("5. Show Class Average")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            load_csv()
        elif choice == "2":
            show_all()
        elif choice == "3":
            top_student()
        elif choice == "4":
            failed_students()
        elif choice == "5":
            class_average()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice")


# run app
main()

# close DB
conn.close()