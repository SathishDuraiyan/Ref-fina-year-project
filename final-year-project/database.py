import mysql.connector

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "database": "your_database"
}

# Function to establish a connection
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Function to create tables if they don't exist
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Table for Labour
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Labour (
            emp_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            dob DATE,
            age INT,
            skill_set VARCHAR(255),
            current_job VARCHAR(255)
        )
    """)

    # Table for Contractors
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Contractor (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            age INT,
            skill VARCHAR(255),
            company VARCHAR(255)
        )
    """)

    # Table for Job Posts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS JobPost (
            job_id INT AUTO_INCREMENT PRIMARY KEY,
            contractor_id INT,
            skill_required VARCHAR(255),
            salary DECIMAL(10,2),
            job_type VARCHAR(255),
            company_details VARCHAR(255),
            contact_details VARCHAR(255),
            FOREIGN KEY (contractor_id) REFERENCES Contractor(id)
        )
    """)

    # Table for Job Offers (Inbox)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS JobInbox (
            id INT AUTO_INCREMENT PRIMARY KEY,
            emp_id INT,
            job_id INT,
            status ENUM('Pending', 'Accepted', 'Rejected') DEFAULT 'Pending',
            FOREIGN KEY (emp_id) REFERENCES Labour(emp_id),
            FOREIGN KEY (job_id) REFERENCES JobPost(job_id)
        )
    """)

    conn.commit()
    conn.close()
