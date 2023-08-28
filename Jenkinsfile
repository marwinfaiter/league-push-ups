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
                        sh "python setup.py bdist_wheel --dist-dir client/dist"
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
    }
    post {
        always {
            sh "docker system prune -af"
        }
    }
}
