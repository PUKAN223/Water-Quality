import React from 'react';

const PercentageCircle = ({ value, maxValue = 1200, size = 100, strokeWidth = 10, color = "#4caf50" }: { value: number, maxValue: number, size: number, strokeWidth: number, color: string }) => {
  // Calculate the percentage based on the value and maxValue
  const percentage = Math.min((value / maxValue) * 100, 100);

  // Calculate the radius and circumference for the circle
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="flex items-center justify-center">
      <svg
        width={size}
        height={size}
        viewBox="0 0 100 100"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Background Circle */}
        <circle
          cx="50"
          cy="50"
          r={radius}
          stroke="#e6e6e6"
          strokeWidth={strokeWidth}
          fill="none"
        />
        {/* Foreground Circle (Percentage Circle) */}
        <circle
          cx="50"
          cy="50"
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
        />
        <text x="50%" y="50%" textAnchor="middle" stroke="#51c5cf" strokeWidth="1px" dy=".3em" fontSize="20">
          {Math.round(percentage)}%
        </text>
      </svg>
    </div>
  );
};

export default PercentageCircle;
