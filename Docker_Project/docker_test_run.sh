docker stop resql || true
docker-compose -f docker-compose.test.yml up -d
docker logs -f testing-framework --tail 0
docker-compose -f docker-compose.test.yml stop
docker-compose up -d