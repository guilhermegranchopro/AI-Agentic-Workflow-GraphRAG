# **🚀 UAE Legal GraphRAG Deployment Guide - A2A Protocol Focus**

## **📋 Overview**

This guide provides step-by-step instructions for deploying the UAE Legal GraphRAG system with **A2A Protocol compliance**. The system is designed to be deployed as a production-ready A2A Protocol agent that can interoperate with other agents.

## **🔧 Prerequisites**

### **System Requirements**
- **Python**: 3.11+ with pip
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **Storage**: 10GB+ available disk space
- **Network**: Outbound access to Azure OpenAI and Neo4j

### **Required Services**
- **Azure OpenAI**: GPT-4o deployment with API access
- **Neo4j Database**: Neo4j 5.15+ instance
- **Environment Variables**: Proper configuration setup

## **📦 Installation Steps**

### **1. Clone Repository**
```bash
git clone <repository-url>
cd internship_GraphRAG
```

### **2. Setup Python Environment**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### **3. Environment Configuration**
Create a `.env` file in the `backend` directory:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password_here

# Application Configuration
APP_ENV=production
PORT=8000
```

## **🚀 Deployment Options**

### **Option 1: Local Development Deployment**

#### **Start Backend Server**
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### **Start Frontend (Optional)**
```bash
cd frontend
npm install
npm run dev
```

#### **Verify A2A Protocol**
```bash
# Test agent discovery
curl http://localhost:8000/.well-known/agent.json

# Test A2A health
curl http://localhost:8000/a2a/health

# Run A2A Protocol tests
python test_a2a_protocol.py
```

### **Option 2: Production Deployment**

#### **Using Docker Compose**
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
```

#### **Manual Production Deployment**
```bash
# Install production dependencies
pip install -r requirements.txt

# Start production server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## **🔍 A2A Protocol Verification**

### **1. Agent Discovery Test**
```bash
# Test public agent card
curl http://your-domain/.well-known/agent.json

# Expected response: JSON with protocolVersion, skills, transports
```

### **2. Core Endpoint Tests**
```bash
# Test message:send
curl -X POST http://your-domain/a2a/v1/message:send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{"message": {"role": "user", "parts": [{"kind": "text", "text": "Test"}], "metadata": {"skill_id": "ai_assistant"}}}'

# Test message:stream
curl -X POST http://your-domain/a2a/v1/message:stream \
  -H "Content-Type: application/json" \
  -d '{"taskId": "test-task"}'

# Test tasks:get
curl http://your-domain/a2a/v1/tasks/test-task
```

### **3. Compliance Testing**
```bash
# Run comprehensive A2A Protocol tests
cd backend
python test_a2a_protocol.py
```

## **🔒 Security Configuration**

### **Authentication Setup**
1. **Generate API Keys**: Create secure API keys for service-to-service communication
2. **Bearer Tokens**: Implement JWT token generation and validation
3. **Rate Limiting**: Configure appropriate rate limits for your use case
4. **CORS Settings**: Configure allowed origins for your deployment

### **Environment Security**
1. **Secure Environment Variables**: Use secure methods to store sensitive data
2. **Network Security**: Configure firewalls and network access controls
3. **SSL/TLS**: Enable HTTPS for production deployments
4. **Monitoring**: Set up security monitoring and alerting

## **📊 Monitoring & Health Checks**

### **Health Endpoints**
- **`/health`**: Overall system health
- **`/a2a/health`**: A2A Protocol health
- **`/.well-known/health`**: Well-known endpoints health

### **Monitoring Setup**
1. **Logging**: Configure structured logging for production
2. **Metrics**: Set up performance monitoring
3. **Alerting**: Configure alerts for critical issues
4. **Dashboard**: Set up monitoring dashboard

## **🔄 Update & Maintenance**

### **Regular Updates**
1. **Dependencies**: Keep Python packages updated
2. **Security Patches**: Apply security updates promptly
3. **A2A Protocol**: Monitor for protocol specification updates
4. **Documentation**: Keep deployment guides current

### **Backup & Recovery**
1. **Database Backups**: Regular Neo4j database backups
2. **Configuration Backups**: Backup environment configurations
3. **Disaster Recovery**: Plan for service restoration
4. **Testing**: Regular backup restoration testing

## **🚨 Troubleshooting**

### **Common Issues**

#### **Server Won't Start**
```bash
# Check port availability
netstat -an | grep :8000

# Check environment variables
python -c "from app.schemas.config import settings; print(settings.port)"
```

#### **A2A Protocol Endpoints Not Working**
```bash
# Check route registration
python -c "from app.main import app; print([r.path for r in app.routes if 'a2a' in str(r.path)])"

# Check well-known routes
python -c "from app.main import app; print([r.path for r in app.routes if 'well-known' in str(r.path)])"
```

#### **Database Connection Issues**
```bash
# Test Neo4j connection
python -c "from app.adapters.neo4j_conn import Neo4jConnection; neo4j = Neo4jConnection(); print('Connection successful')"
```

### **Log Analysis**
```bash
# View application logs
tail -f logs/app.log

# View A2A Protocol logs
grep "A2A" logs/app.log
```

## **📚 Additional Resources**

- **[A2A Protocol Specification](https://a2a-protocol.org/dev/specification/)**
- **[FastAPI Documentation](https://fastapi.tiangolo.com/)**
- **[Neo4j Documentation](https://neo4j.com/docs/)**
- **[Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)**

## **🎯 Deployment Checklist**

- [ ] Environment variables configured
- [ ] Dependencies installed
- [ ] Database connections tested
- [ ] A2A Protocol endpoints verified
- [ ] Security configuration applied
- [ ] Monitoring setup completed
- [ ] Backup procedures configured
- [ ] Documentation updated

## **🚀 Next Steps**

After successful deployment:

1. **Test A2A Protocol compliance** using the test suite
2. **Register your agent** with A2A Protocol directories
3. **Connect with other agents** for interoperability testing
4. **Monitor performance** and optimize as needed
5. **Plan scaling** for increased usage

Your UAE Legal GraphRAG system is now a **fully compliant A2A Protocol agent** ready for production use and agent-to-agent communication!
