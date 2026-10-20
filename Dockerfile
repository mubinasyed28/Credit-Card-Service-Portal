# ==============================================================================
# Credit Card Service Portal (CCSP) - Multi-Stage Production Dockerfile
# Student: Mubina (Roll No: 23102A0039) | Subject: DevOps Lab | Dr. Snehal Andhare
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build & Quality Gate Environment (Eclipse Temurin JDK 17 & Maven)
# ------------------------------------------------------------------------------
FROM eclipse-temurin:17-jdk-alpine AS builder

LABEL maintainer="Mubina <23102A0039@student.devops.edu>"
LABEL project="Credit Card Service Portal"
LABEL task="Task 11: Docker Image and Container Lifecycle"

# Set working directory inside build container
WORKDIR /build

# Install curl for health probes and build utilities
RUN apk add --no-cache curl bash

# Step 1: Copy Maven wrapper / POM file to cache dependencies
COPY app/pom.xml .

# Download dependencies offline to optimize Docker build layer caching
# RUN ./mvnw dependency:go-offline -B (or standard mvn command)

# Step 2: Copy application source code
COPY app/src ./src

# Step 3: Compile, execute automated test quality gate, and assemble executable JAR
RUN ./../mvnw clean package -DskipTests=false 2>/dev/null || \
    (apk add --no-cache maven && mvn clean package -DskipTests=false)

# Verify assembled artifact exists
RUN ls -la target/credit-card-app-1.0.0.jar

# ------------------------------------------------------------------------------
# Stage 2: Minimal Hardened Runtime Environment (Eclipse Temurin JRE 17 Alpine)
# ------------------------------------------------------------------------------
FROM eclipse-temurin:17-jre-alpine AS runtime

WORKDIR /app

# Security Hardening: Create non-root dedicated service user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Install curl/wget for container health checks
RUN apk add --no-cache wget curl bash

# Copy executable fat JAR from builder stage (Multi-Stage Layer Optimization)
COPY --from=builder /build/target/credit-card-app-1.0.0.jar app.jar

# Enforce non-root ownership on application binary
RUN chown -R appuser:appgroup /app

# Switch to unprivileged execution user
USER appuser

# Container Port Exposure
EXPOSE 8080

# Environment Configuration Directives
ENV SPRING_PROFILES_ACTIVE=production \
    SERVER_PORT=8080 \
    JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -XX:+ExitOnOutOfMemoryError -Djava.security.egd=file:/dev/./urandom"

# Built-in Docker Container Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=25s --retries=3 \
    CMD wget -qO- http://localhost:8080/actuator/health | grep '"status":"UP"' || exit 1

# Container Launch Entrypoint
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
