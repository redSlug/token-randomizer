import React, { useState } from 'react';

const IntegerInput = ({ onChange, defaultValue = 0 }) => {
  const [value, setValue] = useState(defaultValue);

  const handleChange = (e) => {
    const newValue = parseInt(e.target.value, 10);
    if (!isNaN(newValue)) {
      setValue(newValue);
      onChange(newValue);
    }
  };

  return (
      <input
          type="number"
          step="1"
          value={value}
          onChange={handleChange}
      />
  );
};

export default IntegerInput;
