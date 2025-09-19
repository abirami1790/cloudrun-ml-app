import React, { useState } from "react";
import { useToken } from "./TokenContext";

function IrisForm({ onResult }) {
  const { idToken } = useToken();
  const [form, setForm] = useState({
    sepal_length: "",
    sepal_width: "",
    petal_length: "",
    petal_width: "",
  });
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    if (!idToken) {
      setError("Authentication required. Please log in.");
      return;
    }
    try {
      // Send request to App A proxy endpoint
  const response = await fetch("https://app-a-357536902999.asia-south1.run.app/route/b/predict/iris", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // Pass Firebase ID token for App A proxy authentication
          Authorization: `Bearer ${idToken}`,
        },
        body: JSON.stringify({
          sepal_length: parseFloat(form.sepal_length),
          sepal_width: parseFloat(form.sepal_width),
          petal_length: parseFloat(form.petal_length),
          petal_width: parseFloat(form.petal_width),
        }),
      });
      if (!response.ok) {
        let errorText = await response.text();
        if (response.status === 401 || response.status === 403) {
          setError("Access denied. Please ensure you are logged in and have permission to access the service.");
        } else if (response.status === 400) {
          setError("Invalid input or request. Please check your data.");
        } else {
          setError(`Server error (${response.status}): ${errorText}`);
        }
        return;
      }
      const data = await response.json();
      onResult(data);
    } catch (err) {
      if (err.name === "TypeError") {
        setError("Network error. Please check your connection or CORS settings.");
      } else {
        setError(`Unexpected error: ${err.message}`);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: 12, display: 'flex', flexDirection: 'column', gap: 12 }}>
      <div style={{ display: 'flex', gap: 8 }}>
        <input
          name="sepal_length"
          placeholder="Sepal Length"
          value={form.sepal_length}
          onChange={handleChange}
          required
          type="number"
          step="any"
          style={{ flex: 1, padding: 8, borderRadius: 6, border: '1px solid #cbd5e1', background: '#f8fafc' }}
        />
        <input
          name="sepal_width"
          placeholder="Sepal Width"
          value={form.sepal_width}
          onChange={handleChange}
          required
          type="number"
          step="any"
          style={{ flex: 1, padding: 8, borderRadius: 6, border: '1px solid #cbd5e1', background: '#f8fafc' }}
        />
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <input
          name="petal_length"
          placeholder="Petal Length"
          value={form.petal_length}
          onChange={handleChange}
          required
          type="number"
          step="any"
          style={{ flex: 1, padding: 8, borderRadius: 6, border: '1px solid #cbd5e1', background: '#f8fafc' }}
        />
        <input
          name="petal_width"
          placeholder="Petal Width"
          value={form.petal_width}
          onChange={handleChange}
          required
          type="number"
          step="any"
          style={{ flex: 1, padding: 8, borderRadius: 6, border: '1px solid #cbd5e1', background: '#f8fafc' }}
        />
      </div>
      <button type="submit" style={{ marginTop: 8, padding: '10px 0', borderRadius: 6, background: '#3182ce', color: '#fff', fontWeight: 600, border: 'none', fontSize: 16, cursor: 'pointer', transition: 'background 0.2s' }}>
        Predict
      </button>
      {error && <div style={{ color: "#e53e3e", marginTop: 4 }}>Error: {error}</div>}
    </form>
  );
}


// Show the prediction as plain text if available
export function IrisPredictionResult({ result }) {
  if (!result) return null;
  // Accept both { prediction: "setosa" } and { prediction: 1 }
  let label = result.prediction;
  if (typeof label === 'number') {
    const irisTypes = ["setosa", "versicolor", "virginica"];
    label = irisTypes[label] || label;
  }
  return (
    <div style={{ marginTop: 28, background: '#f0fff4', border: '1px solid #38a169', borderRadius: 8, padding: 16 }}>
      <h3 style={{ color: '#276749', margin: 0, marginBottom: 8 }}>Iris Prediction Result:</h3>
      <div style={{ color: '#22543d', fontWeight: 600, fontSize: 18 }}>{label}</div>
    </div>
  );
}

export default IrisForm;
