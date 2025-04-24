import React from 'react';

interface CardProps {
  className?: string;
  children: React.ReactNode;
}

export const Card = ({ className = '', children }: CardProps) => {
  return (
    <div className={`bg-slate-800 rounded-lg shadow-md ${className}`}>
      {children}
    </div>
  );
};

interface CardContentProps {
  className?: string;
  children: React.ReactNode;
}

export const CardContent = ({ className = '', children }: CardContentProps) => {
  return (
    <div className={`p-4 ${className}`}>
      {children}
    </div>
  );
}; 