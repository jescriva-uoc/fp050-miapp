pipeline {
    agent any
    triggers { githubPush() }
    environment { IMAGE = "miapp:${BUILD_NUMBER}" }
    stages {
        stage('Build') {
            steps {
                sh '''#!/bin/bash
                    set -e
                    eval $(minikube -p minikube docker-env)
                    docker build -t $IMAGE -t miapp:latest .
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    kubectl apply -f k8s/
                    kubectl set image deployment/miapp miapp=$IMAGE
                    kubectl rollout status deployment/miapp --timeout=120s
                '''
            }
        }
        stage('Verificar') {
            steps { sh 'kubectl get pods -l app=miapp -o wide && kubectl get svc miapp' }
        }
    }
}
