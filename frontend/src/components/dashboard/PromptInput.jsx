export default function PromptInput({ value, onChange }) {
    return (
        <div className="input-group">
            <label className="input-label">Prompt</label>
            <textarea 
                className="mono-textarea"
                placeholder="Enter your prompt here..." 
                value={value}
                onChange={(e) => onChange(e.target.value)}
            />
        </div>
    );
}