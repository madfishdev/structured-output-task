import { Plus, Trash } from 'lucide-react';

export default function FieldsBuilder({ fields, onAddField, onRemoveField, onUpdateField }) {
    return (
        <div className="input-group">
            <div className="label-row">
                <label className="input-label">Response Structure</label>
            </div>
            <div className="fields-stack">
                {fields.map((field, index) => (
                    <div key={index} className="field-row">
                        <input 
                            className="field-input"
                            type="text" 
                            placeholder="Field Name (e.g. birth_year)" 
                            value={field.name}
                            onChange={(e) => onUpdateField(index, 'name', e.target.value)}
                        />
                        <select 
                            className="field-select"
                            value={field.type}
                            onChange={(e) => onUpdateField(index, 'type', e.target.value)}
                        >
                            <option value="string">String</option>
                            <option value="number">Number</option>
                        </select>
                        <button 
                            className="icon-btn danger" 
                            onClick={() => onRemoveField(index)}
                            title="Remove"
                        >
                            <Trash size={18} />
                        </button>
                    </div>
                ))}
            </div>
            <button className="add-field-btn" onClick={onAddField}>
                <Plus size={16} /> Add Field
            </button>
        </div>
    );
}