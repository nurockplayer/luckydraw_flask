build:
	pip3 install -r requirements.txt
	-mysqladmin -f -h mariadb -u root drop luckydraw
	mysql -u root -h mariadb -e "CREATE DATABASE luckydraw CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
	flask db upgrade

test:
	pytest -s

test-cov:
	pytest --cov=. --ignore=venv --cov-report=html

.PHONY: build test test-cov
