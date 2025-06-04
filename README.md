# My Logs Project

A minimal client-server log collection and display system.

## Structure

- `client/`: Python script to scan local MySQL and send logs to server.
- `server/`: Node.js Express API to receive/store logs.
- `frontend/`: React app to display logs in real-time.
- `schema/`: MySQL table schemas.

## Quickstart

1. **Set up MySQL databases:**

   - Create `clientdb` and `serverdb` databases.
   - Run `client_logs.sql` in `clientdb` and `server_logs.sql` in `serverdb`.

2. **Run the server:**
   ```
   cd server
   npm install
   node index.js
   ```

3. **Run the client:**
   - Update DB credentials in `client.py`.
   ```
   cd client
   pip install mysql-connector-python requests
   python client.py
   ```

4. **Run the frontend:**
   - Use [Vite](https://vitejs.dev/) or [Create React App](https://create-react-app.dev/) to start the React app.
   - Make sure the server is running at `localhost:5000`.

5. **View logs:**
   - Open the frontend in your browser.

---

You now have a full-stack log collection and display project!