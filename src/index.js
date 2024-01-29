import React from 'react';
import ReactDOM from 'react-dom/client';
import { Auth0Provider } from '@auth0/auth0-react';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Auth0Provider
    domain="dev-qtcp208o1o3772dz.us.auth0.com"
    clientId="sDLvhi1eJeJFt5bgwgc1DTCaqceMgQ4R"
    authorizationParams={{ redirect_uri: window.location.origin }}
    useRefreshTokens={true}
    cacheLocation="localstorage"
  >
  <React.StrictMode>
    <App />
  </React.StrictMode>
  </Auth0Provider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
