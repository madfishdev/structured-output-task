export default function ResultDisplay({ result }) {
    if (!result) return null;

    return (
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
    );
}