# Mattilda project

## Build containers
```
docker-compose build
```

## Run containers
```
docker-compose up
```

## Stop services
```
docker-compose down
```

## See logs
```
docker-compose logs -f
```

## Running tests
Run sh inside the container
```
docker-compose exec web sh
```
Then inside the sh run the tests
```
pytest -q
```

## Documentation
- API root → http://localhost:8000 
- Swagger UI → http://localhost:8000/docs
- Redoc → http://localhost:8000/redoc
