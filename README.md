The Fast-Downward Planning System (www.fast-downward.org) with Critical hop patches 

Building:

```
python 3.7 setup.py bdist_wheel
```

Publishing:

```
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```
