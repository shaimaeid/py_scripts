pipeline {
    agent any
    tools {
        // Use the Git tool configured in Jenkins Global Tool Configuration
        git 'Default'
    }
        environment {
        // Define your AWS credentials here (replace with your own values)
        AWS_ACCESS_KEY_ID     = credentials('aws_access_key_ID')
        AWS_SECRET_ACCESS_KEY = credentials('aws_access_key')
        AWS_REGION            = 'xxx' // Replace with your desired region
        ECR_REGISTRY          = 'xxx' // Replace with your ECR registry URL
        IMAGE_NAME            = 'xxx'
    }

    stages {
        stage('Copy .env File') {
            steps {
                script {
                    // Checkout source code
                    checkout scm

                    // Copy .env file from /home/env/.project_env to workspace
                    sh 'cp /env/py_env.env ${WORKSPACE}/.env'
                }
            }
        }

        stage('Build and Push Docker Image to ECR') {
            steps {
                script {
                    // Build Docker image locally
                    docker.build("/leadsmart:py_dashboard")
                        // Log in to Amazon ECR using AWS CLI with credentials from Jenkins secrets
                        sh "aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}"
                        sh "aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}"
                        sh "aws configure set region ${AWS_REGION}"

                        // Log in to Amazon ECR using AWS CLI
                        sh "aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 661556210720.dkr.ecr.eu-west-1.amazonaws.com"

                        // Push Docker image to Amazon ECR using AWS CLI
                        sh "docker push /leadsmart:py_dashboard"
                    
                }
            }
        }
    }

    post {
        success {
            // Cleanup workspace after a successful build
            cleanWs()
        }
    }
}
