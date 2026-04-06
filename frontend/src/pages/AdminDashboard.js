import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

function AdminDashboard() {
  const [tickets, setTickets] = useState([]);
  const [statusFilter, setStatusFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [dateFilter, setDateFilter] = useState('');

  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = async () => {
    try {
      const res = await api.get('tickets/');
      setTickets(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const filteredTickets = tickets.filter(t => {
    let match = true;
    if (statusFilter && t.status !== statusFilter) match = false;
    if (categoryFilter && t.category !== categoryFilter) match = false;
    if (priorityFilter && t.priority !== priorityFilter) match = false;
    if (dateFilter) {
      const ticketDate = new Date(t.created_at).toISOString().split('T')[0];
      if (ticketDate !== dateFilter) match = false;
    }
    return match;
  });

  const priorityWeight = { 'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1 };

  const sortedTickets = [...filteredTickets].sort((a, b) => {
    // 1. Sort by Priority (Urgent first)
    const weightA = priorityWeight[a.priority] || 0;
    const weightB = priorityWeight[b.priority] || 0;
    if (weightB !== weightA) {
      return weightB - weightA;
    }
    // 2. Sort by Age (Oldest first if urgency is the same)
    return new Date(a.created_at) - new Date(b.created_at);
  });

  return (
    <>
      <nav className="navbar">
        <h2>Admin Portal - Support Tickets</h2>
        <div className="nav-links">
          <button onClick={() => {
            localStorage.clear();
            window.location.href = '/login';
          }} style={{ background: '#d32f2f' }}>Logout</button>
        </div>
      </nav>

      <div className="card">
        <div style={{ marginBottom: 20, display: 'flex', gap: 15, alignItems: 'center', flexWrap: 'wrap' }}>
          <div>
            <label style={{display:'block', fontSize:12, color:'#666', marginBottom:4}}>Status</label>
            <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)} style={{ padding: 5, minWidth: 120 }}>
              <option value="">All Statuses</option>
              <option value="Open">Open</option>
              <option value="In Progress">In Progress</option>
              <option value="Resolved">Resolved</option>
              <option value="Closed">Closed</option>
            </select>
          </div>
          <div>
            <label style={{display:'block', fontSize:12, color:'#666', marginBottom:4}}>Priority</label>
            <select value={priorityFilter} onChange={e => setPriorityFilter(e.target.value)} style={{ padding: 5, minWidth: 120 }}>
              <option value="">All Priorities</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>
          <div>
            <label style={{display:'block', fontSize:12, color:'#666', marginBottom:4}}>Category</label>
            <select value={categoryFilter} onChange={e => setCategoryFilter(e.target.value)} style={{ padding: 5, minWidth: 140 }}>
              <option value="">All Categories</option>
              <option value="Royalty & Payments">Royalty & Payments</option>
              <option value="ISBN & Metadata">ISBN & Metadata</option>
              <option value="Printing & Quality">Printing & Quality</option>
              <option value="Distribution">Distribution</option>
              <option value="Book Status">Book Status</option>
              <option value="General">General</option>
            </select>
          </div>
          <div>
            <label style={{display:'block', fontSize:12, color:'#666', marginBottom:4}}>Submitted Date</label>
            <input type="date" value={dateFilter} onChange={e => setDateFilter(e.target.value)} style={{ padding: 4 }} />
          </div>
        </div>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Author</th>
              <th>Subject</th>
              <th>Status</th>
              <th>Category (AI)</th>
              <th>Priority (AI)</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {sortedTickets.map(t => (
              <tr key={t.id}>
                <td>#{t.id}</td>
                <td>{t.author_name}</td>
                <td>{t.subject}</td>
                <td><span className={`status-badge status-${t.status.replace(' ', '')}`}>{t.status}</span></td>
                <td>{t.category || '-'}</td>
                <td>{t.priority || '-'}</td>
                <td>
                  <Link to={`/admin/ticket/${t.id}`}>Manage</Link>
                </td>
              </tr>
            ))}
            {sortedTickets.length === 0 && (
              <tr><td colSpan="7">No tickets found matching the criteria.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}

export default AdminDashboard;
