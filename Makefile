.PHONY: initial program setup start_dev


start_compose:
	@echo "Running docker compose..."
	docker-compose up -d

shutdown_compose::
	@echo "Shutting down docker compose..."
	docker-compose down

start_dev:
	@echo "Running app in development.."
	cd src && uvicorn main:app --reload --host 0.0.0.0 --port 80

start_prod:
	@echo "Running app in production..."
	cd src && gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:80