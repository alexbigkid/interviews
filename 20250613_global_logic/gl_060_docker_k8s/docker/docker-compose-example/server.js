const express = require('express');
const { Client } = require('pg');
const redis = require('redis');

const app = express();
const port = process.env.PORT || 3000;

const dbClient = new Client({
  connectionString: process.env.DATABASE_URL
});

const redisClient = redis.createClient({
  url: 'redis://redis:6379'
});

app.use(express.json());

app.get('/', (req, res) => {
  res.json({
    message: 'Hello from Docker Compose!',
    timestamp: new Date().toISOString()
  });
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});