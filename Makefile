.PHONY: install
install:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --two && cp -a .venv/lib/python2.7/site-packages/{workflow,requests,urllib3,chardet,certifi,idna} src/lib/