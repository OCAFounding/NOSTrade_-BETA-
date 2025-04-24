import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import axios from 'axios';

const NOSChat = () => {
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);

    const newMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, newMessage]);
    setInput('');

    try {
      const res = await axios.post('/api/ai-chat', { prompt: input });
      setMessages(prev => [...prev, { role: 'agent', content: res.data.reply }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'agent', content: '⚠️ Error fetching response.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-black text-white flex flex-col">
      <header className="p-6 flex justify-between items-center border-b border-slate-700">
        <h1 className="text-xl font-bold">📊 NOS Trade AI Assistant</h1>
        <Button variant="outline" className="text-sm">Toggle Theme</Button>
      </header>

      <main className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((msg, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`p-4 rounded-md w-fit max-w-xl ${msg.role === 'user' ? 'ml-auto bg-blue-600' : 'bg-slate-700'}`}
          >
            {msg.content}
          </motion.div>
        ))}
      </main>

      <footer className="p-6 border-t border-slate-700 bg-slate-800">
        <div className="flex items-center gap-4">
          <Input
            placeholder="Ask NOS Trade to rebalance..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            className="flex-1 bg-slate-900 border-slate-700 text-white"
          />
          <Button onClick={handleSend} disabled={loading}>
            {loading ? 'Sending...' : 'Send'}
          </Button>
        </div>
      </footer>
    </div>
  );
};

export default NOSChat; 