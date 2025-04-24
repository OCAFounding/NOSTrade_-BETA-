import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost';
  className?: string;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'default', className = '', children, ...props }, ref) => {
    const baseStyles = 'px-4 py-2 rounded-md font-medium transition-colors';
    
    const variantStyles = {
      default: 'bg-blue-600 text-white hover:bg-blue-700',
      outline: 'border border-slate-700 text-white hover:bg-slate-800',
      ghost: 'text-white hover:bg-slate-800'
    };
    
    return (
      <button
        ref={ref}
        className={`${baseStyles} ${variantStyles[variant]} ${className}`}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button'; 