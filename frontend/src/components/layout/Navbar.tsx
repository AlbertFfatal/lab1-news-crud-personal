import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const userEmail = localStorage.getItem('user_email') || 'Гость';
  const token = localStorage.getItem('access_token');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_email');
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="nav-left">
        <Link to="/news" className="nav-link">Новости</Link>
        <Link to="/news/create" className="nav-link">Создать новость</Link>
      </div>

      <div className="nav-right">
        <span className="user-email">{userEmail}</span>
        {token && (
          <button onClick={handleLogout} className="logout-btn">
            Выйти
          </button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;