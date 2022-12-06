pipeline {
    agent any

    parameters {
        booleanParam(
                name: "RELEASE",
                description: "Build a release from current commit",
                defaultValue: false
        )
        string(
                name: "RELEASE_VERSION",
                description: "The version to be released. Fill in only when performing release. For example 1.0.0",
                defaultValue: null
        )
        string(
                name: "NEXT_DEVELOPMENT_VERSION",
                description: "Next version development version. Fill in only when performing release. For example 1.0.1-SNAPSHOT",
                defaultValue: null
        )
    }

    tools {
        maven 'Default'
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }

    stages {
        stage('Build & deploy') {
            steps {
                withCredentials([
                        usernamePassword(
                                credentialsId: 'riigiportaal-nexus',
                                usernameVariable: 'USERNAME',
                                passwordVariable: 'PASSWORD')]) {
                    withMaven() {
                        sh 'mvn clean -U deploy'
                    }
                }
            }
            post {
                success {
                    sh 'echo "success"'
                }
                failure {
                    sh 'echo "fail"'
                }
            }
        }
        stage("Release") {
            when {
                expression {
                    params.RELEASE && params.RELEASE_VERSION != null && params.NEXT_DEVELOPMENT_VERSION != null
                }
            }
            steps {
                withCredentials([
                        usernamePassword(
                                credentialsId: 'riigiportaal-nexus',
                                usernameVariable: 'USERNAME',
                                passwordVariable: 'PASSWORD')]) {
                    withMaven() {
                        sh "mvn clean -U -B -DreleaseVersion=${RELEASE_VERSION} -DdevelopmentVersion=${NEXT_DEVELOPMENT_VERSION} -Djava.awt.headless=true clean release:prepare release:perform -DdryRun"
                    }
                }
            }
        }
    }
}
