pipeline{
    agent any
    stages {
        stage('高德api_state'){
            steps{
                bat 'python Runner.py'
            }
        }
    }
    post {
        always {
            withGroovy {
                'System.setProperty("hudson.model.DirectoryBrowserSupport.CSP","")'
}
            emailext attachLog: true,
            body: '${FILE,path="jenkins_mail_report_template.html"}',
            subject: 'pipeline test mail',
            to: 'zitao@cisco.com,taoziqiang11@sina.com'
        }
    }
}
