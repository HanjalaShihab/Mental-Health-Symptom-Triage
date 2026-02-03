import express from 'express';
import cors from 'cors';
import { v4 as uuidv4 } from 'uuid';
import assessmentRoutes from './routes/assessmentRoutes.js';
import triageRoutes from './routes/triageRoutes.js';

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/assessment', assessmentRoutes);
app.use('/api/triage', triageRoutes);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'Server is running' });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
