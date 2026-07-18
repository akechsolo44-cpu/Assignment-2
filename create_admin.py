import sqlite3

conn = sqlite3.connect("campuswear.db")
cursor = conn.cursor()

username = "ama.malcolmxtra"
email = "ama21177@campuswear.com"
password = "sudo211"
role = "admin"

try:

    cursor.execute(
        """
        INSERT INTO users
        (username, email, password, role)
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            email,
            password,
            role
        )
    )

    conn.commit()

    print("Admin account created successfully!")

except sqlite3.IntegrityError:

    print("Admin account already exists.")

conn.close()