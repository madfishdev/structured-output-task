import { useAuth } from '../../context/AuthContext';
import { LogOut, FileText } from 'lucide-react';

export default function DashboardNav() {
    const { logout } = useAuth();

    return (
        <nav className="dashboard-nav">
            <div className="nav-logo">
                <FileText size={20} className="text-blue-600"/>
                <span>Structured Output Test</span>
            </div>
            <button className="nav-logout" onClick={logout}>
                <LogOut size={16} /> Logout
            </button>
        </nav>
    );
}