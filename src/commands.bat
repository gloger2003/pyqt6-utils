python setup.py sdist bdist_wheel
twine upload --repository pypi dist/*
twine upload --repository testpypi dist/*