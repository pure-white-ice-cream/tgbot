pipeline {
    agent any

    environment {
        TOKEN = credentials('TG_BOT_TOKEN')
    }

    stages {
        stage('签出') {
            steps {
                echo '正在签出源代码...'
                checkout scm
            }
        }

        stage('安装环境') {
            steps {
                echo '正在设置 python 虚拟环境...'
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('部署') {
            steps {
                echo '正在后台部署 Python 应用程序...'
                sh '''
                . venv/bin/activate

                # 定义日志文件与PID文件
                LOG_FILE="app.log"
                PID_FILE="app.pid"

                # 如果旧进程存在，则终止它（避免重复运行）
                if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
                    echo "检测到旧进程。正在终止..."
                    kill $(cat "$PID_FILE") || true
                    sleep 1
                fi

                # 启动新进程到后台并记录PID
                nohup python src/app.py > "$LOG_FILE" 2>&1 &
                echo $! > "$PID_FILE"

                echo "Python 应用程序已启动. PID=$(cat $PID_FILE)"
                '''
            }
        }
    }

    post {
        success {
            echo "✅ 部署完成"
        }
        failure {
            echo "❌ 部署失败，请检查日志"
        }
    }

}
