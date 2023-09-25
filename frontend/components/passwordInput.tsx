// components/PasswordInput.tsx

import React, { useState } from 'react';

interface PasswordInputProps {
  classNames: string;
  password: string;
  setPassword: (value: string) => void;
}

const PasswordInput: React.FC<PasswordInputProps> = ({ classNames, password, setPassword }) => {
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);

  const togglePasswordVisibility = () => {
    setIsPasswordVisible(!isPasswordVisible);
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', border: '1px solid #ccc', padding: '5px' }}>
      <input
        className={classNames}
        type={isPasswordVisible ? 'text' : 'password'}
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder={"Enter your password"}
        style={{ flex: 1 }}
      />
      <button onClick={togglePasswordVisibility} style={{ marginLeft: '5px' }}>
        {isPasswordVisible ? '🙈' : '👁️'}
      </button>
    </div>
  );
}

export default PasswordInput;
