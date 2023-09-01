pipeline {
    agent any
    environment {
        TWINE_CREDENTIALS = credentials("nexus")
    }
    stages {
        stage("Clean workspace") {
            steps {
                sh "git clean -xdf"
            }
        }
        stage("Run client tests") {
            agent {
                docker {
                    image "python:3.11-slim"
                    reuseNode true
                }
            }
            environment {
                HOME = "${env.WORKSPACE}"
            }
            stages {
                stage("Install dependencies") {
                    steps {
                        sh "python -m pip install --user client/[test]"
                    }
                }
                stage("Run tests") {
                    stages {
                        stage("Run mypy") {
                            steps {
                                sh "python -m mypy client/league_push_ups client/tests"
                            }
                        }
                        stage("Run pylint") {
                            steps {
                                sh "python -m pylint client/league_push_ups client/tests"
                            }
                        }
                        stage("Run pytest") {
                            steps {
                                sh "python -m pytest client/tests"
                            }
                        }
                    }
                }
                stage("Build wheel") {
                    steps {
                        dir("client") {
                            sh "python setup.py bdist_wheel"
                        }
                    }
                }
                stage("Publish wheel") {
                    when {
                        branch 'main'
                    }
                    steps {
                        sh "python -m pip install --user twine"
                        sh "python -m twine upload --repository-url https://nexus.buddaphest.se/repository/pypi-releases/ --u '${TWINE_CREDENTIALS_USR}' --p '${TWINE_CREDENTIALS_PSW}' client/dist/*"
                    }
                }
            }
        }
        stage("Run backend tests") {
            agent {
                dockerfile {
                    dir "backend"
                    reuseNode true
                }
            }
            environment {
                HOME = "${env.WORKSPACE}"
            }
            stages {
                stage("Install dependencies") {
                    steps {
                        sh "python -m pip install --user backend/[test]"
                    }
                }
                stage("Run tests") {
                    stages {
                        stage("Run mypy") {
                            steps {
                                sh "python -m mypy backend/league_push_ups_backend"
                            }
                        }
                        stage("Run pylint") {
                            steps {
                                sh "python -m pylint backend/league_push_ups_backend"
                            }
                        }
                    }
                }
            }
        }
        stage("Build and publish docker") {
            stages {
                stage("Backend") {
                    steps {
                        script {
                            docker.withRegistry('https://releases.docker.buddaphest.se', 'nexus') {

                                def customImage = docker.build("marwinfaiter/league_push_ups:backend-${env.BUILD_ID}", "--target prod backend")

                                customImage.push()
                                customImage.push("backend")
                            }
                        }
                    }
                }
                stage("Frontend") {
                    steps {
                        script {
                            docker.withRegistry('https://releases.docker.buddaphest.se', 'nexus') {

                                def customImage = docker.build("marwinfaiter/league_push_ups:frontend-${env.BUILD_ID}", "--target production-stage frontend")

                                customImage.push()
                                customImage.push("frontend")
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            sh "docker system prune -af"
        }
    }
}
