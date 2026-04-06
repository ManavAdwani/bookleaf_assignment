import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import {jwtDecode} from 'jwt-decode';
import './App.css';

import Login from './pages/Login';
import AuthorDashboard from './pages/AuthorDashboard';
import SubmitTicket from './pages/SubmitTicket';
import MyTickets from './pages/MyTickets';
import AdminDashboard from './pages/AdminDashboard';
import TicketDetail from './pages/TicketDetail';

// Simple Auth Wrap
const PrivateRoute = ({ children, roleRequired }) => {
  const token = localStorage.getItem('access_token');
  if (!token) return <Navigate to="/login" />;
  
  try {
    jwtDecode(token);
    // Note: our token doesn't include role by default unless configured,
    // so we fetch user info on login and store role in localStorage for simplicity
    const role = localStorage.getItem('user_role');
    
    if (roleRequired && role !== roleRequired) {
      return <Navigate to="/" />; // Redirect if role mismatch
    }
  } catch (e) {
    return <Navigate to="/login" />;
  }
  
  return children;
};

function App() {
  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route path="/login" element={<Login />} />
          
          <Route path="/" element={
            <PrivateRoute>
              <DashboardRouter />
            </PrivateRoute>
          } />
          
          {/* Author Routes */}
          <Route path="/author/dashboard" element={<PrivateRoute roleRequired="author"><AuthorDashboard /></PrivateRoute>} />
          <Route path="/author/submit-ticket" element={<PrivateRoute roleRequired="author"><SubmitTicket /></PrivateRoute>} />
          <Route path="/author/my-tickets" element={<PrivateRoute roleRequired="author"><MyTickets /></PrivateRoute>} />
          <Route path="/author/ticket/:id" element={<PrivateRoute roleRequired="author"><TicketDetail /></PrivateRoute>} />
          
          {/* Admin Routes */}
          <Route path="/admin/dashboard" element={<PrivateRoute roleRequired="admin"><AdminDashboard /></PrivateRoute>} />
          <Route path="/admin/ticket/:id" element={<PrivateRoute roleRequired="admin"><TicketDetail /></PrivateRoute>} />
        </Routes>
      </div>
    </Router>
  );
}

const DashboardRouter = () => {
  const role = localStorage.getItem('user_role');
  if (role === 'admin') return <Navigate to="/admin/dashboard" />;
  if (role === 'author') return <Navigate to="/author/dashboard" />;
  return <Navigate to="/login" />;
};

export default App;
