import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Loader } from 'lucide-react';
import '../styles/Authentication.css';

export default function LoginForm() {
  const [ username, setUsername ] = useState('');
  const [ password, setPassword ] = useState('');
  const [ error, setError ] = useState(null);
  const [ isLoading, setIsLoading ] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await login(username, password);
      navigate('/');
    } catch (err) {
        let errorMessage = err.response?.data?.detail || 'Login failed. Please check your credentials.';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className='form-stack'>
      <h2 className='auth-title'>Login</h2>
      { error && <div className='error-box'>{error}</div> }
      <input
        className='form-input'
        type='text'
        placeholder='Username'
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        className='form-input'
        type='password'
        placeholder='Password'
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button
        className='submit-btn'
        onClick={handleLogin}
        disabled={isLoading}
      >
        { isLoading ? <Loader className='animate-spin' size={20} /> : 'Login' }
      </button>
    </div>
  );
}