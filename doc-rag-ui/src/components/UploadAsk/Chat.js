// components/Chat/Chat.js
import React, { useState } from 'react';
import API from '../../api';
import 'bootstrap/dist/css/bootstrap.min.css';

const Chat = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAsk = async () => {
    if (!question) return;

    setLoading(true);
    setAnswer('');
    setError(null);

    try {
      const res = await API.get('/ask', { params: { q: question } });
      if (res.data?.answer) {
        setAnswer(res.data.answer);
      } else {
        setError('No answer returned.');
      }
    } catch (err) {
      setError('Error reaching backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h4 className="mb-3">💬 Ask a Question</h4>
      <div className="input-group">
        <input
          type="text"
          className="form-control"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something about the uploaded document"
        />
        <button onClick={handleAsk} className="btn btn-primary">
          Ask
        </button>
      </div>

      {loading && <div className="mt-3 text-secondary">⏳ Loading...</div>}
      {error && <div className="mt-3 text-danger">{error}</div>}
      {answer && (
        <div className="alert alert-success mt-4">
          <strong>Answer:</strong>
          <p className="mb-0">{answer}</p>
        </div>
      )}
    </div>
  );
};

export default Chat;
