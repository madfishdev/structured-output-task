import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Authentication from './pages/Authentication';
import Dashboard from './pages/Dashboard';

// Protect routes based on authentication status
const PrivateRoute = ({ children }) => {
    const { isAuthenticated, isLoading } = useAuth();
    if (isLoading) {
        return <div>Loading...</div>;
    }
    return isAuthenticated ? children : <Navigate to="/login" replace />;
}

// Redirect authenticated users away from auth pages
const PublicRoute = ({ children }) => {
    const { isAuthenticated, isLoading } = useAuth();
    if (isLoading) {
        return <div>Loading...</div>;
    }
    return !isAuthenticated ? children : <Navigate to="/" replace />;
}

function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Routes>
                    <Route path="/login" element={ <PublicRoute><Authentication /></PublicRoute> } />
                    <Route path="/" element={ <PrivateRoute><Dashboard /></PrivateRoute> } />
                    <Route path="*" element={ <Navigate to="/" replace /> } />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;