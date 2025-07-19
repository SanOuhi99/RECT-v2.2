export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

export const validatePassword = (password) => {
  return password.length >= 8;
};

export const validateCompanyCode = (code) => {
  return code.length >= 4;
};

export const validateKvCoreToken = (token) => {
  return token.length >= 50;
};

export const validateForm = (formData) => {
  const errors = {};
  
  if (!formData.email) {
    errors.email = 'Email is required';
  } else if (!validateEmail(formData.email)) {
    errors.email = 'Invalid email address';
  }
  
  if (!formData.password) {
    errors.password = 'Password is required';
  } else if (!validatePassword(formData.password)) {
    errors.password = 'Password must be at least 8 characters';
  }
  
  if (formData.company_code && !validateCompanyCode(formData.company_code)) {
    errors.company_code = 'Company code must be at least 4 characters';
  }
  
  if (formData.kvcore_token && !validateKvCoreToken(formData.kvcore_token)) {
    errors.kvcore_token = 'Token appears invalid';
  }
  
  return errors;
};