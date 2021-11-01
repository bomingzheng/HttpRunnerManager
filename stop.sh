ps -aux | grep python|xargs kill -9
rm -rf djo.out rabbitmq.out worker.out celery.out flower.out
