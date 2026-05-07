pipeline {
  agent {
    kubernetes {
      yaml '''
        apiVersion: v1
        kind: Pod
        spec:
          serviceAccountName: jenkins-agent
          containers:
          - name: python
            image: python:3.12-slim
            command: ["sleep"]
            args: ["infinity"]
          - name: kaniko
            image: gcr.io/kaniko-project/executor:debug
            command: ["sleep"]
            args: ["infinity"]
            volumeMounts:
            - name: docker-config
              mountPath: /kaniko/.docker
          - name: kubectl
            image: bitnami/kubectl:latest
            command: ["sleep"]
            args: ["infinity"]
            securityContext:
              runAsUser: 0
          volumes:
          - name: docker-config
            secret:
              secretName: dockerhub-creds
              items:
              - key: .dockerconfigjson
                path: config.json
      '''
    }
  }

  environment {
    IMAGE = "docker.io/musab35/cicd-demo"
    TAG   = "${env.BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Test') {
      steps {
        container('python') {
          sh '''
            pip install -r requirements.txt pytest
            pytest -q
          '''
        }
      }
    }

    stage('Build & Push image') {
      steps {
        container('kaniko') {
          sh '''
            /kaniko/executor \
              --context=`pwd` \
              --dockerfile=Dockerfile \
              --destination=${IMAGE}:${TAG} \
              --destination=${IMAGE}:latest
          '''
        }
      }
    }

    stage('Deploy to k8s') {
      steps {
        container('kubectl') {
          sh '''
            sed -i "s|IMAGE_PLACEHOLDER|${IMAGE}:${TAG}|g" k8s/deployment.yaml
            kubectl apply -f k8s/deployment.yaml
            kubectl -n default rollout status deploy/cicd-demo --timeout=120s
          '''
        }
      }
    }
  }

  post {
    success { echo "Deployed ${IMAGE}:${TAG}" }
    failure { echo "Pipeline failed - check console output" }
  }
}
