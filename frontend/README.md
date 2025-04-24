# NOS Trade Frontend

This is the frontend for the NOS Trade application, providing a modern web interface for interacting with the trading system.

## Features

- **Modern UI/UX**: Built with React, Framer Motion, and Tailwind CSS
- **Chat Interface**: Real-time communication with the NOS Trade AI
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode**: Sleek dark theme with gradient styling

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

2. Start the development server:
   ```bash
   npm start
   # or
   yarn start
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── public/              # Static files
├── src/                 # Source code
│   ├── components/      # React components
│   │   ├── ui/          # UI components
│   │   └── NOSChat.tsx  # Main chat component
│   ├── App.tsx          # Main App component
│   ├── index.tsx        # Entry point
│   └── index.css        # Global styles
├── package.json         # Dependencies and scripts
└── tailwind.config.js   # Tailwind CSS configuration
```

## Development

### Adding New Components

1. Create a new component in the `src/components` directory
2. Import and use the component in `App.tsx` or another component

### Styling

This project uses Tailwind CSS for styling. You can customize the theme in `tailwind.config.js`.

## Building for Production

```bash
npm run build
# or
yarn build
```

This will create a production build in the `build` directory.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details. 