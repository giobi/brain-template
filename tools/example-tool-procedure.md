# Example Tool Procedure: Docker Container Debugging

> Reusable procedures organized by tool/service, not by date.

## When to Use This

Use this procedure when:
- Container fails to start or crashes immediately
- Application inside container behaves unexpectedly
- Need to inspect container state or logs
- Performance issues with containerized apps

## Prerequisites

- Docker installed and running
- Access to container or image
- Basic understanding of Docker concepts

## Procedure

### 1. Check Container Status

```bash
# List all containers (including stopped)
docker ps -a

# Get detailed info about specific container
docker inspect <container-id>

# Check container resource usage
docker stats <container-id>
```

### 2. View Logs

```bash
# View all logs
docker logs <container-id>

# Follow logs in real-time
docker logs -f <container-id>

# Last 100 lines
docker logs --tail 100 <container-id>

# Logs with timestamps
docker logs -t <container-id>
```

### 3. Access Container Shell

```bash
# Start interactive shell (if container is running)
docker exec -it <container-id> /bin/bash
# or if bash not available:
docker exec -it <container-id> /bin/sh

# For stopped containers, start with entrypoint override
docker run -it --entrypoint /bin/bash <image-name>
```

### 4. Inspect Filesystem

```bash
# Copy file from container to host
docker cp <container-id>:/path/to/file ./local-path

# Copy file from host to container
docker cp ./local-file <container-id>:/path/in/container

# Check disk usage inside container
docker exec <container-id> df -h
```

### 5. Debug Network Issues

```bash
# Inspect network configuration
docker network inspect <network-name>

# Check which networks container is connected to
docker inspect <container-id> | grep -A 10 Networks

# Test connectivity from inside container
docker exec <container-id> ping <host>
docker exec <container-id> curl <url>

# Check exposed ports
docker port <container-id>
```

### 6. Check Environment Variables

```bash
# View all environment variables
docker exec <container-id> env

# View specific variable
docker exec <container-id> printenv <VAR_NAME>
```

### 7. Resource Constraints

```bash
# Check if container is hitting memory limits
docker stats --no-stream <container-id>

# View container config including resource limits
docker inspect <container-id> | grep -A 20 Memory
```

## Common Issues & Solutions

### Issue: Container Exits Immediately

**Diagnosis**:
```bash
docker logs <container-id>
docker inspect <container-id> --format='{{.State.ExitCode}}'
```

**Common causes**:
- Missing required environment variables
- Entrypoint script has errors
- Configuration file issues

**Solution**: Check logs, verify environment, test entrypoint locally

---

### Issue: Cannot Connect to Container

**Diagnosis**:
```bash
docker port <container-id>
docker network inspect bridge
```

**Common causes**:
- Ports not exposed in Dockerfile
- Port mapping incorrect in `docker run`
- Firewall blocking access

**Solution**: Verify port mappings, check network configuration

---

### Issue: Container Running Slow

**Diagnosis**:
```bash
docker stats <container-id>
docker exec <container-id> top
```

**Common causes**:
- Resource limits too restrictive
- Memory leaks in application
- I/O bottlenecks

**Solution**: Increase resource limits, profile application, check disk I/O

## Best Practices

1. **Always check logs first**: `docker logs` reveals 80% of issues
2. **Use health checks**: Add HEALTHCHECK in Dockerfile for better monitoring
3. **Tag images properly**: Use semantic versioning for reproducibility
4. **Minimize layers**: Combine RUN commands to reduce image size
5. **Clean up**: Remove unused containers and images regularly

## Related Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- Related brain notes: `brain/projects/*/index.md` (for project-specific Docker config)

## Example Debug Session

```bash
# Scenario: Web app container won't start

# 1. Check what happened
docker ps -a
# Container shows "Exited (1) 2 minutes ago"

# 2. View logs
docker logs web-app
# Error: "Database connection refused"

# 3. Inspect network
docker network inspect app-network
# Database container is on different network!

# 4. Fix: Reconnect to correct network
docker network connect app-network web-app
docker start web-app

# 5. Verify
docker logs -f web-app
# Success: "Server listening on port 3000"
```

---

**Last Updated**: 2025-10-17
**Tested With**: Docker 24.0.x
