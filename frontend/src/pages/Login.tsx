import React from 'react';
import LoginForm from '../components/auth/LoginForm';
import '../styles/Register.css';

const Login: React.FC = () => {
  return (
    <div className="register-page">
      <div className="register-container">
        <h1>Вход</h1>
        <p className="subtitle">Войдите, чтобы просматривать новости и комментировать</p>

        <LoginForm />

        <div className="login-link">
          Нет аккаунта?{' '}
          <a href="/" className="login-link-text">Зарегистрироваться</a>
        </div>

        <div className="demo-note-small">
        </div>
      </div>
    </div>
  );
};

export default Login;