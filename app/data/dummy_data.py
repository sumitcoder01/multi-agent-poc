# app/data/dummy_data.py

# A simple in-memory "database" of incidents.
incidents_db = {
    "INC-001": {
        "id": "INC-001",
        "title": "Unauthorized Server Access",
        "status": "Open",
        "priority": "High",
        "reporter": "Alice",
        "summary": "Suspicious login activity detected on the main production server after hours.",
    },
    "INC-002": {
        "id": "INC-002",
        "title": "Phishing Email Reported",
        "status": "Closed",
        "priority": "Medium",
        "reporter": "Bob",
        "summary": "User reported a phishing email containing a malicious link. The email was quarantined.",
    },
}

# A simple in-memory "database" of transactions.
transactions_db = {
    "TRN-101": {
        "id": "TRN-101",
        "amount": 1500.75,
        "currency": "USD",
        "status": "Completed",
        "source_account": "ACC-A1",
        "destination_account": "ACC-B1",
        "related_incident": "INC-001",
    },
    "TRN-102": {
        "id": "TRN-102",
        "amount": 99.99,
        "currency": "USD",
        "status": "Pending",
        "source_account": "ACC-C1",
        "destination_account": "ACC-D1",
        "related_incident": None,
    },
}

# A simple in-memory "database" of focal parties.
focal_parties_db = {
    "FP-ALICE": {
        "id": "FP-ALICE",
        "name": "Alice Anderson",
        "role": "System Administrator",
        "contact": "alice@example.com",
        "notes": "Reporter of incident INC-001. Key witness.",
    },
    "FP-BOB": {
        "id": "FP-BOB",
        "name": "Bob Brown",
        "role": "Account Manager",
        "contact": "bob@example.com",
        "notes": "Involved in transaction TRN-102.",
    },
}