pipeline {
  agent any

  options {
    timestamps()
    ansiColor('xterm')
    disableConcurrentBuilds()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  parameters {
    choice(
      name: 'TEST_SCOPE',
      choices: ['ui', 'api', 'ui_api', 'all_no_mobile', 'mobile'],
      description: 'Какие тесты запускать'
    )
    string(name: 'UI_BASE_URL', defaultValue: 'https://www.rustore.ru', description: 'Base URL UI')
    choice(name: 'UI_BROWSER', choices: ['chrome', 'firefox'], description: 'Браузер для UI')
    string(name: 'API_BASE_URL', defaultValue: 'https://fakestoreapi.com', description: 'Base URL API')
    string(name: 'API_TIMEOUT', defaultValue: '15', description: 'Timeout API (сек)')
    string(name: 'SELENOID_URL', defaultValue: '', description: 'SELENOID host или full URL')
    string(name: 'SELENOID_LOGIN', defaultValue: '', description: 'SELENOID login (опционально)')
    password(name: 'SELENOID_PASS', defaultValue: '', description: 'SELENOID pass (опционально)')
  }

  environment {
    PIP_DISABLE_PIP_VERSION_CHECK = '1'
    PYTHONDONTWRITEBYTECODE = '1'
    PYTHONUNBUFFERED = '1'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Set up Python') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run tests') {
      steps {
        sh '''
          . .venv/bin/activate

          MARK_EXPR=""
          EXTRA_ENV=""
          case "${TEST_SCOPE}" in
            ui)
              MARK_EXPR="-m ui tests/ui"
              ;;
            api)
              MARK_EXPR="-m api tests/api"
              EXTRA_ENV="API_RETRIES=6 API_RETRY_DELAY_SECONDS=2.0"
              ;;
            ui_api)
              MARK_EXPR="-m 'ui or api' tests"
              EXTRA_ENV="API_RETRIES=6 API_RETRY_DELAY_SECONDS=2.0"
              ;;
            all_no_mobile)
              MARK_EXPR="-m 'ui or api' tests"
              EXTRA_ENV="API_RETRIES=6 API_RETRY_DELAY_SECONDS=2.0"
              ;;
            mobile)
              MARK_EXPR="-m mobile tests/mobile"
              ;;
            *)
              echo "Unsupported TEST_SCOPE=${TEST_SCOPE}"
              exit 1
              ;;
          esac

          ${EXTRA_ENV} pytest ${MARK_EXPR} --alluredir=allure-results
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
      allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
    }
  }
}
