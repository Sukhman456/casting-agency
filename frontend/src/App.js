import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Auth0Provider, useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const API_URL = process.env.REACT_APP_API_URL;

/* 🔹 Navigation bar with login/logout */
const NavBar = () => {
  const { logout, isAuthenticated, user } = useAuth0();
  return (
    <nav style={{ padding: '10px', background: '#f2f2f2', display: 'flex', justifyContent: 'space-between' }}>
      <div>
        {isAuthenticated && (
          <>
            <Link to="/movies" style={{ marginRight: '10px' }}>Movies</Link>
            <Link to="/actors">Actors</Link>
          </>
        )}
      </div>
      <div>
        {isAuthenticated && user && <span style={{ marginRight: '10px' }}>{user.name}</span>}
        {isAuthenticated && (
          <button onClick={() => logout({ returnTo: window.location.origin })}>Logout</button>
        )}
      </div>
    </nav>
  );
};


/* 🔹 Public Home page with login */
const Home = () => {
  const { loginWithRedirect, isAuthenticated } = useAuth0();
  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Welcome to Casting Agency</h1>
      {!isAuthenticated && <button onClick={() => loginWithRedirect()}>Login</button>}
    </div>
  );
};

/* 🔹 Debug token & permissions */
const DebugToken = () => {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();
  const [token, setToken] = useState('');
  const [permissions, setPermissions] = useState([]);

  useEffect(() => {
    const fetchToken = async () => {
      if (isAuthenticated) {
        const t = await getAccessTokenSilently({
          audience: process.env.REACT_APP_AUTH0_AUDIENCE,
        });
        setToken(t);
        const decoded = jwtDecode(t);
        setPermissions(decoded.permissions || []);
        console.log('🔑 Access Token:', t);
        console.log('🔍 Decoded Token:', decoded);
      }
    };
    fetchToken();
  }, [getAccessTokenSilently, isAuthenticated]);

  if (!isAuthenticated) return null;
  return (
    <div style={{ padding: '10px', background: '#eaeaea', marginTop: '10px' }}>
      <h4>Access Token:</h4>
      <p style={{ fontSize: '12px', wordWrap: 'break-word' }}>{token}</p>
      <h4>Permissions:</h4>
      <ul>
        {permissions.map(p => <li key={p}>{p}</li>)}
      </ul>
    </div>
  );
};

/* 🔹 Movies component */
const MoviesComponent = () => {
  const { getAccessTokenSilently } = useAuth0();
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const token = await getAccessTokenSilently({
          audience: process.env.REACT_APP_AUTH0_AUDIENCE,
        });
        const res = await axios.get(`${API_URL}/movies`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setMovies(res.data.movies || []);
      } catch (err) {
        console.error(' Movies fetch error:', err.response ? err.response.data : err.message);
      }
    };
    fetchMovies();
  }, [getAccessTokenSilently]);

  return (
    <div>
      <h2>Movies</h2>
      <ul>
        {movies.map(m => <li key={m.id}>{m.title} - {m.release_date}</li>)}
      </ul>
      <DebugToken />
    </div>
  );
};

/* 🔹 Actors component */
const ActorsComponent = () => {
  const { getAccessTokenSilently } = useAuth0();
  const [actors, setActors] = useState([]);

  useEffect(() => {
    const fetchActors = async () => {
      try {
        const token = await getAccessTokenSilently({
          audience: process.env.REACT_APP_AUTH0_AUDIENCE,
        });
        const res = await axios.get(`${API_URL}/actors`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setActors(res.data.actors || []);
      } catch (err) {
        console.error('❌ Actors fetch error:', err.response ? err.response.data : err.message);
      }
    };
    fetchActors();
  }, [getAccessTokenSilently]);

  return (
    <div>
      <h2>Actors</h2>
      <ul>
        {actors.map(a => <li key={a.id}>{a.name} - {a.age} - {a.gender}</li>)}
      </ul>
      <DebugToken />
    </div>
  );
};

/* 🔹 Protect routes */
const ProtectedMovies = withAuthenticationRequired(MoviesComponent);
const ProtectedActors = withAuthenticationRequired(ActorsComponent);

/* 🔹 Auth0 Provider wrapper */
function AppWrapper() {
  const domain = process.env.REACT_APP_AUTH0_DOMAIN;
  const clientId = process.env.REACT_APP_AUTH0_CLIENT_ID;
  const audience = process.env.REACT_APP_AUTH0_AUDIENCE;

  return (
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        redirect_uri: window.location.origin,
        audience: audience
      }}
    >
      <Router>
        <NavBar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/movies" element={<ProtectedMovies />} />
          <Route path="/actors" element={<ProtectedActors />} />
        </Routes>
      </Router>
    </Auth0Provider>
  );
}

export default AppWrapper;
