def glb_prod_approved = false
def glb_skip_ci = false

def get_version(json_file) {
    return sh(script: "jq -r '.version' ${json_file}", returnStdout: true).trim()
}

def get_repo_name() {
    if (env.GIT_URL) {
        return env.GIT_URL.tokenize('/').last().replaceAll('.git$', '')
    } else {
        error("GIT_URL environment variable is not available.")
    }
}

def get_branch_name() {
    def branchName = env.GIT_BRANCH ? env.GIT_BRANCH : sh(script: "git rev-parse --abbrev-ref HEAD", returnStdout: true).trim()
    return branchName.replaceFirst(/^origin\//, '')
}

def skip_ci() {
    def commitMessage = sh(script: "git log -1 --pretty=%B", returnStdout: true).trim()
    echo "commitMessage: ${commitMessage}"
    echo "skip_ci: ${commitMessage.contains('[skip ci]')}"
    return commitMessage.contains('[skip ci]')
}

def get_tag_name() {
    return sh(script: 'git describe --tags --abbrev=0', returnStdout: true).trim()
}

def log_env_variables(variable_names) {
    variable_names.sort().each { varName ->
        def value = env.getProperty(varName) ?: "Variable '${varName}' is not defined."
        echo "${varName}: ${value}"
    }
}

def doesArtifactExist() {
    def artifactPattern = "bin/${env.BINARY_NAME}-*.tar.gz"
    def artifactPresent = sh(script: "ls ${artifactPattern} 1> /dev/null 2>&1 && echo true || echo false", returnStdout: true).trim() == 'true'

    if (!artifactPresent) {
        try {
            copyArtifacts(
                projectName: "${env.JOB_NAME}",
                selector: specific("${BUILD_NUMBER}"),
                filter: artifactPattern
            )
            echo "Artifact copied to bin directory."
            artifactPresent = true
        } catch (Exception e) {
            echo "Artifact copy failed: ${e.message}"
            artifactPresent = false
        }
    }
    return artifactPresent
}


pipeline {
    agent any
    options {
        ansiColor('vga')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        timeout(time: 10, unit: "MINUTES")
    }

    triggers {
        pollSCM 'H/5 * * * *'
    }

    environment {
        AAI_DEPLOYMENT_REGION   = 'us-west-2'
        BINARY_NAME             = 'aai-agent'
        // MAIN_BRANCH_NAME        = 'main'
        MAIN_BRANCH_NAME        = 'epic/EI-1132/sea'
    }

    stages {
        // ====================================================================
        stage('Initialize stage') {
        // ====================================================================
            steps {
                script {
                    // --------------------------------------------------------
                    label 'Initialize varaibales'
                    // --------------------------------------------------------
                    env.BRANCH_NAME = get_branch_name()
                    env.TAG_NAME = get_tag_name()
                    env.RELEASE_TYPE = TAG_NAME.replaceAll(/^release-/, '')
                    env.REPO_NAME = get_repo_name()
                    glb_skip_ci = skip_ci()
                    // print variable values
                    sh "docker version"
                    sh "docker info"
                    sh "which jq && jq --version"
                    log_env_variables([
                        'AAI_DEPLOYMENT_REGION',
                        'AAI_VERSION_STRING',
                        'BINARY_NAME',
                        'BRANCH_NAME',
                        'BUILD_NUMBER',
                        'JOB_NAME',
                        'MAIN_BRANCH_NAME',
                        'RELEASE_TYPE',
                        'REPO_NAME',
                        'TAG_NAME'
                    ])
                    echo "glb_skip_ci: ${glb_skip_ci}"
                    echo "glb_prod_approved: ${glb_prod_approved}"
                }
            }
        }

        // ====================================================================
        stage('Build release') {
        // ====================================================================
            when {
                allOf {
                    expression { env.BRANCH_NAME == env.MAIN_BRANCH_NAME }
                    expression { !glb_skip_ci }
                    anyOf {
                        expression { env.RELEASE_TYPE == 'patch' }
                        expression { env.RELEASE_TYPE == 'minor' }
                        expression { env.RELEASE_TYPE == 'major' }
                    }
                }
            }
            steps {
                script {
                    // --------------------------------------------------------
                    label "${env.BINARY_NAME} Release build started - Notify Slack Channel"
                    // --------------------------------------------------------
                    slackSend color: "#FFFF00", message: "${env.BINARY_NAME} release build started - (<${env.BUILD_URL}|Open job#${env.BUILD_NUMBER}>)"
                }
                script {
                    // --------------------------------------------------------
                    label "Remove release tag to prevent pipeline running again"
                    // --------------------------------------------------------
                    withCredentials([sshUserPrivateKey(credentialsId: 'bitbucket-push', keyFileVariable: 'SSH_KEY_PATH')]) {
                        sh "GIT_SSH_COMMAND=\"ssh -i $SSH_KEY_PATH\" git push origin --delete ${env.TAG_NAME}"
                    }
                }
                script {
                    nodejs('Node 20.18.0') {
                        echo "PWD build: ${pwd()}"
                        sh "node -v"
                        sh "npm -v"
                        sh "npm ci"
                        sh "npm version ${env.RELEASE_TYPE} --no-git-tag-version"
                        env.AAI_VERSION_STRING = get_version('package.json')
                        sh "git add ."
                        sh "git commit -m \"${env.AAI_VERSION_STRING} [skip ci]\""
                        sh "git tag v${env.AAI_VERSION_STRING}"
                        log_env_variables(['AAI_VERSION_STRING'])
                        archiveArtifacts artifacts: "bin/${env.BINARY_NAME}-${env.AAI_VERSION_STRING}.tar.gz", allowEmptyArchive: false
                    }
                }
                script {
                    // ---------------------------------------------------------
                    label "${env.BINARY_NAME}-${env.AAI_VERSION_STRING} Build - Adding release tag: ${env.AAI_VERSION_STRING}"
                    // ---------------------------------------------------------
                    withCredentials([sshUserPrivateKey(credentialsId: 'bitbucket-push', keyFileVariable: 'SSH_KEY_PATH')]) {
                        sh "git tag -l | grep ${env.AAI_VERSION_STRING} || echo 'Tag ${env.AAI_VERSION_STRING} not created'"
                        sh "GIT_SSH_COMMAND=\"ssh -i $SSH_KEY_PATH\" git push origin HEAD:${env.MAIN_BRANCH_NAME}"
                        sh "GIT_SSH_COMMAND=\"ssh -i $SSH_KEY_PATH\" git push --tags"
                    }
                }
            }
            post {
                success {
                    script {
                        // ---------------------------------------------------------
                        label "${env.BINARY_NAME}-${env.AAI_VERSION_STRING} release build success - Notify Slack Channel"
                        // ---------------------------------------------------------
                        slackSend color: "#00FF00", message: "${env.BINARY_NAME}-${env.AAI_VERSION_STRING} release build success - (<${env.BUILD_URL}|Open job#${env.BUILD_NUMBER}>)"
                    }
                }
                unsuccessful {
                    script {
                        // ---------------------------------------------------------
                        label "aai-build release build failed - Notify Slack Channel"
                        // ---------------------------------------------------------
                        slackSend color: "#FF0000", failOnError: true, message: "${env.BINARY_NAME}-${env.AAI_VERSION_STRING} release build failed - (<${env.BUILD_URL}|Open job#${env.BUILD_NUMBER}>)"
                    }
                }
            }
        }

        // stage('Debugging before DEV/QA') {
        //     steps {
        //         script {
        //             echo "glb_skip_ci: ${glb_skip_ci}"
        //             echo "doesArtifactExist: ${doesArtifactExist()}"
        //         }
        //     }
        // }

        // ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        stage('Deploy in parallel to DEV and QA') {
            when {
                branch "${env.MAIN_BRANCH_NAME}"
                expression { doesArtifactExist() }
            }
            parallel {
        // ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
                // ====================================================================
                stage('DEV - Deploy') {
                // ====================================================================
                    environment {
                        AAI_DEPLOYMENT_ENV      = 'dev'
                        AAI_AWS_CREDS           = "AWS_${AAI_DEPLOYMENT_ENV.toUpperCase()}"
                        LOG_LEVEL               = 'debug'
                    }
                    steps {
                        dir("${AAI_DEPLOYMENT_ENV}-deploy-workspace") {
                            script {
                                // --------------------------------------------------------
                                label "${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy started - Notify Slack Channel"
                                // --------------------------------------------------------
                                slackSend color: "#FFFF00", message: "${env.BINARY_NAME}-${env.AAI_VERSION_STRING} ${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy started - (<${env.BUILD_URL}|Open job#${env.BUILD_NUMBER}>)"
                            }
                            script {
                                // ---------------------------------------------------------
                                label "${AAI_DEPLOYMENT_ENV.toUpperCase()} - deploy"
                                // ---------------------------------------------------------
                                echo "PWD ${AAI_DEPLOYMENT_ENV}: ${pwd()}"
                                sh 'mkdir -p ./scripts ./bin'
                                sh 'cp ../scripts/sea-deploy-to-s3.sh ./scripts/'
                                sh 'cp ../scripts/common-lib.sh ./scripts/'
                                sh 'cp ../bin/* ./bin/'
                                withAWS(credentials: "${AAI_AWS_CREDS}", region: "${AAI_DEPLOYMENT_REGION}") {
                                    sh "./scripts/sea-deploy-to-s3.sh"
                                }
                            }
                        }
                    }
                    post {
                        success {
                            script {
                                // ---------------------------------------------------------
                                label "${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy success - Notify Slack Channel"
                                // ---------------------------------------------------------
                                slackSend color: "#00FF00", message: "${env.BINARY_NAME}-${env.AAI_VERSION_STRING} ${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy success - (<${env.BUILD_URL}|Open job#${env.BUILD_NUMBER}>)"
                            }
                        }
                        unsuccessful {
                            script {
                                // ---------------------------------------------------------
                                label "${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy failed - Notify Slack Channel"
                                // ---------------------------------------------------------
                                slackSend color: "#FF0000", failOnError: true, message: "${env.BINARY_NAME}-${env.AAI_VERSION_STRING} ${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy failed - (<${env.BUILD_URL}|Open job#${env.BUILD_NUMBER}>)"
                            }
                        }
                    }
                }

                // ====================================================================
                stage('QA - Deploy') {
                // ====================================================================
                    environment {
                        AAI_DEPLOYMENT_ENV      = 'qa'
                        AAI_AWS_CREDS           = "AWS_${AAI_DEPLOYMENT_ENV.toUpperCase()}"
                        LOG_LEVEL               = 'debug'
                    }
                    steps {
                        dir("${AAI_DEPLOYMENT_ENV}-deploy-workspace") {
                            script {
                                // --------------------------------------------------------
                                label "${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy started - Notify Slack Channel"
                                // --------------------------------------------------------
                                slackSend color: "#FFFF00", message: "${env.BINARY_NAME}-${env.AAI_VERSION_STRING} ${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy started - (<${env.BUILD_URL}|Open job#${env.BUILD_NUMBER}>)"
                            }
                            script {
                                // ---------------------------------------------------------
                                label "${AAI_DEPLOYMENT_ENV.toUpperCase()} - deploy"
                                // ---------------------------------------------------------
                                echo "PWD ${AAI_DEPLOYMENT_ENV}: ${pwd()}"
                                sh 'mkdir -p ./scripts ./bin'
                                sh 'cp ../scripts/sea-deploy-to-s3.sh ./scripts/'
                                sh 'cp ../scripts/common-lib.sh ./scripts/'
                                sh 'cp ../bin/* ./bin/'
                                withAWS(credentials: "${AAI_AWS_CREDS}", region: "${AAI_DEPLOYMENT_REGION}") {
                                    sh "./scripts/sea-deploy-to-s3.sh"
                                }
                            }
                        }
                    }
                    post {
                        success {
                            script {
                                // ---------------------------------------------------------
                                label "${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy success - Notify Slack Channel"
                                // ---------------------------------------------------------
                                slackSend color: "#00FF00", message: "${env.BINARY_NAME}-${env.AAI_VERSION_STRING} ${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy success - (<${env.BUILD_URL}|Open job#${env.BUILD_NUMBER}>)"
                            }
                        }
                        unsuccessful {
                            script {
                                // ---------------------------------------------------------
                                label "${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy failed - Notify Slack Channel"
                                // ---------------------------------------------------------
                                slackSend color: "#FF0000", failOnError: true, message: "${env.BINARY_NAME}-${env.AAI_VERSION_STRING} ${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy failed - (<${env.BUILD_URL}|Open job#${env.BUILD_NUMBER}>)"
                            }
                        }
                    }
                }
            }
        }

        // stage('Debugging before PROD') {
        //     steps {
        //         script {
        //             echo "glb_skip_ci: ${glb_skip_ci}"
        //             echo "doesArtifactExist: ${doesArtifactExist()}"
        //         }
        //     }
        // }

        // ====================================================================
        stage('PROD - Approval') {
        // ====================================================================
            when {
                allOf {
                    branch "${env.MAIN_BRANCH_NAME}"
                    expression { doesArtifactExist() }
                }
            }
            steps {
                script {
                    input message: "Deploy to Production?", ok: "Deploy"
                    glb_prod_approved = true
                    log_env_variables([
                        'AAI_DEPLOYMENT_REGION',
                        'AAI_VERSION_STRING',
                        'BINARY_NAME',
                        'BRANCH_NAME',
                        'BUILD_NUMBER',
                        'JOB_NAME',
                        'MAIN_BRANCH_NAME',
                        'RELEASE_TYPE',
                        'REPO_NAME',
                        'TAG_NAME'
                    ])
                    echo "glb_skip_ci: ${glb_skip_ci}"
                    echo "glb_prod_approved: ${glb_prod_approved}"
                }
            }
        }

        // ====================================================================
        stage('PROD - Deploy') {
            when {
                expression { glb_prod_approved }
            }
            environment {
                AAI_DEPLOYMENT_ENV      = 'prod'
                AAI_AWS_CREDS           = "AWS_${AAI_DEPLOYMENT_ENV.toUpperCase()}"
                LOG_LEVEL               = 'error'
            }
            steps {
                script {
                    // --------------------------------------------------------
                    label "${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy started - Notify Slack Channel"
                    // --------------------------------------------------------
                    slackSend color: "#FFFF00", message: "${env.BINARY_NAME}-${env.AAI_VERSION_STRING} ${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy started - (<${env.BUILD_URL}|Open job#${env.BUILD_NUMBER}>)"
                }
                // copyArtifacts(
                //     projectName: "${env.JOB_NAME}",
                //     selector: specific("${BUILD_NUMBER}"),
                //     filter: "bin/${env.BINARY_NAME}-${env.AAI_VERSION_STRING}.tar.gz"
                // )
                script {
                    dir("${AAI_DEPLOYMENT_ENV}-deploy-workspace") {
                        // ---------------------------------------------------------
                        label "${AAI_DEPLOYMENT_ENV.toUpperCase()} - deploy"
                        // ---------------------------------------------------------
                            log_env_variables([
                                'AAI_DEPLOYMENT_REGION',
                                'AAI_VERSION_STRING',
                                'BINARY_NAME',
                                'BRANCH_NAME',
                                'BUILD_NUMBER',
                                'JOB_NAME',
                                'MAIN_BRANCH_NAME',
                                'RELEASE_TYPE',
                                'REPO_NAME',
                                'TAG_NAME'
                        ])
                        echo "glb_skip_ci: ${glb_skip_ci}"
                        echo "glb_prod_approved: ${glb_prod_approved}"
                        echo "PWD ${AAI_DEPLOYMENT_ENV}: ${pwd()}"
                        sh 'mkdir -p ./scripts ./bin'
                        sh 'cp ../scripts/sea-deploy-to-s3.sh ./scripts/'
                        sh 'cp ../scripts/common-lib.sh ./scripts/'
                        sh 'cp ../bin/* ./bin/'
                        withAWS(credentials: "${AAI_AWS_CREDS}", region: "${AAI_DEPLOYMENT_REGION}") {
                            sh "./scripts/sea-deploy-to-s3.sh"
                        }
                    }
                }
            }
            post {
                success {
                    script {
                        // ---------------------------------------------------------
                        label "${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy success - Notify Slack Channel"
                        // ---------------------------------------------------------
                        slackSend color: "#00FF00", message: "${env.BINARY_NAME}-${env.AAI_VERSION_STRING} ${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy success - (<${env.BUILD_URL}|Open job#${env.BUILD_NUMBER}>)"
                    }
                }
                unsuccessful {
                    script {
                        // ---------------------------------------------------------
                        label "${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy failed - Notify Slack Channel"
                        // ---------------------------------------------------------
                        slackSend color: "#FF0000", failOnError: true, message: "${env.JOB_NAME}-${env.AAI_VERSION_STRING} ${AAI_DEPLOYMENT_ENV.toUpperCase()} deploy failed - (<${env.BUILD_URL}|Open job#${env.BUILD_NUMBER}>)"
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
