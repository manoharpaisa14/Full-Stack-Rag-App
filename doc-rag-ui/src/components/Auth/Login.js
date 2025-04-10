import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../../api';
import { useAuth } from './AuthContext';
import 'bootstrap/dist/css/bootstrap.min.css';

const Login = () => {
  const [form, setForm] = useState({ username: '', password: '' });
  const navigate = useNavigate();
  const { setIsAuthenticated } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new URLSearchParams();
    formData.append('username', form.username);
    formData.append('password', form.password);

    try {
      const res = await API.post('/login', formData);
      localStorage.setItem('token', res.data.access_token);
      setIsAuthenticated(true);
      navigate('/app');
    } catch (err) {
      alert('Login failed');
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <div className="card shadow p-4" style={{ width: '100%', maxWidth: '400px' }}>
        <h2 className="text-center mb-4">Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Username"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              required
            />
          </div>
          <div className="mb-3">
            <input
              type="password"
              className="form-control"
              placeholder="Password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary w-100">
            Log In
          </button>
        </form>
        <p className="text-center mt-3">
          No account? <a href="/signup">Sign up</a>
        </p>
      </div>
    </div>
  );
};

export default Login;
