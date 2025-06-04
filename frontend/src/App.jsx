import React, { useEffect, useState } from 'react';

function App() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = () => {
      fetch('http://localhost:5001/api/logs')
        .then(res => res.json())
        .then(setLogs);
    };
    fetchLogs();
    const interval = setInterval(fetchLogs, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ margin: '2rem' }}>
      <h2>Live Logs</h2>
      <table border="1" cellPadding={6} align='center' style={{ width: '80%' }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Client</th>
            <th>Message</th>
            <th>Level</th>
            <th>Created At</th>
            <th>Received At</th>
          </tr>
        </thead>
        <tbody>
          {logs.map(log => (
            <tr key={log.id}>
              <td>{log.id}</td>
              <td>{log.client_id}</td>
              <td>{log.message}</td>
              <td>{log.level}</td>
              <td>{log.created_at}</td>
              <td>{log.received_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;