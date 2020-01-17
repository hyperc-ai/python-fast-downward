The Fast-Downward Planning System (www.fast-downward.org) with Critical Hop patches 

Building:

```
python 3.7 setup.py bdist_wheel
```

Publishing:

1. Build the manylinux distribution

alternatively, rename platform tag to `manylinux1_x86_64`

2. Upload

```
twine upload dist/*
```
