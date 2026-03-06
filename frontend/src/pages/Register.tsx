import React from 'react';
import RegisterForm from '../components/auth/RegisterForm';
import '../styles/Register.css';

const Register: React.FC = () => {
  return (
    <div className="register-page">
      <div className="register-container">
        <h1>Регистрация</h1>
        <p className="subtitle">Создайте аккаунт, чтобы публиковать новости и комментарии</p>

        <RegisterForm />

        <div className="login-link">
          Уже есть аккаунт?{' '}
          <a href="/login" className="login-link-text">Войти</a>
        </div>

        <div className="demo-note-small">
          После успешной регистрации вы будете перенаправлены на страницу новостей
        </div>
      </div>
    </div>
  );
};

export default Register;