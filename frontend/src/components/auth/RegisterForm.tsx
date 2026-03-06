import React, { useState } from 'react';
import axios from 'axios';

interface UserRegister {
  name: string;
  email: string;
  password: string;
  is_author_verified?: boolean;
  is_admin?: boolean;
  avatar?: string | null;
}

const RegisterForm: React.FC = () => {
  const [formData, setFormData] = useState<UserRegister>({
    name: '',
    email: '',
    password: '',
  });

  const [passwordChecks, setPasswordChecks] = useState({
    length: false,
    uppercase: false,
    lowercase: false,
    number: false,
    special: false,
  });

  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));

    if (name === 'password') {
      setPasswordChecks({
        length: value.length >= 8,
        uppercase: /[A-Z]/.test(value),
        lowercase: /[a-z]/.test(value),
        number: /\d/.test(value),
        special: /[@$!%*?&]/.test(value),
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      await axios.post('http://localhost:8000/auth/register', formData);
      alert('✅ Регистрация прошла успешно!');
      window.location.href = '/news';   // редирект на новости
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Ошибка регистрации';
      setError(msg);
    }
  };

  const allChecksPassed = Object.values(passwordChecks).every(Boolean);

  return (
    <form onSubmit={handleSubmit} className="register-form">
      {/* поля формы остаются прежними */}
      <div className="input-group">
        <label>Имя</label>
        <input type="text" name="name" value={formData.name} onChange={handleChange} placeholder="Введите ваше имя" required />
      </div>

      <div className="input-group">
        <label>Email</label>
        <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="example@mail.com" required />
      </div>

      <div className="input-group">
        <label>Пароль</label>
        <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="••••••••" required />

        <div className="password-requirements">
          <p>Требования к паролю:</p>
          <ul>
            <li className={passwordChecks.length ? 'valid' : 'invalid'}>{passwordChecks.length ? '✓' : '✗'} Минимум 8 символов</li>
            <li className={passwordChecks.uppercase ? 'valid' : 'invalid'}>{passwordChecks.uppercase ? '✓' : '✗'} Одна заглавная буква</li>
            <li className={passwordChecks.lowercase ? 'valid' : 'invalid'}>{passwordChecks.lowercase ? '✓' : '✗'} Одна строчная буква</li>
            <li className={passwordChecks.number ? 'valid' : 'invalid'}>{passwordChecks.number ? '✓' : '✗'} Одна цифра</li>
            <li className={passwordChecks.special ? 'valid' : 'invalid'}>{passwordChecks.special ? '✓' : '✗'} Один спецсимвол (@$!%*?&)</li>
          </ul>
        </div>
      </div>

      {error && <p className="error global-error">{error}</p>}

      <button type="submit" className="submit-btn" disabled={!allChecksPassed || !formData.name || !formData.email}>
        Зарегистрироваться
      </button>
    </form>
  );
};

export default RegisterForm;