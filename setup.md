# Запуск бота 
docker compose -f docker/test.yml --env-file docker/.env.test up --build -d                                  
docker compose -f docker/test.yml --env-file docker/.env.test down                                  