export default function Home() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>Real Estate CRM Tracker</h1>
      <p>Welcome to the Real Estate CRM system!</p>
      <div style={{ marginTop: '20px' }}>
        <a href="/auth/signup" style={{ 
          padding: '10px 20px', 
          backgroundColor: '#007bff', 
          color: 'white', 
          textDecoration: 'none', 
          borderRadius: '5px',
          marginRight: '10px'
        }}>
          Sign Up
        </a>
        <a href="/auth/signin" style={{ 
          padding: '10px 20px', 
          backgroundColor: '#6c757d', 
          color: 'white', 
          textDecoration: 'none', 
          borderRadius: '5px'
        }}>
          Sign In
        </a>
      </div>
    </div>
  );
}
