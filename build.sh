rm dist/*
python3 setup.py sdist bdist_wheel
python3 setup.py install
python3 -m twine upload --verbose -r pypi  dist/*

