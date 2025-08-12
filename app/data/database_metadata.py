DATABASE_METADATA = """## Database Schema
This database tracks incidents, transactions, and the people involved (focal_parties).

### Tables
- `focal_parties`(id, full_name, role, email): Stores information about individuals. The central "who" table.
- `i- To find an incident's reporter: JOIN `incidents.reporter_id` ON `focal_parties.id`.
- To find people in a transaction: JOIN `transactions.source_party_id` or `destination_party_id` ON `focal_parties.id`.
- To find a transaction for an incident: JOIN `transactions.related_incident_id` ON `incidents.id`.
ncidents`(id, title, status, priority, reporter_id): Stores information about reported security or operational events.
- `transactions`(id, amount, status, source_party_id, destination_party_id, related_incident_id): Stores information about financial transfers.

### Key Joins
"""