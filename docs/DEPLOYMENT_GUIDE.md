# UAE Legal GraphRAG - Deployment Guide

## Overview

This guide provides instructions for deploying the UAE Legal GraphRAG system in various environments, from local development to production deployment.

## Prerequisites

### Software Requirements
- **Python**: 3.11+ with pip
- **Node.js**: 18+ with npm
- **Docker**: 20.10+ (for containerized deployment)
- **Git**: 2.30+

## Local Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd internship_GraphRAG
```

### 2. Neo4j Database Setup

**This is a critical step that must be completed before running the application.**

#### Install Neo4j Desktop
- Download Neo4j Desktop from [neo4j.com/download](https://neo4j.com/download/)
- Install and launch Neo4j Desktop

#### Create Neo4j Instance
- Click "New" → "Create a Local Graph"
- Choose Neo4j 5.15+ version
- Set a secure password (remember this for your .env file)
- Start the instance

#### Import Knowledge Graph Data
- In Neo4j Desktop, click on your instance
- Go to "Manage" → "Import"
- Upload the `neo4j_knowledge_graph.dump` file from the repository root
- This populates the database with mock UAE legal system data (83+ legal entities, 103+ relationships)
- Wait for the import to complete before proceeding

**Note**: The application will not function properly without this knowledge graph data.

### 3. Python Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 4. Node.js Environment
```bash
cd frontend
npm install
```

### 5. Environment Configuration
```bash
cp .env.template .env
# Edit .env with your configuration, especially:
# - NEO4J_PASSWORD: The password you set for your Neo4j instance
# - AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
# - AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint
```

### 6. Start Services
```bash
# Backend (Terminal 1)
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend (Terminal 2)
cd frontend
npm run dev
```

## Production Deployment

### Docker Deployment

#### 1. Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=production
      - NEO4J_URI=bolt://neo4j:7687
    depends_on:
      - neo4j
      - redis
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
    restart: unless-stopped

  neo4j:
    image: neo4j:5.15
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/secure-password
    volumes:
      - neo4j_data:/data
      - ./neo4j_knowledge_graph.dump:/var/lib/neo4j/import/neo4j_knowledge_graph.dump:ro
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  neo4j_data:
  redis_data:
```

#### 2. Deploy with Docker
```bash
# Build and start services
docker-compose up -d --build

# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
```

**Important**: After the Neo4j container starts, you need to import the knowledge graph data:
```bash
# Connect to Neo4j container
docker exec -it internship_graphrag_neo4j_1 bash

# Import the knowledge graph data
cypher-shell -u neo4j -p secure-password
# Follow Neo4j import instructions for the neo4j_knowledge_graph.dump file
# This is required for the application to function properly
```

### Traditional Server Deployment

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3.11-pip
sudo apt install -y nodejs npm nginx redis-server

# Configure firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8000/tcp  # Application
sudo ufw enable
```

#### 2. Neo4j Installation
```bash
# Add Neo4j repository
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 4.4' | sudo tee /etc/apt/sources.list.d/neo4j.list

# Install Neo4j
sudo apt update
sudo apt install neo4j

# Configure Neo4j
sudo nano /etc/neo4j/neo4j.conf
# Key configurations:
# dbms.connector.bolt.enabled=true
# dbms.connector.bolt.listen_address=:7687
# dbms.memory.heap.initial_size=2G
# dbms.memory.heap.max_size=4G

# Start Neo4j
sudo systemctl start neo4j
sudo systemctl enable neo4j

# Set password
cypher-shell -u neo4j -p neo4j
CALL dbms.security.changePassword('secure-password')
```

#### 3. Import Knowledge Graph Data
```bash
# Copy the knowledge graph dump file to the server
scp neo4j_knowledge_graph.dump user@server:/tmp/

# Import the data into Neo4j
sudo systemctl stop neo4j
sudo cp /tmp/neo4j_knowledge_graph.dump /var/lib/neo4j/import/
sudo chown neo4j:neo4j /var/lib/neo4j/import/neo4j_knowledge_graph.dump

# Start Neo4j and import data
sudo systemctl start neo4j

# Wait for Neo4j to start, then import data
cypher-shell -u neo4j -p secure-password
# Follow Neo4j import instructions for the dump file
# This populates the database with UAE legal system data
```

#### 3. Application Deployment
```bash
# Create application user
sudo useradd -m -s /bin/bash graphrag
sudo usermod -aG sudo graphrag

