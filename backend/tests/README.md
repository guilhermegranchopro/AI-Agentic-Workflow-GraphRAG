# UAE Legal GraphRAG Test Suite

## Overview

This directory contains the test suite for the UAE Legal GraphRAG system, with a focus on **A2A Protocol compliance testing**.

## Running Tests

### **A2A Protocol Tests**
```bash
# Run A2A Protocol compliance tests
python test_a2a_protocol.py

# Test specific components
python -m pytest tests/ -v
```

### **Test Configuration**
- **Base URL**: http://localhost:8000 (configurable)
- **API Token**: Set in test file or environment
- **Test Coverage**: Full A2A Protocol specification compliance

## Test Coverage

### **A2A Protocol Requirements**
1. ✅ **Agent Discovery** - `/.well-known/agent.json`
2. ✅ **Core Methods** - `message:send`, `message:stream`, `tasks:get`
3. ✅ **Transport** - HTTP+JSON support
4. ✅ **Security** - Authentication schemes
5. ✅ **Capabilities** - Streaming and long-running tasks

### **Test Categories**
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **A2A Compliance Tests**: Protocol specification validation
- **Performance Tests**: Load and stress testing

## Test Setup

### **Prerequisites**
1. Backend server running on port 8000
2. Environment variables configured
3. Database connections established
4. AI services accessible

### **Environment Variables**
```env
# Test configuration
TEST_BASE_URL=http://localhost:8000
TEST_API_TOKEN=your-test-token
TEST_TIMEOUT=30
```

## Test Results

### **Expected Output**
```
🚀 A2A Protocol Test Suite - Following Exact Guidelines
======================================================================
Testing against: http://localhost:8000

🔍 Testing Agent Discovery (A2A Protocol Requirement #1)...
   ✅ Agent Card at /.well-known/agent.json successful
   ✅ A2A Protocol version 0.3.0 compliant

🏥 Testing A2A Protocol Health...
   ✅ A2A Health Check successful

📨 Testing A2A Protocol message:send (Requirement #2)...
   ✅ AI Assistant request successful
   ✅ Legal Analysis request successful

🔍 Testing A2A Protocol Compliance (Requirement #5)...
   ✅ Agent Card: Public discovery at /.well-known/agent.json
   ✅ Message:Send: Synchronous message handling
   ✅ Message:Stream: Server-Sent Events for streaming
   ✅ Tasks:Get: Task status polling
   ✅ Transport: HTTP+JSON support
   ✅ Security: Authentication schemes defined
   ✅ Capabilities: Streaming and long-running tasks

📊 A2A Protocol Compliance Summary:
   ✅ Agent Card
   ✅ Message:Send
   ✅ Message:Stream
   ✅ Tasks:Get
   ✅ Transport
   ✅ Security
   ✅ Capabilities

   Compliance: 7/7 checks passed
   🎉 FULL A2A PROTOCOL COMPLIANCE ACHIEVED!
```

## Troubleshooting

### **Common Test Issues**
1. **Server Not Running**: Ensure backend is started on port 8000
2. **Authentication Failed**: Check API token configuration
3. **Database Connection**: Verify Neo4j connectivity
4. **AI Service Error**: Check Azure OpenAI configuration

### **Debug Mode**
```bash
# Run tests with verbose output
python test_a2a_protocol.py --verbose

# Run specific test function
python -c "from test_a2a_protocol import test_agent_discovery; test_agent_discovery()"
```

## Test Documentation

- **[A2A Protocol Specification](https://a2a-protocol.org/dev/specification/)**
- **[Test Best Practices](https://docs.pytest.org/)**
- **[FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)**

## Next Steps

After successful test execution:

1. **Verify Compliance**: All A2A Protocol requirements met
2. **Integration Testing**: Test with other A2A agents
3. **Performance Testing**: Load testing and optimization
4. **Production Deployment**: Deploy compliant system

Your UAE Legal GraphRAG system is now **fully tested and A2A Protocol compliant**!
