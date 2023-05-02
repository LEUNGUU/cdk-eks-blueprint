help:
	@echo "install - Use projen to manage dependencies"
	@echo "lint - check source code with flake8"
	@echo "fmt - format source code with black"
	@echo "test - run unit tests"
	@echo "deploy - deploy all your stacks"
	@echo "destroy - destroy all your stacks"
	@echo "clean - remove build, test, and Python artifacts locally"

VENV = .env
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

install: default

default:
	npx projen default

package:
	npx projen package

publish:
	npx projen publish

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