# Clone application
sudo -u graphrag git clone <repository-url> /home/graphrag/app
cd /home/graphrag/app

# Setup Python environment
sudo -u graphrag python3.11 -m venv .venv
sudo -u graphrag .venv/bin/pip install -r requirements.txt

# Configure environment
sudo -u graphrag cp .env.template .env
sudo -u graphrag nano .env
# Set production environment variables
```

#### 4. Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/graphrag-backend.service

[Unit]
Description=GraphRAG Backend
After=network.target

[Service]
Type=exec
User=graphrag
WorkingDirectory=/home/graphrag/app
Environment=PATH=/home/graphrag/app/.venv/bin
ExecStart=/home/graphrag/app/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable graphrag-backend
sudo systemctl start graphrag-backend
```

#### 5. Nginx Configuration
```bash
# Create Nginx site configuration
sudo nano /etc/nginx/sites-available/graphrag

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/graphrag /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Environment Configuration

### Production Environment Variables
```env
# Application Configuration
APP_ENV=production
PORT=8000
HOST=0.0.0.0

# Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=secure-production-password

# AI Services
AZURE_OPENAI_API_KEY=your-production-api-key
AZURE_OPENAI_ENDPOINT=https://your-production-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Security
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Performance
WORKERS=4
LOG_LEVEL=INFO
```

## Monitoring and Health Checks

### Health Endpoints
- `/health` - Basic health check
- `/a2a/health` - A2A Protocol health
- `/.well-known/health` - Well-known health

### Health Check Script
```bash
#!/bin/bash
HEALTH_URL="http://localhost:8000/health"
response=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $response -eq 200 ]; then
    echo "Application is healthy"
    exit 0
else
    echo "Application health check failed: HTTP $response"
    exit 1
fi
```

## Backup and Recovery

### Database Backup
```bash
#!/bin/bash
BACKUP_DIR="/backups/neo4j"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
sudo systemctl stop neo4j
sudo cp -r /var/lib/neo4j/data $BACKUP_DIR/neo4j_$DATE
sudo systemctl start neo4j

tar -czf $BACKUP_DIR/neo4j_$DATE.tar.gz -C $BACKUP_DIR neo4j_$DATE
rm -rf $BACKUP_DIR/neo4j_$DATE

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Backup Schedule
```bash
# Add to crontab
sudo crontab -e

# Daily backup at 2 AM
0 2 * * * /path/to/backup-neo4j.sh
```

## Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check logs
sudo journalctl -u graphrag-backend -f

# Check configuration
python -c "from app.schemas.config import Settings; Settings()"

# Check dependencies
pip list | grep -E "(fastapi|uvicorn|neo4j)"
```

#### Database Connection Issues
```bash
# Check Neo4j status
sudo systemctl status neo4j

# Check connectivity
telnet localhost 7687

# Check logs
sudo tail -f /var/log/neo4j/neo4j.log
```

### Recovery Procedures
```bash
# Restart all services
sudo systemctl restart neo4j
sudo systemctl restart graphrag-backend
sudo systemctl restart nginx

# Check status
sudo systemctl status neo4j graphrag-backend nginx
```

## Security Considerations

### SSL/TLS Setup
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Firewall Configuration
```bash
# Configure UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw enable
```

## Scaling

### Load Balancer Configuration
```nginx
upstream backend_servers {
    server 192.168.1.10:8000;
    server 192.168.1.11:8000;
    server 192.168.1.12:8000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Performance Optimization
```bash
# Neo4j optimization
sudo nano /etc/neo4j/neo4j.conf

# Performance settings
dbms.memory.heap.initial_size=4G
dbms.memory.heap.max_size=8G
dbms.memory.pagecache.size=4G
dbms.connector.bolt.thread_pool_size=50

# Restart Neo4j
sudo systemctl restart neo4j
```

## Maintenance

### Regular Updates
```bash
# System updates
sudo apt update && sudo apt upgrade -y

# Application updates
git pull origin main
sudo systemctl restart graphrag-backend
sudo systemctl restart nginx
```

### Log Management
```bash
# Log rotation
sudo logrotate -f /etc/logrotate.d/graphrag

# Log monitoring
tail -f logs/app.log | grep ERROR
```

## Conclusion

This deployment guide provides the essential steps for deploying the UAE Legal GraphRAG system. Follow the appropriate sections based on your deployment requirements and ensure all security and performance considerations are addressed.

For additional support or questions about deployment, consult the system documentation or contact the development team.
