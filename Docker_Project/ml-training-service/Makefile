build:
	docker build -t model-trainer .

test:
	docker run -v ${MODEL_DIR}:/app/tests/data/models model-trainer python -m pytest ./tests/e2e/

all: build test
