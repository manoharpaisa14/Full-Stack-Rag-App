
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Signup from './components/Auth/Signup';
import Login from './components/Auth/Login';
import Upload from './components/UploadAsk/Upload';
import { useAuth } from './components/Auth/AuthContext'

function App() {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated === null) return <div>Loading...</div>;

  return (
    <Router>
      <Routes>
        <Route path="/" element={isAuthenticated ? <Navigate to="/app" /> : <Navigate to="/signup" />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/app" element={isAuthenticated ? <Upload /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
