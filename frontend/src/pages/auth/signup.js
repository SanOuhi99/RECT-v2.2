import AuthForm from '../../components/auth/AuthForm';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'next/router';

export default function SignUp() {
  const { signup } = useAuth();
  const router = useRouter();

  const handleSignup = async (formData) => {
    try {
      await signup(formData);
      router.push('/dashboard');
    } catch (error) {
      console.error('Signup failed:', error);
    }
  };

  return (
    <AuthForm 
      type="signup" 
      onSubmit={handleSignup}
      title="Create your account"
      subtitle="Join your company's Real Estate CRM"
    />
  );
}