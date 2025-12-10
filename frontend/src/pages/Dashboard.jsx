import { useState} from 'react';
import { useAuth } from '../context/AuthContext';
import { Plus, Trash, Upload, Loader, LogOut, Code, FileText } from 'lucide-react';
import api from '../api';
import '../styles/Dashboard.css';

export default function Dashboard() {
    const { logout } = useAuth();

    const [ prompt, setPrompt ] = useState('');
    const [ imageFile, setImageFile ] = useState(null);
    const [ fields, setFields ] = useState([]);

    const [ isAnalyzing, setIsAnalyzing ] = useState(false);
    const [ result, setResult ] = useState(null);
    const [ error, setError ] = useState(null);

    const handleAddField = () => {
        setFields([ ...fields, { name: '', type: 'string' } ]);
    }

    const handleRemoveField = (index) => {
        const newFields = [ ...fields ];
        newFields.splice(index, 1);
        setFields(newFields);
    }

    const updateField = (index, key, value) => {
        const newFields = [ ...fields ];
        newFields[index][key] = value;
        setFields(newFields);
    }

    const handleSubmit = async () => {
        if (!prompt.trim()) {
            setError('Prompt cannot be empty.');
            return;
        }

        if (fields.length == 0) {
            setError('At least one field must be defined.');
            return;
        }

        setIsAnalyzing(true);
        setError(null);
        setResult(null);

        try {
            const formData = new FormData();
            formData.append('prompt', prompt);
            formData.append('fields', JSON.stringify(fields));
            if (imageFile) {
                formData.append('image', imageFile);
            }

            const response = await api.post('/analyze', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            setResult(response.data);
        } catch (err) {
            let errorMessage = err.response?.data?.detail || 'Analysis failed. Please try again.';
            setError(errorMessage);
        } finally {
            setIsAnalyzing(false);
        }
    }

    return (
        <div className="dashboard-container">
            <nav className="dashboard-nav">
                <div className="nav-logo">
                    <FileText size={20} className="text-blue-600"/>
                    <span>Structured Output Test</span>
                </div>
                <button className="nav-logout" onClick={logout}>
                    <LogOut size={16} /> Logout
                </button>
            </nav>
            <div className="content-wrapper">
                <div className="dashboard-card form-section">
                    <h2 className="section-title">Assignment Task</h2>
                    <div className="input-group">
                        <label className="input-label">Prompt</label>
                        <textarea 
                            className="mono-textarea"
                            placeholder="Enter your prompt here..." 
                            value={prompt}
                            onChange={e => setPrompt(e.target.value)}
                        />
                    </div>
                    <div className="input-group">
                        <label className="input-label">Image (Optional)</label>
                        <label className={`file-upload-box ${imageFile ? 'has-file' : ''}`}>
                            <Upload size={20} strokeWidth={1.5} />
                            <span className="file-name">
                                {imageFile ? imageFile.name : "Choose File..."}
                            </span>
                            <input 
                                type="file" 
                                accept="image/*"
                                hidden
                                onChange={(e) => setImageFile(e.target.files[0])}
                            />
                        </label>
                    </div>
                    <div className="input-group">
                        <div className="label-row">
                            <label className="input-label">Response Structure</label>
                        </div>
                        <div className="fields-stack">
                            {fields.map((field, index) => (
                                <div key={index} className="field-row">
                                    <input 
                                        type="text" 
                                        placeholder="Field Name (e.g. birth_year)" 
                                        value={field.name}
                                        onChange={(e) => updateField(index, 'name', e.target.value)}
                                        className="field-input"
                                    />
                                    <select 
                                        value={field.type}
                                        onChange={(e) => updateField(index, 'type', e.target.value)}
                                        className="field-select"
                                    >
                                        <option value="string">String</option>
                                        <option value="number">Number</option>
                                    </select>
                                    <button 
                                        className="icon-btn danger" 
                                        onClick={() => handleRemoveField(index)}
                                        title="Remove"
                                    >
                                        <Trash size={18} />
                                    </button>
                                </div>
                            ))}
                        </div>
                        <button className="add-field-btn" onClick={handleAddField}>
                            <Plus size={16} /> Add Field
                        </button>
                    </div>
                    {error && (
                        <div className="error-banner">
                            {error}
                        </div>
                    )}
                    <button 
                        className="primary-btn" 
                        onClick={handleSubmit} 
                        disabled={isAnalyzing}
                    >
                        { isAnalyzing ? <Loader className="animate-spin" size={20} /> : "Submit" }
                    </button>
                </div>
                {result && (
                    <div className="dashboard-card result-section">
                        <h3 className="result-header">Structured Output</h3>
                        <div className="result-list">
                            {Object.entries(result).map(([key, value]) => (
                                <div key={key} className="result-row">
                                    <span className="result-key">{key}:</span>
                                    <span className="result-value">{String(value)}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}