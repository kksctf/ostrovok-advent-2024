import React, { useState } from 'react';
import QRCode from "react-qr-code";
import axios from 'axios';
import NavBar from './NavBar';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [walletAddress, setWalletAddress] = useState('');
  const [recipientAddress, setRecipientAddress] = useState('');
  const [amount, setAmount] = useState('');
  const [handoff, setHandoff] = useState('');
  const [signature, setSignature] = useState('');
  const [balance, setBalance] = useState('');
  const [status, setStatus] = useState('');
  const [token, setToken] = useState('');

  const registerUser = async () => {
    try {
      const response = await axios.post(`/api/register`, {
        username,
        email,
        password,
      });
      setWalletAddress(response.data.wallet_address);
      setStatus('Успешная регистрация. Войдите');
    } catch (error) {
      console.error('Ошибка регистрации:', error);
      setStatus('Ошибка регистрации');
    }
  };

  const loginUser = async () => {
    try {
      const response = await axios.post(`/api/login`, {
        username,
        password,
      });
      setToken(response.data.token);
      setWalletAddress(response.data.wallet_address);
      setStatus('Успешный вход');
    } catch (error) {
      console.error('Ошибка входа:', error);
      setStatus('Ошибка входа');
    }
  };

  const createPackage = async () => {
    if (!token) {
      setStatus('Сначала войдите');
      return;
    }

    try {
      const response = await axios.post(`/api/create-package`, {
        recipientAddress,
        amount
      }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setHandoff(response.data.handoff);
      setStatus('Передачка создана успешно');
    } catch (error) {
      console.error('Проблема создания передачки:', error);
      setStatus('Проблема создания передачки');
    }
  };

  const redeemPackage = async () => {
    if (!token) {
      setStatus('Сначала войдите');
      return;
    }

    try {
      const response = await axios.post(`/api/redeem-package`, {
        handoff,
      }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setBalance(response.data.balance);
      setStatus('Передачка получена успешно');
    } catch (error) {
      console.error('Ошибка получения передачки:', error);
      setStatus(`Ошибка получения передачки: ${error}`);
    }
  };

  const redeemFlag = async () => {
    if (!token) {
      setStatus('Сначала войдите');
      return;
    }

    try {
      const response = await axios.post(`/api/get-flag`, {
        handoff,
      }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setBalance(response.data.balance);
      setStatus(`Передачка получена успешно: ${response.data.flag}`);
    } catch (error) {
      console.error('Ошибка получения передачки:', error);
      setStatus(`Ошибка получения передачки: ${error}`);
    }
  };

  const checkBalance = async () => {
    if (!token) {
      setStatus('Сначала войдите');
      return;
    }

    try {
      const response = await axios.post(`/api/balance`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setBalance(response.data.balance);
    } catch (error) {
      console.error('Ошибка проверки баланса:', error);
      setStatus('Ошибка проверки баланса');
    }
  };

  return (
    <div className="App">
      <NavBar status={status} />
      <div className="slide" id="slide1">
        <img src={require('./logo.png')} alt="Logo" className="logo-left" />
        <div className="content-container">
          <div className="form-container">
            <h2>Регистрация</h2>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
            />
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
            />
            <button onClick={registerUser}>Зарегистрироваться</button>
          </div>
          <div className="form-container">
            <h2>Вход</h2>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
            />
            <button onClick={loginUser}>Войти</button>
          </div>
        </div>
        <img src={require('./logo.png')} alt="Logo" className="logo-right" />
      </div>

      <div className="slide" id="slide2">
        <div className="content-box">
          <h2>Создать передачку</h2>
          <input
            type="text"
            value={recipientAddress}
            onChange={(e) => setRecipientAddress(e.target.value)}
            placeholder="Адрес кошелька получателя"
          />
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="Количество"
          />
          <button onClick={createPackage}>Создать</button>
          <div>
            <div style={{ height: "auto", margin: "0 auto", maxWidth: 256, width: "100%" }}>
              <QRCode
                size={512}
                style={{ height: "auto", maxWidth: "100%", width: "100%" }}
                value={handoff}
                viewBox={`0 0 256 256`}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="slide" id="slide3">
        <div className="content-box">
          <h2>Получить передачку</h2>
          <input
            type="text"
            value={handoff}
            onChange={(e) => setHandoff(e.target.value)}
            placeholder="Код передачки"
          />
          <button onClick={redeemPackage}>Получить</button>

          <h2>Проверить баланс</h2>
          <button onClick={checkBalance}>Проверить</button>
          <div>
            <strong>Баланс:</strong> <pre>{balance}</pre>
          </div>

          <h2>Секретная передачка</h2>
          <input
            type="text"
            value={handoff}
            onChange={(e) => setHandoff(e.target.value)}
            placeholder="Код передачки"
          />
          <button onClick={redeemFlag}>Получить</button>
        </div>
      </div>
    </div>
  );
}

export default App;