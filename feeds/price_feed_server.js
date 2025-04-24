import express from 'express';
import axios from 'axios';
import bodyParser from 'body-parser';

const app = express();
const port = 3000;

app.use(bodyParser.json());

// Simulated WebSocket Data Feed (replace with real provider like Binance, Alpaca, etc.)
let mockMarketPrice = 1000;

setInterval(() => {
  mockMarketPrice += (Math.random() - 0.5) * 10; // Simulated price change
}, 2000);

// Route to fetch live price
app.get('/api/price', (req, res) => {
  res.json({ price: mockMarketPrice });
});

// Signal Processor (AI Trigger)
app.post('/api/analyze', async (req, res) => {
  const { symbol, threshold } = req.body;
  const currentPrice = mockMarketPrice;
  
  // Signal condition
  if (currentPrice > threshold) {
    console.log(`[AI Signal] ${symbol} exceeded threshold (${threshold}) at ${currentPrice}`);
    res.json({ decision: 'SELL', price: currentPrice });
  } else {
    console.log(`[AI Signal] ${symbol} below threshold (${threshold}) at ${currentPrice}`);
    res.json({ decision: 'HOLD', price: currentPrice });
  }
});

app.listen(port, () => {
  console.log(`NOS Trade - Real-time feed running at http://localhost:${port}`);
});

// TODO in next phase:
// - Connect to real Binance or Alpaca websocket feeds
// - Automate POST to /api/analyze based on event listeners
// - Store price logs in a local DB or CSV for analysis 