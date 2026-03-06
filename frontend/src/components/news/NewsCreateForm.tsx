import React, { useState } from 'react';
import axios from 'axios';

const NewsCreateForm: React.FC = () => {
  const [formData, setFormData] = useState<NewsCreate>({
    title: '',
    content: {},  // JSON
    cover: '',
  });

  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: name === 'content' ? JSON.parse(value) : value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/news', formData, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
      });
      alert(' Новость создана!');
      window.location.reload();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Ошибка создания новости';
      setError(msg);  // 403: "Author is not verified"
      }
   };

  return (
    <form onSubmit={handleSubmit} className="register-form">
      <div className="input-group">
        <label>Заголовок</label>
        <input type="text" name="title" value={formData.title} onChange={handleChange} required />
      </div>

      <div className="input-group">
        <label>Содержимое (JSON)</label>
        <textarea name="content" value={JSON.stringify(formData.content)} onChange={handleChange} required />
      </div>

      <div className="input-group">
        <label>Обложка (URL)</label>
        <input type="text" name="cover" value={formData.cover} onChange={handleChange} />
      </div>

      {error && <p className="error">{error}</p>}

      <button type="submit" className="submit-btn">Создать новость</button>
    </form>
  );
};

export default NewsCreateForm;