// ControlledCheckbox.tsx

import React from 'react';

interface ControlledCheckboxProps {
  isChecked: boolean;
  onChange: (checked: boolean) => void;
}

const ControlledCheckbox: React.FC<ControlledCheckboxProps> = ({ isChecked, onChange }) => {
  return (
    <input
      type="checkbox"
      checked={isChecked}
      onChange={(e) => onChange(e.target.checked)}
    />
  );
}

export default ControlledCheckbox;
