import mysql.connector
import requests
import time
import sys

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "dwiharsh123#",
    "database": "clientdb"
}

SERVER_URL = "http://localhost:5001/api/logs"
CLIENT_ID = "client1"
POLL_INTERVAL = 5  # seconds

def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    conn.autocommit = True  # Enable autocommit mode
    return conn

def fetch_unsent_logs(conn):
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM logs WHERE sent = 0")
        results = cursor.fetchall()
    print(f"[DEBUG] Current unsent logs: {[log['id'] for log in results]}")
    return results

def mark_log_as_sent(conn, log_id):
    print(f"[DEBUG] Marking log {log_id} as sent...")
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE logs SET sent = 1 WHERE id = %s", (log_id,))
            print(f"[DEBUG] Rows affected: {cursor.rowcount}")
    except Exception as e:
        print(f"[ERROR] Failed to mark log as sent: {e}")
    # Confirm update
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT sent FROM logs WHERE id = %s", (log_id,))
        result = cursor.fetchone()
        print(f"[DEBUG] After update, log {log_id} sent status: {result['sent'] if result else 'NOT FOUND'}")

def send_log_to_server(log):
    payload = {
        "client_id": CLIENT_ID,
        "message": log.get("message"),
        "level": log.get("level"),
        "created_at": log.get("created_at").strftime('%Y-%m-%d %H:%M:%S') if log.get("created_at") else None
    }
    try:
        response = requests.post(SERVER_URL, json=payload, timeout=5)
        if response.status_code in (200, 201):
            print(f"Log ID {log['id']} sent successfully.")
            return True
        else:
            print(f"Server returned status code {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"Error sending log ID {log['id']}: {e}")
        return False

def main():
    print("Connecting to clientdb database.")
    conn = None
    try:
        conn = get_db_connection()
        while True:
            try:
                logs = fetch_unsent_logs(conn)
                if not logs:
                    print("No new logs found.")
                for log in logs:
                    print(f"Sending log ID {log['id']}: { {k: v for k, v in log.items() if k != 'sent'} }")
                    if send_log_to_server(log):
                        mark_log_as_sent(conn, log['id'])
                time.sleep(POLL_INTERVAL)
            except mysql.connector.Error as db_err:
                print(f"MySQL error: {db_err}. Attempting to reconnect...")
                if conn:
                    conn.close()
                time.sleep(2)
                conn = get_db_connection()
            except Exception as e:
                print(f"Unexpected error: {e}")
                time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()