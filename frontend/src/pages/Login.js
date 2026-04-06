import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // 1. Get Tokens
      const res = await api.post('auth/login/', { email, password });
      localStorage.setItem('access_token', res.data.access);
      localStorage.setItem('refresh_token', res.data.refresh);

      // 2. Fetch User Profile to get role
      const userRes = await api.get('auth/user/');
      localStorage.setItem('user_role', userRes.data.role);
      localStorage.setItem('user_id', userRes.data.id);

      // 3. Redirect matching role
      if (userRes.data.role === 'admin') {
        navigate('/admin/dashboard');
      } else {
        navigate('/author/dashboard');
      }
    } catch (err) {
      alert('Login failed. Please check your credentials.');
    }
  };

  return (
    <div className="login-container card">
      <h2>Welcome to BookLeaf</h2>
      <p style={{marginBottom: 20}}>Please login to continue.</p>
      <form onSubmit={handleLogin}>
        <div className="form-group">
          <label>Email Address</label>
          <input 
            type="email" 
            value={email} 
            onChange={e => setEmail(e.target.value)} 
            required 
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input 
            type="password" 
            value={password} 
            onChange={e => setPassword(e.target.value)} 
            required 
          />
        </div>
        <button type="submit" style={{width: '100%'}}>Login</button>
      </form>
    </div>
  );
}

export default Login;
