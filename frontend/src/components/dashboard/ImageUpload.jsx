import { Upload } from 'lucide-react';

export default function ImageUpload({ file, onChange }) {
    return (
        <div className="input-group">
            <label className="input-label">Image (Optional)</label>
            <label className={`file-upload-box ${file ? 'has-file' : ''}`}>
                <Upload size={20} strokeWidth={1.5} />
                <span className="file-name">
                    {file ? file.name : "Choose File..."}
                </span>
                <input 
                    type="file" 
                    accept="image/*"
                    hidden
                    onChange={(e) => onChange(e.target.files[0])}
                />
            </label>
        </div>
    );
}