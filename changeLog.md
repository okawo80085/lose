# Change log

## 0.6.5v
unit test usage changed, also unit tests is a module now(since unit test code is separate from the main library), refer to the [readme](README.md/#unit-tests) for more info

current unit test version: `0.1`

## 0.6.4v
windows only bug fixed

## 0.6.3v
added partial unit tests to lose, to run them do
```python
python3 -m lose -v
```

## 0.6.2v
file name typo

minor changes

## 0.6.1v
readme for pypi.org changed

minor non code related changes

## 0.6v
`LOSE.generator()` and `LOSE.makeGenerator()` got a new optional keyword argument, `mask_callback`, which accepts a function, `None` disables the mask, refer to the [readme](README.md/#generator-details) for examples

`LOSE.newGroup()` now doesn't need a zeros before the shape of the group

`batch_obj` keyword argument in `LOSE.load()` now accepts any slice object or slice like string

minor changes

## 0.5.1v
typo related bug fix from 0.4.5v

## 0.5v
added `LOSE.renameGroup()`

`LOSE.batch_obj` moved from class vars to `LOSE.load()` as a keyword argument

minor non performance/syntax related changes

## 0.4.6v
typo related bug fix

## 0.4.5v
added `LOSE.removeGroup()`

`LOSE.fmode` moved from class vars to `LOSE.newGroup()` as a keyword argument

`LOSE.get_shape()` renamed to `LOSE.getShape()`

`LOSE.make_generator()` renamed to `LOSE.makeGenerator()`

`LOSE.save()` now only works in append mode

## 0.4.4v
typo

non performance/syntax related changes

## 0.4.3v
added `LOSE.make_generator()`

## 0.4.2v
improved shuffling in `LOSE.generator()`

## 0.4.1v
typo

## 0.4v
changed syntax for `LOSE.generator()` usage

## 0.3.2v
bug fix

## 0.3.1v
docs updated

## 0.3v
performance upgrade for `LOSE.generator()`

## 0.1.1v-0.2v
added shuffling for `LOSE.generator()`

typos

## 0.1v

initial commit