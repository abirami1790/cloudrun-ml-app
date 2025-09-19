
import React, { useState } from 'react';
import Login from './Login';
import IrisForm, { IrisPredictionResult } from './IrisForm';
import { TokenProvider, useToken } from './TokenContext';

function MainApp() {
  const { idToken, setIdToken } = useToken();
  const [irisResult, setIrisResult] = useState(null);
  const [error, setError] = useState('');

  // User must log in to get Firebase ID token for App A proxy
  if (!idToken) {
    return <Login onLogin={setIdToken} />;
  }

  return (
    <div style={{ minHeight: '100vh', background: '#f6f8fa', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ background: '#fff', borderRadius: 12, boxShadow: '0 2px 16px rgba(0,0,0,0.08)', padding: 36, maxWidth: 420, width: '100%' }}>
        <h1 style={{ textAlign: 'center', marginBottom: 8, color: '#2d3748' }}>Iris Predictor</h1>
        <p style={{ textAlign: 'center', color: '#4a5568', marginBottom: 24 }}>You are logged in.</p>
        <IrisForm onResult={setIrisResult} />
        <IrisPredictionResult result={irisResult} />
        {irisResult && (
          <div style={{ marginTop: 28, background: '#f0fff4', border: '1px solid #38a169', borderRadius: 8, padding: 16 }}>
            <h3 style={{ color: '#276749', margin: 0, marginBottom: 8 }}>Iris Prediction Result:</h3>
            <pre style={{ background: 'none', padding: 0, color: '#22543d', fontWeight: 500 }}>{JSON.stringify(irisResult, null, 2)}</pre>
          </div>
        )}
        {error && <div style={{ color: '#e53e3e', marginTop: 16 }}>{error}</div>}
      </div>
    </div>
  );
}

export default function App() {
  return (
    <TokenProvider>
      <MainApp />
    </TokenProvider>
  );
}
