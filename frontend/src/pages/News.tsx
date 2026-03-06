import React from 'react';
import Navbar from '../components/layout/Navbar';
import NewsList from '../components/news/NewsList';
import '../styles/Register.css';

const News: React.FC = () => {
  return (
    <>
      <Navbar />
      <div className="news-page" style={{ paddingTop: '80px' }}>
        <div className="news-container">
          <h1>Все новости</h1>
          <p className="subtitle">Просмотр и поиск новостей</p>
          <NewsList />
        </div>
      </div>
    </>
  );
};

export default News;