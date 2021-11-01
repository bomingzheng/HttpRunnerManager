ps -aux | grep python|xargs kill -9
nohup python manage.py runserver 192.168.1.129:8000 >djo.out 2>&1 &
nohup ./rabbitmq-server --loglevel=info >rabbitmq.out 2>&1 &
nohup python3 manage.py celery -A HttpRunnerManager worker --loglevel=info >worker.out 2>&1 &
nohup python3 manage.py celery beat --loglevel=info >celery.out 2>&1 &
nohup flower >flower.out 2>&1 &
