# Deployment Guide

This guide covers deploying the UAE Legal GraphRAG system for different environments, from development to production.

## 🚀 Quick Deployment

### For Presentations/Demos

```bash
# 1. Clone and setup
git clone <repository-url>
cd internship_GraphRAG
python setup.py

# 2. Start the application
python start.py
```

**Access URLs:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8012
- API Docs: http://localhost:8012/docs

## 🔧 Environment-Specific Deployments

### Development Environment

**Prerequisites:**
- Python 3.8+
- Node.js 16+
- Neo4j (optional)
- Azure OpenAI (optional)

**Setup:**
```bash
# Install dependencies
python setup.py

# Start development servers
python start.py
```

**Features:**
- Hot reload enabled
- Mock data fallback
- Development logging
- Debug mode

### Production Environment

**Prerequisites:**
- Production server (Linux/Windows)
- Docker (recommended)
- Reverse proxy (Nginx)
- SSL certificates
- Production database

**Docker Deployment:**
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build individually
docker build -t uae-legal-graphrag-backend ./backend
docker build -t uae-legal-graphrag-frontend ./frontend
```

**Manual Deployment:**
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8012

# Frontend
cd frontend
npm install
npm run build
npm start
```

### Presentation Environment

**For 2-Hour Presentations:**

1. **Pre-setup (Before Presentation):**
   ```bash
   # Load mock data for guaranteed functionality
   echo "Legal data loading script not yet implemented"
   
   # Test the system
   python start.py --backend-only
   # In another terminal
   python start.py --frontend-only
   ```

2. **During Presentation:**
   ```bash
   # Start both services
   python start.py
   ```

3. **Fallback Strategy:**
   - If backend fails: Frontend automatically uses mock data
   - If Neo4j fails: System continues with mock data
   - If Azure OpenAI fails: System uses mock responses

## 📊 System Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 10GB
- **Network**: Internet connection (for AI services)

### Recommended Requirements
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Storage**: 50GB SSD
- **Network**: High-speed internet

### Production Requirements
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Storage**: 100GB+ SSD
- **Network**: Load balancer, CDN

## 🔒 Security Configuration

### Environment Variables
```env
# Production Security
APP_ENV=production
LOG_LEVEL=WARNING
CORS_ORIGINS=https://yourdomain.com

# Database Security
NEO4J_URI=bolt://your-neo4j-server:7687
NEO4J_USER=your_username
NEO4J_PASSWORD=your_secure_password

# AI Services
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your_secure_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
```

### SSL/TLS Configuration
```nginx
# Nginx configuration example
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://localhost:8012;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 Performance Optimization

### Backend Optimization
```python
# Production settings in backend/app/main.py
app = FastAPI(
    title="UAE Legal GraphRAG API",
    version="1.0.0",
    docs_url="/docs" if APP_ENV == "development" else None,
    redoc_url="/redoc" if APP_ENV == "development" else None
)

# Database connection pooling
NEO4J_POOL_SIZE = 20
NEO4J_MAX_OVERFLOW = 30
```

### Frontend Optimization
```javascript
// next.config.js
module.exports = {
  compress: true,
  poweredByHeader: false,
  generateEtags: false,
  experimental: {
    optimizeCss: true,
  },
}
```

## 🔍 Monitoring & Health Checks

### Health Check Endpoints
- **Backend**: `GET /health`
- **Frontend**: `GET /api/health`
- **Database**: `GET /health` (includes Neo4j status)
- **AI Services**: `GET /health` (includes Azure OpenAI status)

### Monitoring Setup
```bash
# Health check script
curl -f http://localhost:8012/health || exit 1
curl -f http://localhost:3000/api/health || exit 1
```

### Logging Configuration
```python
# Production logging
import logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

## 🚨 Troubleshooting

### Common Issues

1. **Backend Won't Start**
   ```bash
   # Check logs
   tail -f logs/app.log
   
   # Check dependencies
   pip list | grep -E "(fastapi|uvicorn|neo4j)"
   
   # Check environment
   python -c "import os; print(os.getenv('NEO4J_URI'))"
   ```

2. **Frontend Shows Mock Data**
   ```bash
   # Check backend health
   curl http://localhost:8012/health
   
   # Check network connectivity
   telnet localhost 8012
   ```

3. **Database Connection Issues**
   ```bash
   # Test Neo4j connection
   python -c "
   from backend.app.adapters.neo4j_conn import Neo4jConnection
   conn = Neo4jConnection()
   print(conn.test_connection())
   "
   ```

### Emergency Procedures

1. **Complete System Failure**
   ```bash
   # Restart all services
   pkill -f "uvicorn\|npm\|node"
   python start.py
   ```

2. **Database Failure**
   ```bash
   # Switch to mock data
   python start.py --frontend-only
   ```

3. **AI Service Failure**
   - System automatically falls back to mock responses
   - No manual intervention required

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] Database connection tested
- [ ] AI services accessible
- [ ] SSL certificates installed
- [ ] Firewall rules configured
- [ ] Monitoring setup complete

### Deployment
- [ ] Code deployed to production
- [ ] Dependencies installed
- [ ] Services started
- [ ] Health checks passing
- [ ] Load balancer configured
- [ ] SSL certificates working

### Post-Deployment
- [ ] Performance monitoring active
- [ ] Error logging configured
- [ ] Backup procedures tested
- [ ] Documentation updated
- [ ] Team notified

## 🔄 Update Procedures

### Rolling Updates
```bash
# 1. Deploy new backend
docker-compose up -d --no-deps backend

# 2. Health check
curl -f http://localhost:8012/health

# 3. Deploy new frontend
docker-compose up -d --no-deps frontend

# 4. Final health check
curl -f http://localhost:3000/api/health
```

### Zero-Downtime Deployment
```bash
# Blue-green deployment
# 1. Deploy to staging
# 2. Run tests
# 3. Switch traffic
# 4. Monitor health
# 5. Rollback if needed
```

## 📞 Support & Maintenance

### Regular Maintenance
- **Daily**: Health check monitoring
- **Weekly**: Log analysis and cleanup
- **Monthly**: Security updates and patches
- **Quarterly**: Performance review and optimization

### Support Contacts
- **Technical Issues**: Development team
- **Infrastructure**: DevOps team
- **Security**: Security team
- **Business**: Product team

---

This deployment guide ensures reliable, secure, and scalable deployment of the UAE Legal GraphRAG system across all environments.
