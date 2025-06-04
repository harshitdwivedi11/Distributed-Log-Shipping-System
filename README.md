# Distributed Log Shipping System

A robust, scalable system for collecting logs from distributed clients and forwarding them to a central server for aggregation, monitoring, and analysis.

---

## Features

- **Reliable Log Shipping:** Ensures each log is sent exactly once from client to server.
- **Supports Multiple Clients:** Easily add new clients to ship logs from various sources.
- **Centralized Storage:** All logs are collected on a central server for easy querying and analysis.
- **Extensible:** Easily integrate with other log analysis tools or alerting systems.
- **Resilient:** Handles network and database errors gracefully with automatic retries.

---

## Architecture

```
+-------------+      HTTP POST      +-----------------+
|             |   ============>     |                 |
|  Client(s)  | ------------------> |    Server API   |
|  (Python)   |                     |   (Flask/Python)|
+-------------+                     +-----------------+
     |                                    |
     |                                    |
 MySQL DB                            Central DB or
 (per client)                        Log Store
```

- **Client:** Periodically checks its local MySQL DB for new (unsent) logs and sends them to the server.
- **Server:** Receives logs via an HTTP API endpoint and stores them centrally.

---

## Technologies Used

- **Python:** Client log shipping script.
- **MySQL:** Local log storage on each client.
- **Flask:** REST API server for receiving and storing logs.
- **Requests:** For HTTP communication from client to server.
- **SQL:** For database operations.
- **(Optional) Node.js:** Can be used for real-time dashboards or alternative backend implementation.

---

## Getting Started

### Prerequisites

- Python 3.7+
- MySQL Server
- (Server) Flask (`pip install flask`)
- (Client) Requests (`pip install requests`)
- (Optional) Node.js, if you want to build a dashboard or alternate backend

---

### 1. Set Up MySQL Database

On each client machine:
```sql
CREATE DATABASE clientdb;
USE clientdb;

CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255),
    level VARCHAR(32),
    created_at DATETIME,
    sent TINYINT DEFAULT 0
);
```

### 2. Insert Sample Logs

```sql
INSERT INTO logs (message, level, created_at, sent) VALUES ('Sample log', 'INFO', NOW(), 0);
```

### 3. Run the Server

On the central server:
```bash
pip install flask
python server.py
```

### 4. Run the Client(s)

On each client machine:
```bash
pip install mysql-connector-python requests
python client.py
```

---

## Example: Client Flow

1. Connects to local MySQL database.
2. Fetches logs where `sent = 0`.
3. Sends each unsent log to the server API.
4. On successful delivery, updates `sent = 1` for that log.
5. Repeats periodically.

---

## Example: Server Flow

1. Receives log data via POST `/api/logs`.
2. Validates and stores the log in the central log store or database.
3. Responds with HTTP 201 and a success message.

---

## Extending the System

- **Add Authentication:** Secure log transmission with API keys or OAuth.
- **Real-Time Dashboards:** Use Node.js with Socket.IO for live log updates.
- **Alerting:** Integrate with email, Slack, or other notification services.
- **Support More Log Sources:** Adapt the client for other databases or log formats.

---

## Troubleshooting

- **Log not marked as sent?**  
  Ensure your client updates the `sent` field after successful delivery and that autocommit is enabled for MySQL connections.

- **Logs not appearing on server?**  
  Check server and client logs for errors. Ensure the server API is reachable from clients.

---