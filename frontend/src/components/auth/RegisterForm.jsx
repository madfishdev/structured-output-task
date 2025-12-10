import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Loader } from 'lucide-react';

export default function RegisterForm() {
  const [ username, setUsername ] = useState('');
  const [ password, setPassword ] = useState('');
  const [ repeatPassword, setRepeatPassword ] = useState('');
  const [ error, setError ] = useState(null);
  const [ isLoading, setIsLoading ] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleRegister = async () => {
    setIsLoading(true);
    setError(null);
    if (password !== repeatPassword) {
      setError('Passwords do not match.');
      setIsLoading(false);
      return;
    }
    try {
      await register(username, password);
      navigate('/');
    } catch (err) {
        let errorMessage = err.response?.data?.detail || 'Registration failed. Please try again.';
      setError(errorMessage);
    }
    finally {
      setIsLoading(false);
    }
  }

  return (
    <div className='form-stack'>
      <h2 className='auth-title'>Register</h2>
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
      <input
        className='form-input'
        type='password'
        placeholder='Repeat Password'
        value={repeatPassword}
        onChange={(e) => setRepeatPassword(e.target.value)}
      />
      <button
        className='submit-btn'
        onClick={handleRegister}
        disabled={isLoading}
      >
        { isLoading ? <Loader className='animate-spin' size={20} /> : 'Register' }
      </button>
    </div>
  );
}