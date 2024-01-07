pipeline {
    agent any
    options {
        parallelsAlwaysFailFast()
    }
    environment {
        NEXUS_CREDENTIALS = credentials("nexus")
    }
    stages {
        stage("Clean workspace") {
            steps {
                sh "git clean -xdf"
            }
        }
        stage("Run stages in parallel") {
            parallel {
                stage("Run client tests") {
                    agent {
                        docker {
                            image "python:3.11-slim"
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
                        stage("Mark client success") {
                            steps {
                                script {
                                    env.CLIENT_SUCCESS = true
                                }
                            }
                        }
                    }
                }
                stage("Run backend tests") {
                    agent {
                        dockerfile {
                            dir "backend"
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
                        stage("Mark backend success") {
                            steps {
                                script {
                                    env.BACKEND_SUCCESS = true
                                }
                            }
                        }
                    }
                }
                stage("Build and publish artifacts") {
                    when {
                        branch "main"
                        beforeAgent true
                    }
                    stages {
                        stage("Wait for tests to finish") {
                            steps {
                                waitUntil(initialRecurrencePeriod: 5000, quiet: true) {
                                    script {
                                        return env.CLIENT_SUCCESS && env.CLIENT_SUCCESS.toBoolean()
                                    }
                                }
                                waitUntil(initialRecurrencePeriod: 5000, quiet: true) {
                                    script {
                                        return env.BACKEND_SUCCESS && env.BACKEND_SUCCESS.toBoolean()
                                    }
                                }
                            }
                        }
                        stage("Client") {
                            agent {
                                docker {
                                    image "tobix/pywine:3.11"
                                }
                            }
                            environment {
                                HOME = "${env.WORKSPACE}"
                            }
                            stages {
                                stage("Set package version") {
                                    steps {
                                        contentReplace(
                                            configs: [
                                                fileContentReplaceConfig(
                                                    configs: [
                                                        fileContentReplaceItemConfig(
                                                        search: '(VERSION = )"0\\.0\\.0"',
                                                        replace: '$1"0.0.${BUILD_ID}"',
                                                        matchCount: 1,
                                                        verbose: false,
                                                        )
                                                    ],
                                                    fileEncoding: 'UTF-8',
                                                    lineSeparator: 'Unix',
                                                    filePath: 'client/setup.py'
                                                )
                                            ]
                                        )
                                    }
                                }
                                stage("Build exe") {
                                    steps {
                                        dir("client") {
                                            sh """
                                                . /opt/mkuserwineprefix
                                                script -qefc 'wine \$WINEPREFIX/drive_c/Python/python.exe -m pip install .' /dev/null
                                                script -qefc 'wine \$WINEPREFIX/drive_c/Python/Scripts/pyinstaller.exe --onefile main.py -n leaguepushups-0.0.${BUILD_ID}' /dev/null
                                            """
                                        }
                                    }
                                }
                                stage("Upload exe") {
                                    steps {
                                        dir("client") {
                                            sh "curl -u '${NEXUS_CREDENTIALS_USR}:${NEXUS_CREDENTIALS_PSW}' --upload-file dist/leaguepushups-0.0.${BUILD_ID}.exe https://nexus.buddaphest.se/repository/raw-releases/league-push-ups/leaguepushups-0.0.${BUILD_ID}.exe"
                                        }
                                    }
                                }
                            }
                        }
                        stage("Backend") {
                            steps {
                                contentReplace(
                                    configs: [
                                        fileContentReplaceConfig(
                                            configs: [
                                                fileContentReplaceItemConfig(
                                                search: '(VERSION = )"0\\.0\\.0"',
                                                replace: '$1"0.0.${BUILD_ID}"',
                                                matchCount: 1,
                                                verbose: false,
                                                )
                                            ],
                                            fileEncoding: 'UTF-8',
                                            lineSeparator: 'Unix',
                                            filePath: 'backend/setup.py'
                                        )
                                    ]
                                )
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
        }
    }
    post {
        always {
            sh "docker system prune -af"
        }
    }
}
