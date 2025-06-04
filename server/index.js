const express = require('express');
const cors = require('cors');
const db = require('./db');

const app = express();
app.use(cors());
app.use(express.json());

// Receive and store logs
app.post('/api/logs', async (req, res) => {
  const { client_id, message, level, created_at } = req.body;
  try {
    await db.execute(
      'INSERT INTO logs (client_id, message, level, created_at) VALUES (?, ?, ?, ?)',
      [client_id, message, level, created_at]
    );
    res.status(201).json({ msg: 'Log stored' });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Fetch logs
app.get('/api/logs', async (req, res) => {
  try {
    const [rows] = await db.execute('SELECT * FROM logs ORDER BY received_at DESC LIMIT 100');
    res.json(rows);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.listen(5001, () => console.log('Server running on http://localhost:5001'));