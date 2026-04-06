import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

function MyTickets() {
  const [tickets, setTickets] = useState([]);

  useEffect(() => {
    fetchTickets();
    // Simple Polling (auto-refresh every 10 seconds)
    const interval = setInterval(fetchTickets, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchTickets = async () => {
    try {
      const res = await api.get('tickets/');
      setTickets(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <>
      <nav className="navbar">
        <h2>My Tickets</h2>
        <div className="nav-links">
          <Link to="/author/dashboard">Dashboard</Link>
          <Link to="/author/submit-ticket">
            <button>Submit New Ticket</button>
          </Link>
        </div>
      </nav>

      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Ticket ID</th>
              <th>Subject</th>
              <th>Book</th>
              <th>Status</th>
              <th>Category</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {tickets.map(t => (
              <tr key={t.id}>
                <td>#{t.id}</td>
                <td>{t.subject}</td>
                <td>{t.book_title || 'General'}</td>
                <td><span className={`status-badge status-${t.status.replace(' ', '')}`}>{t.status}</span></td>
                <td>{t.category || '-'}</td>
                <td>
                  <Link to={`/author/ticket/${t.id}`}>View details</Link>
                </td>
              </tr>
            ))}
            {tickets.length === 0 && (
              <tr><td colSpan="6">No tickets found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}

export default MyTickets;
