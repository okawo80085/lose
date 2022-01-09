![](https://github.com/okawo80085/lose/workflows/unit%20tests/badge.svg)
# lose

wrapper for `PyTables`, has 3 classes rn:

`Loser` - base data handler, run `help()` for more info

`HumanIterator` - iterator, run `help()` for more info

`LOSE` - a mistake

```python
>>> import lose
(;^ω^)
>>> # base data handler class
>>> l = lose.Loser('test.h5', verboseRepr=True)
>>> l
<lose.dataHandler.Loser fname="test.h5", fast_active=False, verboseRepr=True at 0x7fe872fe8730>
test.h5 (File) ''
Last modif.: '2022-01-09T20:15:03+00:00'
Object Tree: 
/ (RootGroup) ''
/x (EArray(100, 640, 480)) ''
/y (EArray(100, 2)) ''

>>>
>>>
>>> # allows loading data
>>> l.load('x', 'y')
# list of [array of x, array of y], i.e. a bunch of data
>>> # as well as saving data
>>> l.save(x=np.ones((400, 640, 480)), y=np.ones((300, 2)))
>>> l
<lose.dataHandler.Loser fname="test.h5", fast_active=False, verboseRepr=True at 0x7fe872fe8730>
test.h5 (File) ''
Last modif.: '2022-01-09T20:20:23+00:00'
Object Tree: 
/ (RootGroup) ''
/x (EArray(500, 640, 480)) ''
/y (EArray(400, 2)) ''

>>>
>>>
>>> # as well as creating new labels
>>> l.new_group(z=(15,), k=(21, 3))
>>> l
<lose.dataHandler.Loser fname="test.h5", fast_active=False, verboseRepr=True at 0x7fe872fe8730>
test.h5 (File) ''
Last modif.: '2022-01-09T20:22:02+00:00'
Object Tree: 
/ (RootGroup) ''
/k (EArray(0, 21, 3)) ''
/x (EArray(500, 640, 480)) ''
/y (EArray(400, 2)) ''
/z (EArray(0, 15)) ''

>>>
>>>
>>> # after a new label was created it can be used for saving arrays
>>> l.save(z=np.zeros((10, 15)), k=np.zeros((50, 21, 3)))
>>> l
<lose.dataHandler.Loser fname="test.h5", fast_active=False, verboseRepr=True at 0x7fe872fe8730>
test.h5 (File) ''
Last modif.: '2022-01-09T20:23:56+00:00'
Object Tree: 
/ (RootGroup) ''
/k (EArray(50, 21, 3)) ''
/x (EArray(500, 640, 480)) ''
/y (EArray(400, 2)) ''
/z (EArray(10, 15)) ''

>>>
>>>
>>> # labels can be removed
>>> l.remove_group('y', 'z')
>>> l
<lose.dataHandler.Loser fname="test.h5", fast_active=False, verboseRepr=True at 0x7f343a4e2730>
test.h5 (File) ''
Last modif.: '2022-01-09T20:26:41+00:00'
Object Tree: 
/ (RootGroup) ''
/k (EArray(50, 21, 3)) ''
/x (EArray(500, 640, 480)) ''

>>>
>>>
>>> # as well as renamed
>>> l.rename_group(x='input', k='output')
>>> l
<lose.dataHandler.Loser fname="test.h5", fast_active=False, verboseRepr=True at 0x7f343a4e2730>
test.h5 (File) ''
Last modif.: '2022-01-09T20:28:07+00:00'
Object Tree: 
/ (RootGroup) ''
/input (EArray(500, 640, 480)) ''
/output (EArray(50, 21, 3)) ''

>>>
>>>
>>># and to get shapes of labels call l.get_shapes
>>> l.get_shapes('input', 'output')
[(500, 640, 480), (50, 21, 3)]

>>>
>>>
>>> # load, save and get_shape methods work in "fast" mode, "fast" mode allows the file open lifetime to be handled outside of the load/save/get_shape calls, to enter "fast" mode pass your data handler instance to a context manger, recommended to be used when performing a lot of iterations over the stored data, here is an example:
>>> with l:
...     for _ in range(200):
...             l.load('input', 'output')
# *a bunch of data*

>>>
>>>
>>> # there is also an iterator, for more info on it's arguments, checkout help(lose.HumanIterator)
>>> iter = lose.HumanIterator('test.h5', 'input', 'output', limit=40)

>>> for i in iter:
...     print(i)
# i on each step will be [batch from 'input' array, batch from 'output' array], these batches depend on the initial iterator parameters
```

## installation
```
pip install lose
```

or

```
pip install -e .
```

or 

```
pip install git+https://github.com/okawo80085/lose
```

## docs

code comments and doc strings

## issues/contributions/what ever
just do it


[change log](changeLog.md)