import React from 'react';
import ReactDOM from 'react-dom/client';
import AppWrapper from './app'; 



const rootElement = document.getElementById('root');
console.log('rootElement:', rootElement); // Should NOT be null

const root = ReactDOM.createRoot(rootElement);
root.render(<AppWrapper />);