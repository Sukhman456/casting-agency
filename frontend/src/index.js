import React from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  return <h1>Hello Casting Agency</h1>;
}

const rootElement = document.getElementById('root');
console.log('rootElement:', rootElement); // Should NOT be null

const root = ReactDOM.createRoot(rootElement);
root.render(<App />);