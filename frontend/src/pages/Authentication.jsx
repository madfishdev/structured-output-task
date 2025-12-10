import { useState } from 'react';
import LoginForm from '../components/auth/LoginForm';
import RegisterForm from '../components/auth/RegisterForm';
import '../styles/Authentication.css';

export default function Authentication() {
  const [ isLoginMode, setIsLoginMode ] = useState(true);

  return (
    <div className='auth-page-container'>
      <div className='auth-card'>
        { isLoginMode ? <LoginForm /> : <RegisterForm /> }
        <div className='toggle-area'>
          { isLoginMode ? (
            <>
              Don't have an account?{' '}<button className="toggle-link" onClick={() => setIsLoginMode(false)}>Register here</button>
            </>
          ) : (
            <>
              Already have an account?{' '}<button className="toggle-link" onClick={() => setIsLoginMode(true)}>Login here</button>
            </>
          ) }
        </div>
      </div>
    </div>
  );
}