import React, { useState } from 'react';
import axios from 'axios';

interface UserLogin {
  email: string;
  password: string;
}

const LoginForm: React.FC = () => {
  const [formData, setFormData] = useState<UserLogin>({
    email: '',
    password: '',
  });

  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/auth/login', formData);
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      localStorage.setItem('user_email', formData.email);
      alert('✅ Вход успешен!');
      window.location.href = '/news';  // редирект
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Ошибка входа';
      setError(msg);  // 401: Invalid credentials
    }
  };

  return (
    <form onSubmit={handleSubmit} className="register-form">
      <div className="input-group">
        <label>Email</label>
        <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="example@mail.com" required />
      </div>

      <div className="input-group">
        <label>Пароль</label>
        <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="••••••••" required />
      </div>

      {error && <p className="error global-error">{error}</p>}

      <button type="submit" className="submit-btn">
        Войти
      </button>

      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <a href="http://localhost:8000/auth/github/login" className="github-btn">
          Войти через GitHub
        </a>
      </div>
    </form>
  );
};

export default LoginForm;