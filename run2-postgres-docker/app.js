const express = require('express');
const { Pool } = require('pg');
const { createClient } = require('redis');

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';
const POSTGRES_URL = process.env.DATABASE_URL || 'postgres://postgres:postgres@localhost:5432/appdb';

const redisClient = createClient({ url: REDIS_URL });
redisClient.on('error', (err) => console.log('Redis Error:', err));

const pool = new Pool({ connectionString: POSTGRES_URL });

// Cache-aside pattern route
app.get('/data/:key', async (req, res) => {
    const { key } = req.params;
    try {
        // 1. Check Redis Cache
        const cachedValue = await redisClient.get(key);
        if (cachedValue) {
            return res.json({ source: 'redis-cache', key, value: JSON.parse(cachedValue) });
        }

        // 2. Fetch from Postgres on Cache Miss
        const dbRes = await pool.query('SELECT value FROM store WHERE key = $1', [key]);
        if (dbRes.rows.length === 0) {
            return res.status(404).json({ error: 'Key not found in database' });
        }

        const value = dbRes.rows[0].value;

        // 3. Cache result in Redis with 60-second TTL
        await redisClient.setEx(key, 60, JSON.stringify(value));

        return res.json({ source: 'postgresql-db', key, value });
    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy', timestamp: new Date() });
});

async function start() {
    try {
        await redisClient.connect();
        console.log('Connected to Redis');
        app.listen(PORT, () => console.log(`Microservice listening on port ${PORT}`));
    } catch (err) {
        console.error('Failed to start server:', err);
    }
}

start();