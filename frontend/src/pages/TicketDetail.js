import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';

function TicketDetail() {
  const { id } = useParams();
  const [ticket, setTicket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [internalNotes, setInternalNotes] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [newNote, setNewNote] = useState('');
  
  const role = localStorage.getItem('user_role');
  const isAdmin = role === 'admin';

  const fetchTicket = useCallback(async () => {
    try {
      const res = await api.get(`tickets/${id}/`);
      setTicket(res.data);
      setMessages(res.data.messages || []);
      setInternalNotes(res.data.internal_notes || []);
    } catch (err) {
      console.error(err);
    }
  }, [id]);

  useEffect(() => {
    fetchTicket();
    const interval = setInterval(fetchTicket, 10000); // Polling every 10s
    return () => clearInterval(interval);
  }, [fetchTicket]);

  const handleUpdateStatus = async (status) => {
    try {
      await api.patch(`tickets/${id}/`, { status });
      fetchTicket();
    } catch (err) {
      alert('Error updating status');
    }
  };

  const handleUpdateCategory = async (category) => {
    try {
      await api.patch(`tickets/${id}/`, { category });
      fetchTicket();
    } catch (err) {
      alert('Error updating category');
    }
  };

  const handleUpdatePriority = async (priority) => {
    try {
      await api.patch(`tickets/${id}/`, { priority });
      fetchTicket();
    } catch (err) {
      alert('Error updating priority');
    }
  };

  const handleAssignToMe = async () => {
    try {
      const currentUserId = localStorage.getItem('user_id');
      await api.patch(`tickets/${id}/`, { assigned_to: currentUserId });
      fetchTicket();
    } catch (err) {
      alert('Error assigning ticket');
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;
    try {
      await api.post('messages/', { ticket: id, text: newMessage });
      setNewMessage('');
      fetchTicket();
    } catch (err) {
      alert('Error sending message');
    }
  };

  const handleAddNote = async (e) => {
    e.preventDefault();
    if (!newNote.trim()) return;
    try {
      await api.post('internal_notes/', { ticket: id, note: newNote });
      setNewNote('');
      fetchTicket();
    } catch (err) {
      alert('Error adding note');
    }
  };

  if (!ticket) return <div>Loading...</div>;

  return (
    <>
      <nav className="navbar">
        <h2>Ticket #{ticket.id} - {ticket.subject}</h2>
        <div className="nav-links">
          <Link to={isAdmin ? "/admin/dashboard" : "/author/dashboard"}>Back to Dashboard</Link>
        </div>
      </nav>

      <div className="ticket-layout">
        {/* Left Column: Chat */}
        <div className="ticket-layout-main">
          <div className="card">
            <h3>Conversation</h3>
            <div className="chat-box">
              <div className="message author">
                <strong>{ticket.author_name} (Author)</strong>
                <p>{ticket.description}</p>
              </div>

              {messages.map(msg => (
                <div key={msg.id} className={`message ${msg.sender_role === 'admin' ? 'admin' : 'author'}`}>
                  <strong>{msg.sender_name} ({msg.sender_role})</strong>
                  <p>{msg.text}</p>
                </div>
              ))}
            </div>

            <form onSubmit={handleSendMessage} className="send-form">
              <input 
                type="text" 
                value={newMessage} 
                onChange={e => setNewMessage(e.target.value)}
                placeholder="Type your response here..." 
              />
              <button type="submit">Send</button>
            </form>
          </div>
        </div>

        {/* Right Column: Details & Admin Actions */}
        <div className="ticket-layout-side">
          <div className="card">
            <h3>Ticket Details</h3>
            <p><strong>Status:</strong> {ticket.status}</p>
            <p><strong>Assigned To:</strong> {ticket.assigned_to_name || 'Unassigned'} 
              {isAdmin && !ticket.assigned_to && (
                <button onClick={handleAssignToMe} style={{marginLeft: 10, padding: '2px 8px', fontSize: 11}}>Claim Ticket</button>
              )}
            </p>
            <p><strong>Book:</strong> {ticket.book_title || 'General'}</p>
            <p><strong>Category:</strong> 
              {!isAdmin ? (ticket.category || 'N/A') : (
                <select value={ticket.category || ''} onChange={e => handleUpdateCategory(e.target.value)} style={{marginLeft: 5, padding: 3}}>
                  <option value="General Inquiry">General Inquiry</option>
                  <option value="Royalty & Payments">Royalty & Payments</option>
                  <option value="ISBN & Metadata Issues">ISBN & Metadata Issues</option>
                  <option value="Printing & Quality">Printing & Quality</option>
                  <option value="Distribution & Availability">Distribution & Availability</option>
                  <option value="Book Status & Production Updates">Book Status & Production Updates</option>
                </select>
              )}
            </p>
            <p><strong>Priority:</strong> 
              {!isAdmin ? (ticket.priority || 'N/A') : (
                <select value={ticket.priority || ''} onChange={e => handleUpdatePriority(e.target.value)} style={{marginLeft: 5, padding: 3}}>
                  <option value="Critical">Critical</option>
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </select>
              )}
            </p>
            
            {isAdmin && (
              <div style={{ marginTop: 20 }}>
                <h4>Update Status</h4>
                <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap' }}>
                  {['Open', 'In Progress', 'Resolved', 'Closed'].map(s => (
                    <button key={s} onClick={() => handleUpdateStatus(s)} disabled={ticket.status === s}
                      style={{ background: ticket.status === s ? '#ccc' : '#0066cc', padding: '5px 10px', fontSize: 12 }}>
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {isAdmin && ticket.ai_draft_response && (
            <div className="card ai-draft-box">
              <h4>🤖 AI Draft Response</h4>
              <p style={{ fontSize: 14 }}>{ticket.ai_draft_response}</p>
              <button onClick={() => setNewMessage(ticket.ai_draft_response)} style={{ marginTop: 10, fontSize: 12 }}>
                Use as Response
              </button>
            </div>
          )}

          {isAdmin && (
            <div className="card">
              <h4>Internal Notes (Private)</h4>
              <div style={{ maxHeight: 200, overflowY: 'auto', marginBottom: 10 }}>
                {internalNotes.map(n => (
                  <div key={n.id} className="message internal">
                    <strong>{n.admin_name}</strong>
                    <p style={{ margin: '5px 0' }}>{n.note}</p>
                  </div>
                ))}
              </div>
              <form onSubmit={handleAddNote} style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
                <textarea 
                  rows="2" 
                  value={newNote} 
                  onChange={e => setNewNote(e.target.value)} 
                  placeholder="Add a private note..."
                  style={{ width: '100%', padding: 5 }}
                />
                <button type="submit" style={{ fontSize: 12 }}>Add Note</button>
              </form>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default TicketDetail;
