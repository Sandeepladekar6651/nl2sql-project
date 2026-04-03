import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

DB_NAME = "clinic.db"

fake = Faker()


def create_connection():
    """Create SQLite connection."""
    return sqlite3.connect(DB_NAME)


def create_tables(conn):
    """Create database tables."""
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        date_of_birth DATE,
        gender TEXT,
        city TEXT,
        registered_date DATE
    );

    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        department TEXT,
        phone TEXT
    );

    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date DATETIME,
        status TEXT,
        notes TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(id)
    );

    CREATE TABLE IF NOT EXISTS treatments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        treatment_name TEXT,
        cost REAL,
        duration_minutes INTEGER,
        FOREIGN KEY(appointment_id) REFERENCES appointments(id)
    );

    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        invoice_date DATE,
        total_amount REAL,
        paid_amount REAL,
        status TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    );
    """)

    conn.commit()


def insert_doctors(conn):
    """Insert doctor records."""
    cursor = conn.cursor()

    specializations = [
        "Dermatology",
        "Cardiology",
        "Orthopedics",
        "General",
        "Pediatrics"
    ]

    doctors = []

    for _ in range(15):
        specialization = random.choice(specializations)

        doctors.append((
            fake.name(),
            specialization,
            specialization + " Department",
            fake.phone_number()
        ))

    cursor.executemany(
        "INSERT INTO doctors (name, specialization, department, phone) VALUES (?, ?, ?, ?)",
        doctors
    )

    conn.commit()
    return len(doctors)


def insert_patients(conn):
    """Insert patient records."""
    cursor = conn.cursor()

    cities = [
        "Mumbai", "Pune", "Delhi", "Bangalore",
        "Hyderabad", "Chennai", "Kolkata", "Nagpur"
    ]

    patients = []

    for _ in range(200):

        email = fake.email() if random.random() > 0.2 else None
        phone = fake.phone_number() if random.random() > 0.1 else None

        patients.append((
            fake.first_name(),
            fake.last_name(),
            email,
            phone,
            fake.date_of_birth(minimum_age=18, maximum_age=80),
            random.choice(["M", "F"]),
            random.choice(cities),
            fake.date_between(start_date="-3y", end_date="today")
        ))

    cursor.executemany("""
    INSERT INTO patients
    (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, patients)

    conn.commit()
    return len(patients)


def insert_appointments(conn):
    """Insert appointment records."""
    cursor = conn.cursor()

    statuses = ["Scheduled", "Completed", "Cancelled", "No-Show"]

    appointments = []

    for _ in range(500):

        appointment_date = fake.date_time_between(
            start_date="-12M",
            end_date="now"
        )

        notes = fake.sentence() if random.random() > 0.3 else None

        appointments.append((
            random.randint(1, 200),
            random.randint(1, 15),
            appointment_date,
            random.choice(statuses),
            notes
        ))

    cursor.executemany("""
    INSERT INTO appointments
    (patient_id, doctor_id, appointment_date, status, notes)
    VALUES (?, ?, ?, ?, ?)
    """, appointments)

    conn.commit()
    return len(appointments)


def insert_treatments(conn):
    """Insert treatment records."""
    cursor = conn.cursor()

    treatments = []

    for appointment_id in range(1, 351):

        treatments.append((
            appointment_id,
            random.choice([
                "Blood Test",
                "X-Ray",
                "MRI Scan",
                "Vaccination",
                "Consultation"
            ]),
            random.uniform(50, 5000),
            random.randint(10, 120)
        ))

    cursor.executemany("""
    INSERT INTO treatments
    (appointment_id, treatment_name, cost, duration_minutes)
    VALUES (?, ?, ?, ?)
    """, treatments)

    conn.commit()
    return len(treatments)


def insert_invoices(conn):
    """Insert invoice records."""
    cursor = conn.cursor()

    statuses = ["Paid", "Pending", "Overdue"]

    invoices = []

    for _ in range(300):

        total = round(random.uniform(100, 5000), 2)
        paid = total if random.random() > 0.3 else round(total * random.random(), 2)

        invoices.append((
            random.randint(1, 200),
            fake.date_between(start_date="-12M", end_date="today"),
            total,
            paid,
            random.choice(statuses)
        ))

    cursor.executemany("""
    INSERT INTO invoices
    (patient_id, invoice_date, total_amount, paid_amount, status)
    VALUES (?, ?, ?, ?, ?)
    """, invoices)

    conn.commit()
    return len(invoices)


def main():

    conn = create_connection()

    create_tables(conn)

    doctors = insert_doctors(conn)
    patients = insert_patients(conn)
    appointments = insert_appointments(conn)
    treatments = insert_treatments(conn)
    invoices = insert_invoices(conn)

    conn.close()

    print("\nDatabase created successfully!")
    print(f"Doctors inserted: {doctors}")
    print(f"Patients inserted: {patients}")
    print(f"Appointments inserted: {appointments}")
    print(f"Treatments inserted: {treatments}")
    print(f"Invoices inserted: {invoices}")


if __name__ == "__main__":
    main()