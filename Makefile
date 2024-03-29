help:
	@echo "install - create venv and install dependencies"
	@echo "fmt - format source code with black"
	@echo "test - run unit tests"
	@echo "synth - synthesize all project files"
	@echo "build - build PyPi package"
	@echo "publish - Publish packages to Pypi"
	@echo "clean - remove build, test, and Python artifacts locally"

VENV = .env
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

install: venv dependency

venv:
	@python3 -m venv ".env"

dependency:
	$(PIP) install -r ./requirements.txt
	$(PIP) install -r ./requirements-dev.txt

build:
	$(PYTHON) -m build

publish:
	$(PYTHON) -m twine upload dist/*

test:
	pytest

synth:
	npx cdk synth --quiet -a "python app.py"

fmt:
	$(PYTHON) -m black .

# need to define arn partition by region
# arn partition could be aws or aws-cn
assume-role:
	aws sts assume-role --role-arn "arn:aws-cn:iam::${REMOTE_ACCOUNT_ID}:role/${REMOTE_ROLE}" --role-session-name "cdksession" >.assume_role_json
	echo "export AWS_ACCESS_KEY_ID=$$(cat .assume_role_json | jq '.Credentials.AccessKeyId' -r)" >.env.assumed_role
	echo "export AWS_SECRET_ACCESS_KEY=$$(cat .assume_role_json | jq '.Credentials.SecretAccessKey' -r)" >>.env.assumed_role
	echo "export AWS_SESSION_TOKEN=$$(cat .assume_role_json | jq '.Credentials.SessionToken' -r)" >>.env.assumed_role
	rm .assume_role_json

clean:
	@rm -fr cdk.out/
	@rm -fr .tox/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name "*.py[co]" -o -name .pytest_cache -exec rm -rf {} +
	@find . -name '*.egg' -exec rm -f {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +
	@rm -fr build/
	@rm -fr dist/

