import AuthForm from '../../components/auth/AuthForm';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'next/router';

export default function SignIn() {
  const { login } = useAuth();
  const router = useRouter();

  const handleLogin = async (formData) => {
    try {
      await login(formData.email, formData.password);
      router.push('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <AuthForm 
      type="signin" 
      onSubmit={handleLogin}
      title="Sign in to your account"
      subtitle="Welcome back to Real Estate CRM"
    />
  );
}