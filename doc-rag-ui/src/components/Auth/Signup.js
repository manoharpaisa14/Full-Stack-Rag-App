// components/Auth/Signup.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../../api';
import 'bootstrap/dist/css/bootstrap.min.css';

const Signup = () => {
  const [form, setForm] = useState({ username: '', password: '' });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await API.post('/signup', form);
      navigate('/login');
    } catch (err) {
      alert('Signup failed');
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
      <div className="card p-4 shadow" style={{ width: '100%', maxWidth: '400px' }}>
        <h3 className="text-center mb-3">Sign Up</h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Username</label>
            <input
              type="text"
              className="form-control"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary w-100">Sign Up</button>
        </form>
        <p className="mt-3 text-center">
          Already have an account? <a href="/login">Login</a>
        </p>
      </div>
    </div>
  );
};

export default Signup;
