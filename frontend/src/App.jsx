import { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    Age: '',
    Sex: 'M',
    ChestPainType: 'ATA',
    RestingBP: '',
    Cholesterol: '',
    FastingBS: '0',
    RestingECG: 'Normal',
    MaxHR: '',
    ExerciseAngina: 'N',
    Oldpeak: '',
    ST_Slope: 'Up'
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    // Convert numeric fields
    const payload = {
      ...formData,
      Age: Number(formData.Age),
      RestingBP: Number(formData.RestingBP),
      Cholesterol: Number(formData.Cholesterol),
      FastingBS: Number(formData.FastingBS),
      MaxHR: Number(formData.MaxHR),
      Oldpeak: Number(formData.Oldpeak)
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Server error occurred');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      if (err.message === 'Failed to fetch') {
        setError('Cannot reach the prediction server. Please ensure the backend is running on localhost:5000.');
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <div className="cardiac-logo">🫀</div>
        <h1>CardioDetect </h1>
        <p>Professional Clinical Decision Support System for Heart Disease Assessment</p>
      </header>

      <main className="glass-panel">
        <form onSubmit={handleSubmit} className="prediction-form">
          <div className="form-grid">
            <div className="input-group">
              <label htmlFor="Age">Age (1-120)</label>
              <input type="number" id="Age" name="Age" value={formData.Age} onChange={handleChange} required min="1" max="120" placeholder="e.g., 45" />
              <span className="helper-text">Patient age in years.</span>
            </div>

            <div className="input-group">
              <label htmlFor="Sex">Sex</label>
              <select id="Sex" name="Sex" value={formData.Sex} onChange={handleChange}>
                <option value="M">Male</option>
                <option value="F">Female</option>
              </select>
              <span className="helper-text">Biological sex at birth.</span>
            </div>

            <div className="input-group">
              <label htmlFor="ChestPainType">Chest Pain Type</label>
              <select id="ChestPainType" name="ChestPainType" value={formData.ChestPainType} onChange={handleChange}>
                <option value="ATA">Atypical Angina (ATA)</option>
                <option value="NAP">Non-Anginal Pain (NAP)</option>
                <option value="ASY">Asymptomatic (ASY)</option>
                <option value="TA">Typical Angina (TA)</option>
              </select>
              <span className="helper-text">TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic.</span>
            </div>

            <div className="input-group">
              <label htmlFor="RestingBP">Resting BP (60-250 mm Hg)</label>
              <input type="number" id="RestingBP" name="RestingBP" value={formData.RestingBP} onChange={handleChange} required min="60" max="250" placeholder="e.g., 120" />
              <span className="helper-text">Resting blood pressure on admission.</span>
            </div>

            <div className="input-group">
              <label htmlFor="Cholesterol">Cholesterol (0-600 mg/dl)</label>
              <input type="number" id="Cholesterol" name="Cholesterol" value={formData.Cholesterol} onChange={handleChange} required min="0" max="600" placeholder="e.g., 200" />
              <span className="helper-text">Serum cholesterol level.</span>
            </div>

            <div className="input-group">
              <label htmlFor="FastingBS">Fasting Blood Sugar {'>'} 120 mg/dl</label>
              <select id="FastingBS" name="FastingBS" value={formData.FastingBS} onChange={handleChange}>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
              <span className="helper-text">Fasting blood sugar level {'>'} 120 mg/dl.</span>
            </div>

            <div className="input-group">
              <label htmlFor="RestingECG">Resting ECG</label>
              <select id="RestingECG" name="RestingECG" value={formData.RestingECG} onChange={handleChange}>
                <option value="Normal">Normal</option>
                <option value="ST">ST-T Wave Abnormality</option>
                <option value="LVH">Left Ventricular Hypertrophy</option>
              </select>
              <span className="helper-text">ST: ST-T wave abnormality, LVH: Left ventricular hypertrophy.</span>
            </div>

            <div className="input-group">
              <label htmlFor="MaxHR">Max Heart Rate (60-220)</label>
              <input type="number" id="MaxHR" name="MaxHR" value={formData.MaxHR} onChange={handleChange} required min="60" max="220" placeholder="e.g., 150" />
              <span className="helper-text">Maximum heart rate achieved during stress test.</span>
            </div>

            <div className="input-group">
              <label htmlFor="ExerciseAngina">Exercise Induced Angina</label>
              <select id="ExerciseAngina" name="ExerciseAngina" value={formData.ExerciseAngina} onChange={handleChange}>
                <option value="N">No</option>
                <option value="Y">Yes</option>
              </select>
              <span className="helper-text">Chest pain induced by physical exertion.</span>
            </div>

            <div className="input-group">
              <label htmlFor="Oldpeak">Oldpeak (-2.6 to 6.2)</label>
              <input type="number" step="0.1" id="Oldpeak" name="Oldpeak" value={formData.Oldpeak} onChange={handleChange} required min="-2.6" max="6.2" placeholder="e.g., 1.5" />
              <span className="helper-text">ST depression induced by exercise relative to rest.</span>
            </div>

            <div className="input-group">
              <label htmlFor="ST_Slope">ST Slope</label>
              <select id="ST_Slope" name="ST_Slope" value={formData.ST_Slope} onChange={handleChange}>
                <option value="Up">Upsloping</option>
                <option value="Flat">Flat</option>
                <option value="Down">Downsloping</option>
              </select>
              <span className="helper-text">The slope of the peak exercise ST segment.</span>
            </div>
          </div>


          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? <span className="loader"></span> : 'Generate Assessment'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            <div className="error-content">
              <strong>System Error</strong>
              <p>{error}</p>
            </div>
          </div>
        )}

        {result && (
          <div className={`result-card ${result.prediction === 1 ? 'high-risk' : 'low-risk'}`}>
            <div className="result-header">
              <h2>{result.prediction === 1 ? 'Elevated Cardiac Risk' : 'Low Cardiac Risk'}</h2>
              <span className="status-badge">{result.prediction === 1 ? 'Immediate Review' : 'Stable'}</span>
            </div>

            <p className="message">{result.message}</p>

            {result.probability !== null && (
              <div className="risk-meter-container">
                <div className="risk-labels">
                  <span className="risk-label-text">Calculated Probability</span>
                  <span className="risk-percent">{(result.probability * 100).toFixed(1)}%</span>
                </div>
                <div className="risk-track">
                  <div
                    className="risk-bar"
                    style={{
                      width: `${result.probability * 100}%`,
                      background: result.probability > 0.7 ? '#ef4444' : result.probability > 0.4 ? '#f59e0b' : '#10b981'
                    }}
                  ></div>
                </div>
              </div>
            )}

            <div className="clinical-details">
              <div className="detail-item">
                <h4> What this means</h4>
                <p>
                  {result.prediction === 1
                    ? "Our analysis indicates multiple indicators associated with cardiovascular pathology. This score suggests a higher likelihood of existing heart disease based on the provided clinical features."
                    : "The patient's clinical profile aligns with low-risk patterns in the training cohort. Most cardiovascular indicators are within standard parameters."}
                </p>
              </div>
              <div className="detail-item">
                <h4> Clinical Guidance</h4>
                <p>
                  {result.prediction === 1
                    ? "Recommended next steps: Schedule a comprehensive cardiovascular evaluation, including a stress test or imaging, as soon as possible."
                    : "Recommended next steps: Continue regular health screenings and maintain a heart-healthy lifestyle. Monitor for any new or unusual symptoms."}
                </p>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="footer-disclaimer">
        <p>
          <strong>MEDICAL DISCLAIMER:</strong> This tool is for informational and educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. The predictions are generated by an AI model trained on historical data and may contain errors. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
        </p>
      </footer>
    </div>
  );
}

export default App;
