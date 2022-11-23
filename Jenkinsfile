pipeline{
    agent any
    withGroovy {
        System.setProperty("hudson.model.DirectoryBrowserSupport.CSP","")
}
    stages {
        stage('高德api_state'){
            steps{
                bat 'python Runner.py'
            }
        }
    }
    post {
        always {
            emailext attachLog: true,
            body: '${FILE,path="jenkins_mail_report_template.html"}',
            subject: 'pipeline test mail',
            to: 'zitao@cisco.com,taoziqiang11@sina.com'
        }
    }
}
