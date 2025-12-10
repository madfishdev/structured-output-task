import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [authToken, setAuthToken] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    
    useEffect(() => {
        const storedAuthToken = localStorage.getItem('authToken');
        if (storedAuthToken) {
            setAuthToken(storedAuthToken);
            setIsAuthenticated(true);
        }
        
        setIsLoading(false);
    }, []);

    const login = async (username, password) => {
        try {
            const response = await api.post(`/login`, { username, password });
            const authToken = response.data.access_token;

            localStorage.setItem('authToken', authToken);
            setAuthToken(authToken);
            setIsAuthenticated(true);
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    };

    const register = async (username, password) => {
        try {
            const response = await api.post(`/register`, { username, password });
            const authToken = response.data.access_token;

            localStorage.setItem('authToken', authToken);
            setAuthToken(authToken);
            setIsAuthenticated(true);
        } catch (error) {
            console.error('Registration failed:', error);
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem('authToken');
        setAuthToken(null);
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ authToken, isAuthenticated, isLoading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => {
    return useContext(AuthContext);
}