import React from 'react';
import './App.css';

function NavBar({ status }) {
    return (
        <nav className="navbar">
            <div className="status-display">
                <strong>Статус: </strong>{status}
            </div>
            <div className="nav-buttons">
                <a href="#slide1">Регистрация/Вход</a>
                <a href="#slide2">Новая передачка</a>
                <a href="#slide3">Получить передачку</a>
            </div>
        </nav>
    );
}

export default NavBar;