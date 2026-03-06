import React, { useState, useEffect } from 'react';
import axios from 'axios';

const NewsList: React.FC = () => {
  const [news, setNews] = useState<News[]>([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await axios.get('http://localhost:8000/news');
        setNews(response.data);
      } catch (err: any) {
        console.error('Ошибка: ', err);
        alert('Ошибка загрузки новостей: ' + (err.response?.data?.detail || 'Проверьте соединение'));
        }
    };
    fetchNews();
  }, []);

  const filteredNews = news.filter(item => item.title.toLowerCase().includes(filter.toLowerCase()));

  return (
    <div>
      <input
        type="text"
        placeholder="Фильтр по заголовку"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        className="filter-input"
      />

      {filteredNews.map(item => (
        <div key={item.id} className="news-item">
          <h3>{item.title}</h3>
          <p>Автор: {item.author_id} | Дата: {item.publication_date}</p>
          <p>{item.content.text || JSON.stringify(item.content)}</p>
        </div>
      ))}
    </div>
  );
};

export default NewsList;