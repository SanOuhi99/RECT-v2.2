import { useState } from 'react';

export default function SignUp() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    fullName: '',
    companyCode: '',
    kvcoreToken: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Signup data:', formData);
    
    try {
      const response = await fetch('/api/v1/onboarding/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const result = await response.json();
      console.log('Signup result:', result);
    } catch (error) {
      console.error('Signup error:', error);
    }
  };

  return (
    <div style={{ 
      padding: '20px', 
      maxWidth: '400px', 
      margin: '50px auto',
      border: '1px solid #ddd',
      borderRadius: '8px',
      backgroundColor: '#f9f9f9'
    }}>
      <h1 style={{ textAlign: 'center', marginBottom: '30px' }}>Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label>Full Name:</label>
          <input
            type="text"
            value={formData.fullName}
            onChange={(e) => setFormData({...formData, fullName: e.target.value})}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            required
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label>Email:</label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            required
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label>Password:</label>
          <input
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            required
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label>Company Code:</label>
          <input
            type="text"
            value={formData.companyCode}
            onChange={(e) => setFormData({...formData, companyCode: e.target.value})}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            placeholder="WWSZ1HWOXQ7OTHTBX28LZE89PH3DIDJPPALXXFONOFEVA1HC53"
            required
          />
        </div>
        
        <div style={{ marginBottom: '20px' }}>
          <label>KvCore Token:</label>
          <input
            type="text"
            value={formData.kvcoreToken}
            onChange={(e) => setFormData({...formData, kvcoreToken: e.target.value})}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            required
          />
        </div>
        
        <button 
          type="submit" 
          style={{ 
            width: '100%', 
            padding: '12px', 
            backgroundColor: '#007bff', 
            color: 'white', 
            border: 'none',
            borderRadius: '5px',
            fontSize: '16px'
          }}
        >
          Create Account
        </button>
      </form>
      
      <p style={{ textAlign: 'center', marginTop: '20px' }}>
        <a href="/auth/signin">Already have an account? Sign in</a>
      </p>
    </div>
  );
}
