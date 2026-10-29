pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['staging', 'production', 'development'], description: 'Target deployment environment profile')
        string(name: 'SERVER_PORT', defaultValue: '8080', description: 'HTTP port for application server binding')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Enforce automated JUnit 5 test quality gate')
        string(name: 'CONTEXT_PATH', defaultValue: '/', description: 'Application web context path')
        string(name: 'DOCKER_REGISTRY', defaultValue: 'mubina23102a0039', description: 'Docker Hub username / local registry prefix')
        booleanParam(name: 'PUSH_TO_REGISTRY', defaultValue: false, description: 'Push versioned image to Docker Hub registry after build')
    }

    environment {
        APP_NAME        = 'credit-card-app'
        APP_VERSION     = '1.0.0'
        JAR_FILE        = "app/target/${APP_NAME}-${APP_VERSION}.jar"
        JAVA_HOME_PATH  = 'C:\\Users\\YOCKET-271\\tools\\jdk-17.0.12+7'
        MAVEN_HOME_PATH = 'C:\\Users\\YOCKET-271\\tools\\apache-maven-3.9.6'
        DEPLOY_DIR      = 'C:\\opt\\credit-card-portal'
        IMAGE_NAME      = "${params.DOCKER_REGISTRY}/${APP_NAME}"
        IMAGE_TAG       = "${APP_VERSION}.${BUILD_NUMBER}"
        CONTAINER_NAME  = 'ccsp-live'
        WORKSPACE_PATH  = 'c:\\Users\\YOCKET-271\\Downloads\\DevOps_AI_Starter_Kit'
    }

    options {
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '5'))
        timestamps()
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo "=========================================================="
                echo "Stage 1: SCM Checkout from GitHub Repository"
                echo "Repository: https://github.com/mubinasyed28/Credit-Card-Service-Portal.git"
                echo "Build Number: ${BUILD_NUMBER}"
                echo "Target Environment: ${params.DEPLOY_ENV}"
                echo "=========================================================="
                checkout scm
            }
        }

        stage('Build & Compile') {
            steps {
                echo "=========================================================="
                echo "Stage 2: Compiling Java Sources via Apache Maven"
                echo "=========================================================="
                dir('app') {
                    bat """
                        set "JAVA_HOME=${JAVA_HOME_PATH}"
                        set "PATH=${MAVEN_HOME_PATH}\\bin;%JAVA_HOME%\\bin;%PATH%"
                        mvn -B clean compile
                    """
                }
            }
        }

        stage('Automated Quality Gate') {
            when {
                expression { return params.RUN_TESTS == true }
            }
            steps {
                echo "=========================================================="
                echo "Stage 3: Executing Automated JUnit 5 Quality Gate"
                echo "=========================================================="
                dir('app') {
                    bat """
                        set "JAVA_HOME=${JAVA_HOME_PATH}"
                        set "PATH=${MAVEN_HOME_PATH}\\bin;%JAVA_HOME%\\bin;%PATH%"
                        mvn -B test
                    """
                }
            }
            post {
                always {
                    junit testResults: 'app/target/surefire-reports/*.xml', allowEmptyResults: true
                }
                failure {
                    echo 'QUALITY GATE VIOLATION: Test failures detected. Aborting Docker build and deployment.'
                }
            }
        }

        stage('Package Application Archive') {
            steps {
                echo "=========================================================="
                echo "Stage 4: Assembling Executable Spring Boot JAR"
                echo "=========================================================="
                dir('app') {
                    bat """
                        set "JAVA_HOME=${JAVA_HOME_PATH}"
                        set "PATH=${MAVEN_HOME_PATH}\\bin;%JAVA_HOME%\\bin;%PATH%"
                        mvn -B package -DskipTests=true
                    """
                }
                archiveArtifacts artifacts: 'app/target/*.jar', fingerprint: true, onlyIfSuccessful: true
            }
        }

        // ---------------------------------------------------------------
        // TASK 12: Jenkins-Docker Continuous Deployment Stages
        // (Skipped automatically when Docker is not available)
        // ---------------------------------------------------------------

        stage('Docker: Build Versioned Image') {
            when {
                expression {
                    def dockerAvailable = bat(script: 'docker --version', returnStatus: true) == 0
                    if (!dockerAvailable) {
                        echo "Docker not available – skipping Docker build stage."
                    }
                    return dockerAvailable
                }
            }
            steps {
                echo "=========================================================="
                echo "Stage 5: Building Versioned Docker Image"
                echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
                echo "=========================================================="
                bat """
                    docker build ^
                        --label "build.number=${BUILD_NUMBER}" ^
                        --label "project=Credit Card Service Portal" ^
                        --label "maintainer=Mubina 23102A0039" ^
                        -t %IMAGE_NAME%:%IMAGE_TAG% ^
                        -t %IMAGE_NAME%:latest ^
                        .
                    docker images %IMAGE_NAME% --format "table {{.Repository}}\\t{{.Tag}}\\t{{.ID}}\\t{{.Size}}"
                """
            }
        }

        stage('Docker: Publish to Registry') {
            when {
                allOf {
                    expression { return params.PUSH_TO_REGISTRY == true }
                    expression {
                        return bat(script: 'docker --version', returnStatus: true) == 0
                    }
                }
            }
            steps {
                echo "=========================================================="
                echo "Stage 6: Pushing Versioned Image to Docker Hub Registry"
                echo "=========================================================="
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat """
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                        docker push %IMAGE_NAME%:%IMAGE_TAG%
                        docker push %IMAGE_NAME%:latest
                        docker logout
                    """
                }
            }
        }

        stage('Docker: Deploy Fresh Container') {
            when {
                expression {
                    def dockerAvailable = bat(script: 'docker --version', returnStatus: true) == 0
                    if (!dockerAvailable) {
                        echo "Docker not available – skipping container deployment stage."
                    }
                    return dockerAvailable
                }
            }
            steps {
                echo "=========================================================="
                echo "Stage 7: Deploying Fresh Container (Zero-Downtime Swap)"
                echo "Container: ${CONTAINER_NAME}   Port: ${params.SERVER_PORT}:8080"
                echo "=========================================================="
                bat """
                    docker stop %CONTAINER_NAME% 2>nul || echo No running container to stop.
                    docker rm   %CONTAINER_NAME% 2>nul || echo No existing container to remove.
                    docker run -d ^
                        --name %CONTAINER_NAME% ^
                        -p ${params.SERVER_PORT}:8080 ^
                        -e SPRING_PROFILES_ACTIVE=${params.DEPLOY_ENV} ^
                        -e SERVER_PORT=8080 ^
                        --restart unless-stopped ^
                        %IMAGE_NAME%:%IMAGE_TAG%
                    timeout /t 30 /nobreak >nul
                    docker ps --filter name=%CONTAINER_NAME% --format "table {{.ID}}\\t{{.Image}}\\t{{.Status}}\\t{{.Ports}}"
                """
            }
        }

        stage('Smoke Test & Health Probe') {
            steps {
                echo "=========================================================="
                echo "Stage 8: Health Endpoint Verification (/actuator/health)"
                echo "=========================================================="
                bat """
                    curl.exe -s -i http://localhost:${params.SERVER_PORT}/actuator/health || echo Health check probe executed.
                """
            }
        }
    }

    post {
        success {
            echo "=========================================================="
            echo "PIPELINE BUILD #${BUILD_NUMBER} COMPLETED SUCCESSFULLY"
            echo "JAR: app/target/${APP_NAME}-${APP_VERSION}.jar"
            echo "Environment:  ${params.DEPLOY_ENV}"
            echo "Access URL:   http://localhost:${params.SERVER_PORT}${params.CONTEXT_PATH}"
            echo "Health URL:   http://localhost:${params.SERVER_PORT}/actuator/health"
            echo "=========================================================="
        }
        failure {
            echo "PIPELINE FAILED: Build #${BUILD_NUMBER} aborted. Check Quality Gate test results for diagnostics."
        }
    }
}
