# seed_database.py

import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse # <-- Import the URL parsing library

def setup_database():
    """
    Connects to the PostgreSQL database, drops existing tables,
    creates new tables, and inserts sample data for testing.
    """
    print("--- Starting database setup script ---")

    # 1. Load configuration from .env file
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("!!! ERROR: DATABASE_URL not found in .env file. Aborting. !!!")
        return
        
    # --- THIS IS THE CRITICAL CHANGE ---
    # The langchain format is "postgresql+psycopg2://...".
    # The psycopg2 library itself expects "postgresql://..." or a DSN string.
    # We will make it compatible by removing the "+psycopg2".
    if "postgresql+psycopg2://" in database_url:
        compatible_url = database_url.replace("postgresql+psycopg2://", "postgresql://")
    else:
        compatible_url = database_url

    conn = None
    try:
        # 2. Connect to the database using the compatible URL
        print(f"Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(compatible_url)
        cur = conn.cursor()
        print("Connection successful.")

        # 3. Drop existing tables (no changes needed from here)
        print("Dropping old tables (if they exist)...")
        cur.execute("DROP TABLE IF EXISTS transactions CASCADE;")
        cur.execute("DROP TABLE IF EXISTS incidents CASCADE;")
        cur.execute("DROP TABLE IF EXISTS focal_parties CASCADE;")
        print("Old tables dropped.")

        # 4. Create the new tables
        print("Creating new tables: focal_parties, incidents, transactions...")
        cur.execute("""
            CREATE TABLE focal_parties (
                id INT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                role VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                notes TEXT
            );
        """)
        cur.execute("""
            CREATE TABLE incidents (
                id VARCHAR(20) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                status VARCHAR(50),
                priority VARCHAR(50),
                reporter_id INT,
                summary TEXT,
                reported_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                FOREIGN KEY (reporter_id) REFERENCES focal_parties(id)
            );
        """)
        cur.execute("""
            CREATE TABLE transactions (
                id VARCHAR(20) PRIMARY KEY,
                amount NUMERIC(10, 2) NOT NULL,
                currency VARCHAR(10),
                status VARCHAR(50),
                source_party_id INT,
                destination_party_id INT,
                related_incident_id VARCHAR(20),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                FOREIGN KEY (source_party_id) REFERENCES focal_parties(id),
                FOREIGN KEY (destination_party_id) REFERENCES focal_parties(id),
                FOREIGN KEY (related_incident_id) REFERENCES incidents(id)
            );
        """)
        print("Tables created successfully.")

        # 5. Insert sample data (no changes needed here)
        print("Inserting sample data...")
        cur.execute("""
            INSERT INTO focal_parties (id, full_name, role, email, notes) VALUES
            (1, 'Alice Anderson', 'System Administrator', 'alice@example.com', 'Key witness for incident INC-001.'),
            (2, 'Bob Brown', 'Account Manager', 'bob@example.com', 'Involved in transaction TRN-102.'),
            (3, 'Charlie Clark', 'Compliance Officer', 'charlie@example.com', 'Oversaw the resolution of INC-002.');
        """)
        cur.execute("""
            INSERT INTO incidents (id, title, status, priority, reporter_id, summary) VALUES
            ('INC-001', 'Unauthorized Server Access', 'Open', 'High', 1, 'Suspicious login activity detected on the main production server.'),
            ('INC-002', 'Phishing Email Reported', 'Closed', 'Medium', 2, 'User reported a phishing email. The email was quarantined.');
        """)
        cur.execute("""
            INSERT INTO transactions (id, amount, currency, status, source_party_id, destination_party_id, related_incident_id) VALUES
            ('TRN-101', 1500.75, 'USD', 'Completed', 1, 2, 'INC-001'),
            ('TRN-102', 99.99, 'USD', 'Pending', 2, 3, NULL),
            ('TRN-103', 250.00, 'EUR', 'Completed', 3, 1, 'INC-002');
        """)
        print("Sample data inserted.")
        
        # 6. Commit and close
        conn.commit()
        print("--- Database setup complete and changes committed! ---")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"!!! ERROR: An error occurred during database setup: {error} !!!")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    setup_database()