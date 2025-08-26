# GraphRAG Frontend

This is the Next.js frontend for the UAE Legal GraphRAG application. It provides a modern, responsive web interface for interacting with the legal knowledge graph and RAG system.

## Features

- **Modern UI/UX**: Built with Next.js, TypeScript, and Tailwind CSS
- **Real-time Chat**: Interactive chat interface for legal queries
- **Graph Visualization**: Interactive knowledge graph display
- **Responsive Design**: Mobile-first responsive design
- **Type Safety**: Full TypeScript support
- **Performance Optimized**: Next.js optimizations and code splitting

## Tech Stack

- **Framework**: Next.js 13+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React hooks and context
- **HTTP Client**: Axios
- **Graph Visualization**: D3.js / React Force Graph
- **UI Components**: Custom components with Tailwind

## Project Structure

```
frontend/
├── components/           # Reusable React components
│   ├── ui/              # Base UI components
│   ├── chat/            # Chat-related components
│   ├── graph/           # Graph visualization components
│   └── layout/          # Layout components
├── pages/               # Next.js pages (if using pages router)
├── app/                 # Next.js app directory
├── lib/                 # Utility libraries and configurations
├── utils/               # Helper functions
├── types/               # TypeScript type definitions
├── styles/              # Global styles and CSS modules
├── public/              # Static assets
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── tailwind.config.js   # Tailwind CSS configuration
├── next.config.js       # Next.js configuration
└── README.md           # This file
```

## Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running (see backend README)

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Environment Variables

Create a `.env.local` file in the frontend directory:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1

# Feature Flags
NEXT_PUBLIC_ENABLE_GRAPH_VISUALIZATION=true
NEXT_PUBLIC_ENABLE_ANALYTICS=false

# External Services
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=your-ga-id
```

## Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript type checking

# Testing
npm run test         # Run tests
npm run test:watch   # Run tests in watch mode
npm run test:coverage # Run tests with coverage

# Code Quality
npm run format       # Format code with Prettier
npm run lint:fix     # Fix ESLint issues
```

## Development

### Code Style

The project uses:
- **ESLint** for code linting
- **Prettier** for code formatting
- **TypeScript** for type safety
- **Tailwind CSS** for styling

### Component Structure

```typescript
// Example component structure
interface ComponentProps {
  title: string;
  onAction?: () => void;
}

export const Component: React.FC<ComponentProps> = ({ title, onAction }) => {
  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-xl font-semibold">{title}</h2>
      {onAction && (
        <button 
          onClick={onAction}
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
        >
          Action
        </button>
      )}
    </div>
  );
};
```

### API Integration

The frontend communicates with the backend API using axios:

```typescript
// Example API call
import { apiClient } from '@/lib/api';

const sendChatMessage = async (message: string) => {
  try {
    const response = await apiClient.post('/api/chat', {
      message,
      strategy: 'hybrid',
      max_results: 10
    });
    return response.data;
  } catch (error) {
    console.error('Chat error:', error);
    throw error;
  }
};
```

## Key Components

### Chat Interface

The main chat component provides:
- Real-time message exchange
- Message history
- Source citations
- Loading states
- Error handling

### Graph Visualization

Interactive knowledge graph display with:
- Node and edge visualization
- Zoom and pan controls
- Node selection and details
- Search and filtering

### Layout Components

- **Header**: Navigation and branding
- **Sidebar**: Additional controls and information
- **Footer**: Links and metadata

## Styling

### Tailwind CSS

The project uses Tailwind CSS for styling with a custom configuration:

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          // ... more shades
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
};
```

### Custom CSS

Global styles are defined in `styles/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600;
  }
}
```

## Testing

### Test Structure

- **Unit Tests**: Component testing with React Testing Library
- **Integration Tests**: API integration testing
- **E2E Tests**: End-to-end testing with Playwright

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

## Performance Optimization

### Next.js Optimizations

- **Image Optimization**: Using Next.js Image component
- **Code Splitting**: Automatic code splitting by pages
- **Static Generation**: Pre-rendering static pages
- **Incremental Static Regeneration**: Dynamic content with static benefits

### Bundle Analysis

```bash
# Analyze bundle size
npm run analyze
```

## Deployment

### Vercel (Recommended)

1. **Connect your repository to Vercel**
2. **Set environment variables in Vercel dashboard**
3. **Deploy automatically on push to main branch**

### Other Platforms

The app can be deployed to any platform that supports Next.js:

- **Netlify**: Use `npm run build` and `npm run start`
- **AWS Amplify**: Configure build settings
- **Docker**: Use the provided Dockerfile

### Docker Deployment

```bash
# Build the image
docker build -t graphrag-frontend .

# Run the container
docker run -p 3000:3000 graphrag-frontend
```

## Monitoring and Analytics

### Error Tracking

- **Sentry**: Error monitoring and performance tracking
- **Console Logging**: Development error logging

### Analytics

- **Google Analytics**: User behavior tracking
- **Custom Metrics**: Performance and usage metrics

## Security

### Best Practices

- **Input Validation**: All user inputs are validated
- **XSS Prevention**: React's built-in XSS protection
- **CSP Headers**: Content Security Policy headers
- **HTTPS**: Secure communication with backend

### Environment Variables

- Never commit sensitive data to version control
- Use environment variables for configuration
- Validate environment variables at runtime

## Troubleshooting

### Common Issues

1. **Build Errors**
   - Check TypeScript errors: `npm run type-check`
   - Verify all dependencies are installed
   - Clear Next.js cache: `rm -rf .next`

2. **API Connection Issues**
   - Verify backend is running
   - Check API URL in environment variables
   - Test API endpoints directly

3. **Styling Issues**
   - Verify Tailwind CSS is properly configured
   - Check for CSS conflicts
   - Use browser dev tools to inspect styles

### Debug Mode

Enable debug mode for detailed logging:

```bash
# Set debug environment variable
export DEBUG=true
npm run dev
```

## Contributing

1. **Follow the existing code style and patterns**
2. **Add tests for new components**
3. **Update documentation for new features**
4. **Ensure all tests pass before submitting**

### Development Workflow

1. Create a feature branch
2. Make your changes
3. Add tests
4. Run linting and type checking
5. Submit a pull request

## License

This project is part of the UAE Legal GraphRAG application.
