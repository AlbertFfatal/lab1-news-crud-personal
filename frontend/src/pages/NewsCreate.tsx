import React from 'react';
import Navbar from '../components/layout/Navbar';
import NewsCreateForm from '../components/news/NewsCreateForm';
import '../styles/Register.css';

const NewsCreate: React.FC = () => {
  return (
    <>
      <Navbar />
      <div className="news-page" style={{ paddingTop: '80px' }}>
        <div className="news-container">
          <h1>Создание новости</h1>
          <p className="subtitle">Только для проверенных авторов и администраторов</p>
          <NewsCreateForm />
        </div>
      </div>
    </>
  );
};

export default NewsCreate;