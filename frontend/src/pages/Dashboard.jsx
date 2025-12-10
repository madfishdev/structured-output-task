import { useState } from 'react';
import { Loader } from 'lucide-react';
import api from '../api';
import DashboardNav from '../components/dashboard/DashboardNav';
import PromptInput from '../components/dashboard/PromptInput';
import ImageUpload from '../components/dashboard/ImageUpload';
import FieldsBuilder from '../components/dashboard/FieldsBuilder';
import ResultDisplay from '../components/dashboard/ResultDisplay';
import '../styles/Dashboard.css';

export default function Dashboard() {
    const [prompt, setPrompt] = useState('');
    const [imageFile, setImageFile] = useState(null);
    const [fields, setFields] = useState([]);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleAddField = () => {
        setFields([...fields, { name: '', type: 'string' }]);
    };

    const handleRemoveField = (index) => {
        const newFields = [...fields];
        newFields.splice(index, 1);
        setFields(newFields);
    };

    const updateField = (index, key, value) => {
        const newFields = [...fields];
        newFields[index][key] = value;
        setFields(newFields);
    };

    const handleSubmit = async () => {
        if (!prompt.trim()) {
            setError('Prompt cannot be empty.');
            return;
        }

        if (fields.length === 0) {
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
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            setResult(response.data);
        } catch (err) {
            const errorMessage = err.response?.data?.detail || 'Analysis failed. Please try again.';
            setError(errorMessage);
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <div className="dashboard-container">
            <DashboardNav />
            <div className="content-wrapper">
                <div className="dashboard-card form-section">
                    <h2 className="section-title">Assignment Task</h2>
                    <PromptInput value={prompt} onChange={setPrompt} />
                    <ImageUpload file={imageFile} onChange={setImageFile} />
                    <FieldsBuilder fields={fields} onAddField={handleAddField} onRemoveField={handleRemoveField} onUpdateField={updateField}/>
                    {error && <div className="error-banner">{error}</div>}
                    <button 
                        className="primary-btn" 
                        onClick={handleSubmit} 
                        disabled={isAnalyzing}
                    >
                        {isAnalyzing ? <Loader className="animate-spin" size={20} /> : "Submit"}
                    </button>
                </div>

                <ResultDisplay result={result} />
            </div>
        </div>
    );
}