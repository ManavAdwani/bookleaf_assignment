import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';

function SubmitTicket() {
  const [books, setBooks] = useState([]);
  const [bookId, setBookId] = useState('');
  const [subject, setSubject] = useState('');
  const [description, setDescription] = useState('');
  const [attachment, setAttachment] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch books to populate dropdown
    api.get('books/').then(res => {
      setBooks(res.data);
    });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('tickets/', {
        book: bookId || null,
        subject,
        description
      });
      alert('Ticket created successfully!');
      navigate('/author/my-tickets');
    } catch (err) {
      alert('Error creating ticket.');
    }
  };

  return (
    <>
      <nav className="navbar">
        <h2>Submit Ticket</h2>
        <div className="nav-links">
          <Link to="/author/dashboard">Dashboard</Link>
          <Link to="/author/my-tickets">My Tickets</Link>
        </div>
      </nav>

      <div className="card" style={{ maxWidth: 600 }}>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Related Book</label>
            <select value={bookId} onChange={e => setBookId(e.target.value)}>
              <option value="">General Support (No Specific Book)</option>
              {books.map(b => (
                <option key={b.id} value={b.id}>{b.title}</option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>Subject</label>
            <input 
              type="text" 
              required 
              value={subject} 
              onChange={e => setSubject(e.target.value)} 
            />
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea 
              rows="5" 
              required 
              value={description} 
              onChange={e => setDescription(e.target.value)} 
            />
          </div>

          <div className="form-group">
            <label>Optional Attachment (Screenshots, PDFs, etc.)</label>
            <input 
              type="file" 
              onChange={e => setAttachment(e.target.files[0])} 
              style={{marginTop: 5}}
            />
            {attachment && <small style={{color: 'gray'}}>File selected: {attachment.name} (UI Only)</small>}
          </div>

          <button type="submit">Submit Ticket</button>
        </form>
      </div>
    </>
  );
}

export default SubmitTicket;
