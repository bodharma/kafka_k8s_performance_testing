# Kafka Kubernetes Performance Testing

A containerized Apache Kafka performance testing framework designed for load testing and benchmarking Kafka clusters in both Docker and Kubernetes environments. This project provides configurable producer and consumer applications with controllable message throughput for simulating real-world messaging scenarios.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Features](#features)
- [Use Cases](#use-cases)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development Setup](#local-development-setup)
  - [Running with Docker Compose](#running-with-docker-compose)
  - [Deploying to Kubernetes](#deploying-to-kubernetes)
- [Configuration](#configuration)
- [Performance Testing](#performance-testing)
- [Repository Status](#repository-status)

---

## Overview

This project implements a complete Kafka producer-consumer testing framework with configurable message rates. It's designed to simulate message traffic and measure Kafka cluster performance under various load conditions. The default configuration sends 50 messages per second, with support for custom rates and message payloads.

The system is fully containerized and can be deployed locally via Docker Compose or scaled horizontally in Kubernetes environments for distributed performance testing.

---

## Architecture

### System Components

The architecture follows a microservices pattern with three primary components:

```
+-------------------+          +-------------------+          +-------------------+
|                   |          |                   |          |                   |
|   Producer App    | -------> |   Kafka Broker    | -------> |   Consumer App    |
|   (Python 3.7)    |  Pub/Sub |   + ZooKeeper     |  Consume |   (Python 3.7)    |
|                   |          |                   |          |                   |
+-------------------+          +-------------------+          +-------------------+
        |                              |                              |
        v                              v                              v
   Dockerized                    Dockerized                     Dockerized
   Configurable Rate             Confluent Platform             Logging & Metrics
```

### Component Details

**1. Producer Service**
- Generates and publishes JSON messages to Kafka topics at configurable rates
- Uses the Confluent Kafka Python client for reliable message delivery
- Implements rate-limiting via sleep-based throttling mechanism
- Supports custom message payloads via JSON configuration
- Environment-driven configuration for deployment flexibility

**2. Kafka Cluster**
- Based on Confluent Platform Docker images
- Single-broker configuration suitable for testing and development
- Integrated ZooKeeper for cluster coordination
- Configurable listeners for both inter-broker and external communication
- Replication factor of 1 (suitable for single-node testing)

**3. Consumer Service**
- Subscribes to Kafka topics and processes messages in real-time
- Implements consumer group protocol for distributed consumption
- Comprehensive logging using Loguru for message tracking and debugging
- Graceful shutdown handling for clean consumer closure
- Error handling for resilient message processing

### Communication Flow

1. **Message Production**: Producer reads JSON template, generates messages, and publishes to Kafka topic with controlled rate limiting
2. **Message Brokering**: Kafka broker receives, persists, and manages message distribution using topic partitions
3. **Message Consumption**: Consumer polls Kafka broker, retrieves messages, and logs detailed information about received data
4. **Monitoring**: Both producer and consumer provide timestamped logging for performance analysis

### Data Flow

```
data.json -> Producer -> Kafka Topic (test) -> Consumer -> Console Logs
                |              |                    |
           Rate Control   Persistence          Processing
          (5 msg/sec)    (disk-based)         (real-time)
```

---

## Tech Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Message Broker | Apache Kafka | Latest (Confluent) | Distributed streaming platform |
| Coordination | Apache ZooKeeper | Latest (Confluent) | Cluster coordination and configuration |
| Runtime | Python | 3.7 | Application runtime environment |
| Containerization | Docker | - | Application packaging and isolation |
| Orchestration | Docker Compose | 2.1 | Local multi-container deployment |
| Container Platform | Kubernetes | - | Production-scale container orchestration |

### Python Libraries

**Producer Dependencies:**
- `confluent-kafka`: High-performance Kafka client library
- `loguru`: Modern logging framework with structured output

**Consumer Dependencies:**
- `confluent-kafka`: Kafka consumer group implementation
- `loguru`: Consistent logging across services

### Infrastructure

- **Container Images**:
  - `confluentinc/cp-kafka:latest` - Enterprise Kafka distribution
  - `confluentinc/cp-zookeeper:latest` - ZooKeeper coordinator
  - `python:3.7` - Base image for custom applications

- **Deployment Tools**:
  - Docker Compose for local orchestration
  - Kubernetes manifests for cluster deployment
  - Environment variable configuration

---

## Project Structure

```
kafka_k8s_performance_testing/
|
|-- consumer/
|   |-- Dockerfile              # Consumer container build specification
|   |-- consumer.py             # Consumer application logic
|   |-- requirements.txt        # Consumer Python dependencies
|
|-- producer/
|   |-- Dockerfile              # Producer container build specification
|   |-- producer.py             # Producer application with rate control
|   |-- data.json               # Sample message template/payload
|   |-- requirements.txt        # Producer Python dependencies
|
|-- kafka/
|   |-- init.py                 # Shared Kafka client wrapper and utilities
|
|-- k8s/
|   |-- msg-simulator.yaml.tmpl # Kubernetes deployment template
|
|-- docker-compose.yml          # Local development orchestration
|-- .gitignore                  # Version control exclusions
|-- README.md                   # Project documentation (this file)
```

### Directory Breakdown

**`/consumer`** - Consumer microservice
- Subscribes to Kafka topics and processes incoming messages
- Implements consumer group protocol with configurable group ID
- Provides detailed logging of message metadata (topic, key, value)

**`/producer`** - Producer microservice
- Publishes messages to Kafka at controlled rates
- Includes message templating via JSON configuration
- Rate-limiting logic to simulate realistic load patterns

**`/kafka`** - Shared Kafka utilities
- `KafkaMessenger` class for producer initialization
- Message serialization and formatting utilities
- Reusable components across producer services

**`/k8s`** - Kubernetes deployment manifests
- Template for deploying to Kubernetes clusters
- Separate deployments for producer and consumer
- Configurable Kafka endpoint via environment variables

---

## Features

### Core Capabilities

- **Configurable Message Rate**: Control message throughput via environment variables (default: 5 messages/second)
- **Custom Message Payloads**: Define JSON message templates for realistic data simulation
- **Containerized Deployment**: Fully Dockerized applications for consistent environments
- **Multi-Platform Support**: Run on Docker Compose (local) or Kubernetes (production)
- **Environment-Based Configuration**: No code changes required for different deployments
- **Comprehensive Logging**: Structured logging with timestamps for performance analysis
- **Consumer Groups**: Support for distributed consumption and load balancing
- **Graceful Shutdown**: Proper cleanup and resource management

### Configuration Options

Both producer and consumer services support environment variable configuration:

**Producer Environment Variables:**
- `KAFKA_TOPIC` - Target topic name (default: "test")
- `KAFKA_URL` - Kafka broker endpoint (default: "kafka:9092")
- `MESSAGES_PER_SECOND` - Message production rate (default: 5)

**Consumer Environment Variables:**
- `KAFKA_TOPIC` - Topic to subscribe to (default: "test")
- `KAFKA_URL` - Kafka broker endpoint (default: "kafka:9092")

### Performance Characteristics

- **Default Throughput**: 5 messages per second (configurable up to hundreds/thousands per second)
- **Message Format**: JSON-based with customizable schema
- **Latency**: Sub-second message delivery in local environments
- **Reliability**: At-least-once delivery semantics
- **Scalability**: Horizontal scaling via Kubernetes replicas

---

## Use Cases

### 1. Kafka Performance Benchmarking

**Scenario**: Measure Kafka cluster throughput and latency under various load conditions

**Implementation**:
- Deploy multiple producer replicas with different message rates
- Monitor broker resource utilization (CPU, memory, disk I/O)
- Measure end-to-end message latency from production to consumption
- Test different partition counts and replication factors

**Value**: Establish baseline performance metrics for capacity planning

### 2. Load Testing and Stress Testing

**Scenario**: Validate Kafka cluster behavior under extreme load

**Implementation**:
- Scale producer instances to generate high message volumes
- Introduce message bursts to test buffer handling
- Simulate consumer lag scenarios by slowing consumption
- Test broker failover and recovery mechanisms

**Value**: Identify breaking points and validate resilience strategies

### 3. Kafka Cluster Configuration Tuning

**Scenario**: Optimize Kafka broker and client configurations

**Implementation**:
- Test different batch sizes, compression codecs, and acknowledgment modes
- Compare performance across various partition and replica configurations
- Measure impact of JVM tuning and OS-level optimizations
- Validate producer and consumer configuration best practices

**Value**: Data-driven optimization for production deployments

### 4. Educational and Training Purposes

**Scenario**: Learn Kafka architecture and operational patterns

**Implementation**:
- Hands-on environment for understanding producer-consumer patterns
- Explore message ordering, partitioning, and offset management
- Practice monitoring and troubleshooting techniques
- Experiment with different deployment topologies

**Value**: Safe learning environment without production risk

### 5. Continuous Integration Testing

**Scenario**: Automated Kafka integration tests in CI/CD pipelines

**Implementation**:
- Spin up Kafka environment in CI pipeline
- Run producer/consumer tests to validate application changes
- Verify message serialization and deserialization logic
- Test error handling and retry mechanisms

**Value**: Early detection of Kafka integration issues

### 6. Message Schema Evolution Testing

**Scenario**: Validate backward/forward compatibility of message formats

**Implementation**:
- Modify `data.json` to test different schema versions
- Validate consumer handling of schema changes
- Test Schema Registry integration patterns
- Verify error handling for incompatible schemas

**Value**: Safe schema evolution without breaking consumers

### 7. Kubernetes Deployment Validation

**Scenario**: Test Kafka deployment patterns in Kubernetes

**Implementation**:
- Deploy using provided Kubernetes manifests
- Test pod scheduling, resource limits, and auto-scaling
- Validate service discovery and networking
- Test persistent volume configuration for Kafka storage

**Value**: Proven deployment patterns for production Kubernetes clusters

### 8. Disaster Recovery Testing

**Scenario**: Validate backup, recovery, and failover procedures

**Implementation**:
- Simulate broker failures during active message production
- Test consumer rebalancing and offset management
- Validate data persistence and retention policies
- Measure recovery time objectives (RTO) and recovery point objectives (RPO)

**Value**: Confidence in disaster recovery capabilities

### 9. Multi-Environment Development

**Scenario**: Consistent Kafka environment across dev, staging, and production

**Implementation**:
- Use Docker Compose for local development
- Deploy to Kubernetes staging environment
- Maintain environment parity through containerization
- Test configuration changes before production deployment

**Value**: Reduced environment-related bugs and deployment issues

### 10. Message Rate Simulation

**Scenario**: Simulate real-world message traffic patterns

**Implementation**:
- Configure message rates to match production workloads
- Test diurnal patterns (variable load throughout the day)
- Validate queue depth and consumer lag thresholds
- Optimize consumer scaling based on message rates

**Value**: Realistic performance validation before production deployment

---

## Getting Started

### Prerequisites

**Required Software:**
- Docker Engine 19.03 or later
- Docker Compose 1.27 or later (for local development)
- Kubernetes cluster with kubectl configured (for K8s deployment)
- Python 3.7+ with pipenv (for local development without Docker)

**System Requirements:**
- Minimum 4GB RAM (8GB recommended for performance testing)
- 10GB available disk space for Docker images and Kafka data
- Network access for pulling Docker images

### Local Development Setup

**1. Clone the Repository**

```bash
git clone <repository-url>
cd kafka_k8s_performance_testing
```

**2. Set Up Python Virtual Environment (Optional - for development)**

```bash
# Install pipenv if not already installed
pip install pipenv

# Create and activate virtual environment
pipenv shell

# Install dependencies
cd producer && pipenv install -r requirements.txt
cd ../consumer && pipenv install -r requirements.txt
```

### Running with Docker Compose

**Start Complete Stack (Kafka + ZooKeeper + Producer + Consumer):**

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

**Run Producer Only:**

```bash
# Build the producer image
docker-compose build producer-local

# Start producer service
docker-compose up producer-local
```

**Run Consumer Only:**

```bash
# Build the consumer image
docker-compose build consumer-local

# Start consumer service
docker-compose up consumer-local
```

**Separate Terminal Approach (Recommended for Monitoring):**

Terminal 1 - Start Kafka Infrastructure:
```bash
docker-compose up kafka zookeeper
```

Terminal 2 - Start Producer:
```bash
docker-compose up producer-local
```

Terminal 3 - Start Consumer:
```bash
docker-compose up consumer-local
```

**Stop All Services:**

```bash
# Stop services (preserves data)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers, and clean up volumes
docker-compose down -v
```

### Deploying to Kubernetes

**1. Configure Kafka Endpoint**

Edit `k8s/msg-simulator.yaml.tmpl` and replace `<KAFKA_IP>` with your Kafka broker address:

```yaml
env:
  - name: KAFKA_URL
    value: "your-kafka-broker.namespace.svc.cluster.local:9092"
```

**2. Build and Push Container Images**

```bash
# Build producer image
docker build -f producer/Dockerfile -t your-registry/msg-simulator:latest .

# Build consumer image
docker build -f consumer/Dockerfile -t your-registry/msg-consumer:latest .

# Push to container registry
docker push your-registry/msg-simulator:latest
docker push your-registry/msg-consumer:latest
```

**3. Update Image References**

Modify `k8s/msg-simulator.yaml.tmpl` to reference your container images:

```yaml
spec:
  containers:
  - name: msg-simulator
    image: "your-registry/msg-simulator:latest"
```

**4. Deploy to Kubernetes**

```bash
# Apply the manifest
kubectl apply -f k8s/msg-simulator.yaml.tmpl

# Verify deployment
kubectl get pods -n msg-simulator

# Check logs
kubectl logs -n msg-simulator deployment/msg-simulator -f
kubectl logs -n msg-simulator deployment/msg-consumer -f
```

**5. Scale Deployments**

```bash
# Scale producers for higher throughput
kubectl scale deployment/msg-simulator --replicas=5 -n msg-simulator

# Scale consumers for parallel processing
kubectl scale deployment/msg-consumer --replicas=3 -n msg-simulator
```

---

## Configuration

### Customizing Message Payload

Edit `producer/data.json` to define your message structure:

```json
{
  "location": {
    "address1": "123 Main St.",
    "city": "Iowa",
    "state": "TEX",
    "country": "USA"
  }
}
```

### Adjusting Message Rate

Modify the `MESSAGES_PER_SECOND` environment variable in `docker-compose.yml`:

```yaml
environment:
  MESSAGES_PER_SECOND: 100  # Send 100 messages per second
```

Or override at runtime:

```bash
docker-compose run -e MESSAGES_PER_SECOND=50 producer-local
```

### Changing Kafka Topic

Set the `KAFKA_TOPIC` environment variable:

```yaml
environment:
  KAFKA_TOPIC: "performance-test"
```

### External Kafka Cluster

To connect to an external Kafka cluster:

```yaml
environment:
  KAFKA_URL: "external-kafka.example.com:9092"
```

---

## Performance Testing

### Basic Performance Test

```bash
# Start infrastructure
docker-compose up -d kafka zookeeper

# Wait for Kafka to be ready (30-60 seconds)
sleep 60

# Run producer at 100 msg/sec
docker-compose run -e MESSAGES_PER_SECOND=100 producer-local

# Monitor consumer in separate terminal
docker-compose up consumer-local
```

### Measuring Latency

Check consumer logs for message timestamps and compare with producer timestamps:

```bash
docker-compose logs -f consumer-local | grep "Received message"
```

### Monitoring Kafka

Connect to Kafka container for monitoring:

```bash
# List topics
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Describe topic
docker-compose exec kafka kafka-topics --describe --topic test --bootstrap-server localhost:9092

# Check consumer groups
docker-compose exec kafka kafka-consumer-groups --list --bootstrap-server localhost:9092

# Consumer group lag
docker-compose exec kafka kafka-consumer-groups --describe --group jmsgroup --bootstrap-server localhost:9092
```

---

## Repository Status

**Status**: Archived

This repository represents a functional Kafka performance testing framework suitable for development, testing, and educational purposes. The project includes:

- Working producer and consumer applications
- Docker Compose configuration for local testing
- Kubernetes deployment templates (requires environment-specific configuration)
- Sample message payload structure
- Configurable message rate control

**Known Limitations:**
- Kubernetes deployment requires manual configuration of Kafka endpoints
- Single-broker Kafka configuration (not production-ready for high availability)
- Python 3.7 base image (newer versions available)
- Consumer group ID is hardcoded ("jmsgroup")

**Future Enhancement Opportunities:**
- Implement random data generation (see TODO in `kafka/init.py`)
- Add metrics collection (Prometheus integration)
- Support for Avro/Protobuf schemas with Schema Registry
- Kubernetes StatefulSet for Kafka deployment
- Helm chart packaging
- Performance test result aggregation and reporting
- Multi-broker Kafka cluster support
- TLS/SASL authentication support

---

## License

This project is provided as-is for educational and testing purposes.

---

## Contributing

This repository is archived and not actively maintained. Feel free to fork and adapt for your own use cases.

---

**Last Updated**: January 2026
