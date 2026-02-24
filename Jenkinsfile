pipeline {
    agent any
    
    parameters {
        string(name: 'BRD_FILE', defaultValue: 'data/brd_sample.txt', description: 'Path to BRD file')
        string(name: 'TEST_NAME', defaultValue: 'GeneratedTest', description: 'Base name for generated tests')
        booleanParam(name: 'USE_STRONG_MODEL', defaultValue: true, description: 'Use stronger LLM model')
    }
    
    environment {
        PYTHON_VERSION = '3.12'
        JAVA_HOME = tool 'JDK-11'
        MAVEN_HOME = tool 'Maven-3.9'
        PATH = "${MAVEN_HOME}/bin:${JAVA_HOME}/bin:${env.PATH}"
    }
    
    stages {
        stage('Setup') {
            steps {
                echo 'Setting up environment...'
                sh 'python3 --version'
                sh 'java -version'
                sh 'mvn --version'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 -m pip install -r requirements.txt
                '''
            }
        }
        
        stage('Start Ollama') {
            steps {
                echo 'Starting Ollama service...'
                sh '''
                    # Start Ollama in background
                    ollama serve > ollama.log 2>&1 &
                    sleep 5
                    
                    # Pull model if not exists
                    ollama pull qwen2.5:latest || true
                '''
            }
        }
        
        stage('Generate Tests') {
            steps {
                echo "Generating tests from BRD: ${params.BRD_FILE}"
                sh """
                    python3 main.py \\
                        --brd ${params.BRD_FILE} \\
                        --base-name ${params.TEST_NAME} \\
                        ${params.USE_STRONG_MODEL ? '--use-strong-model' : ''}
                """
            }
        }
        
        stage('Prepare Java Project') {
            steps {
                echo 'Setting up Maven project structure...'
                sh '''
                    mkdir -p test-project/src/test/java/com/automation
                    cp outputs/tests/*.java test-project/src/test/java/com/automation/ || true
                    cp cicd/pom.xml test-project/
                '''
            }
        }
        
        stage('Compile Tests') {
            steps {
                dir('test-project') {
                    echo 'Compiling generated Java tests...'
                    sh 'mvn clean compile test-compile'
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                dir('test-project') {
                    echo 'Executing Selenium tests...'
                    sh 'mvn test || true'
                }
            }
        }
        
        stage('Generate Reports') {
            steps {
                dir('test-project') {
                    echo 'Generating test reports...'
                    sh 'mvn surefire-report:report || true'
                }
            }
        }
    }
    
    post {
        always {
            echo 'Archiving artifacts...'
            
            // Archive generated code
            archiveArtifacts artifacts: 'outputs/**/*.feature, outputs/**/*.java', 
                            allowEmptyArchive: true
            
            // Archive compiled tests
            archiveArtifacts artifacts: 'test-project/target/**/*.class', 
                            allowEmptyArchive: true
            
            // Publish test results
            junit testResults: 'test-project/target/surefire-reports/*.xml', 
                 allowEmptyResults: true
            
            // Publish HTML report
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'test-project/target/site',
                reportFiles: 'surefire-report.html',
                reportName: 'Test Execution Report'
            ])
            
            // Stop Ollama
            sh 'pkill ollama || true'
        }
        
        success {
            echo '✅ Pipeline completed successfully!'
            // Add notifications (Slack, email, etc.)
        }
        
        failure {
            echo '❌ Pipeline failed!'
            // Add failure notifications
        }
    }
}
