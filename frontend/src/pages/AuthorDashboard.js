import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

function AuthorDashboard() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const res = await api.get('books/');
      setBooks(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <>
      <nav className="navbar">
        <h2>My Dashboard</h2>
        <div className="nav-links">
          <Link to="/author/my-tickets">My Tickets</Link>
          <button style={{marginLeft: 15}} onClick={() => {
            localStorage.clear();
            window.location.href = '/login';
          }}>Logout</button>
        </div>
      </nav>

      <div className="card">
        <h3>My Books</h3>
        <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>ISBN</th>
              <th>Genre</th>
              <th>Publication Date</th>
              <th>Status</th>
              <th>MRP</th>
              <th>Copies Sold</th>
              <th>Royalty Earned</th>
              <th>Royalty Paid</th>
              <th>Royalty Pending</th>
            </tr>
          </thead>
          <tbody>
            {books.map(b => (
              <tr key={b.id}>
                <td>{b.title}</td>
                <td>{b.isbn}</td>
                <td>{b.genre}</td>
                <td>{b.publication_date || 'N/A'}</td>
                <td>{b.status}</td>
                <td>₹{b.mrp}</td>
                <td>{b.copies_sold}</td>
                <td>₹{b.royalty_earned}</td>
                <td>₹{b.royalty_paid}</td>
                <td>₹{b.royalty_pending}</td>
              </tr>
            ))}
            {books.length === 0 && (
              <tr><td colSpan="10">No books found.</td></tr>
            )}
          </tbody>
        </table>
        </div>
      </div>
    </>
  );
}

export default AuthorDashboard;
