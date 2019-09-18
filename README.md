# lose

lose, but in particular `lose.LOSE()`, is a helper class for handling data using `hdf5` file format and `PyTables`

```python
>>> from lose import LOSE
>>> l = LOSE()
>>> l
<hdf5 data handler, fname=None, fmode='r', atom=Float32Atom(shape=(), dflt=0.0)>
generator parameters: iterItems=None, iterOutput=None, batch_size=1, limit=None, loopforever=False, shuffle=False

```

## installation
```python
pip3 install -U lose
```
or
```python
pip install -U lose
```

## structure
#### vars
`LOSE.fname` is the path to  to the `.h5` file including the name and extension, default is `None`.

`LOSE.fmode` is the mode `.h5` file from `LOSE.fname` will be opened with, `'r'` for read(default), `'w'` for write, `'a'` for append.

`LOSE.atom` recommended to be left at default, is the `dtype` for the data to be stored in, default is `tables.Float32Atom()` which results to arrays with `dtype==np.float32`.

`LOSE.batch_obj` default is `'[:]'`, recommended to be left default, specifies the amount of data to be loaded by `LOSE.load()`, works like python list slicing, must be a string, default loads everything.

**`LOSE.generator()` related vars:**

`LOSE.batch_size` batch size of data getting pulled from the `.h5` file, default is `1`.

`LOSE.limit` limits the amount of data loaded by the generator, default is `None`, if `None` all available data will be loaded. 

`LOSE.loopforever` bool that allows infinite looping over the data, default is `False`.

`LOSE.iterItems` list of X group names and list of Y group names, default is `None`, required to be user defined for `LOSE.generator()` to work.

`LOSE.iterOutput` list of X output names and list of Y output names, default is `None`, required to be user defined for `LOSE.generator()` to work.

`LOSE.shuffle` bool that enables shuffling of the data, default is `False`, shuffling is affected by `LOSE.limit` and `LOSE.batch_size`.

#### methods
```
Help on class LOSE in module lose.dataHandler:

class LOSE(builtins.object)
 |  Methods defined here:
 |  
 |  __init__(self)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  __repr__(self)
 |      Return repr(self).
 |  
 |  generator(self)
 |  
 |  get_shape(self, arrName)
 |  
 |  load(self, *args)
 |  
 |  make_generator(self, layerNames, limit=None, batch_size=1, shuffle=False, **kwards)
 |  
 |  newGroup(self, **kwards)
 |  
 |  save(self, **kwards)
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 ```

`LOSE.newGroup(**groupNames)` is used to add/set(depends on the file mode) group(expandable array) names and shapes in the `.h5` file.


`LOSE.save(**groupNamesAndSahpes)` is used to save data in write/append mode(depends on the file mode) into a group into a `.h5` file, the data needs to have the same shape as `group.shape[1:]` the data was passed to, `LOSE.get_shape(groupName)` can be used to get the `group.shape` of a group.


`LOSE.load(*groupNames)` is used to load data(hole group or a slice, to load a slice change `LOSE.batch_obj` to a string with the desired slice, default is `"[:]"`) from a group, group has to be present in the `.h5` file.


`LOSE.get_shape(groupName)` is used to get the shape of a single group, group has to be present in the `.h5` file.


`LOSE.generator()` check `LOSE.generator() details` section, `LOSE.iterItems` and `LOSE.iterOutput` have to be defined.


`LOSE.make_generator(layerNames, limit=None, batch_size=1, shuffle=False, **kwards)` again check `LOSE.generator() details` more details.

## example usage

##### creating/adding new groups to a file in append/write mode
```python
import numpy as np
from lose import LOSE

l = LOSE()
l.fname = 'path/to/you/save/file.h5' # path to the .h5 file, has to be user defined before any methods can be used, default is None
l.fmode = 'w' # 'w' for write mode, 'a' for append mode, default is 'r'

exampleDataX = np.arange(20, dtype=np.float32)
exampleDataY = np.arange(3, dtype=np.float32)

l.newGroup(x=(0, *exampleDataX.shape), y=(0, *exampleDataY.shape)) # creating new groups(ready for data saved to) in a file, if fmode is 'w' all groups in the file will be overwritten
```
##### saving data into a group in append/write mode
```python
import numpy as np
from lose import LOSE

l = LOSE()
l.fname = 'path/to/you/save/file.h5' # path to the .h5 file, has to be user defined before any methods can be used, default is None
l.fmode = 'a' # 'w' for write mode, 'a' for append mode, default is 'r', 'a' mode append data to the file, 'w' mode overwrites data for the group in the file

exampleDataX = np.arange(20, dtype=np.float32)
exampleDataY = np.arange(3, dtype=np.float32)

l.save(x=[exampleDataX, exampleDataX], y=[exampleDataY, exampleDataY]) # saving data into groups defined in the previous example, in append mode
l.save(y=[exampleDataY], x=[exampleDataX]) # the same thing
```
##### loading data from a group within a file
```python
import numpy as np
from lose import LOSE

l = LOSE()
l.fname = 'path/to/you/save/file.h5' # path to the .h5 file, has to be user defined before any methods can be used, default is None

x, y = l.load('x', 'y') # loading data from the .h5 file(has to be a real file) populated by previous examples
y2compare, x2compare = l.load('y', 'x') # the same thing

print (np.all(x == x2compare), np.all(y == y2compare)) # True True
```
##### getting the shape of a group
```python
import numpy as np
from lose import LOSE

l = LOSE()
l.fname = 'path/to/you/save/file.h5' # path to the .h5 file(populated by previous examples), has to be user defined before any methods can be used, default is None

print (l.get_shape('x')) # (3, 20)
print (l.get_shape('y')) # (3, 3)
```
## `LOSE.generator()` details
`LOSE.generator()` is a python generator used to access data from a `hdf5` file in `LOSE.batch_size` pieces without loading the hole file/group into memory, also works with `tf.keras.model.fit_generator()`, __have__ to be used with a `with` context statement(see examples below).

`LOSE.iterItems` and `LOSE.iterOutput` __have__ to be defined by user first.


`LOSE.make_generator(layerNames, limit=None, batch_size=1, shuffle=False, **kwards)` has the same rules as `LOSE.generator()`. however the data needs to be passed to it each time it's initialized, data is only stored temporarily, the parameters are passed to it on initialization, `layerNames` acts like `LOSE.iterOutput` but every name in it has to match to names of the data passed(see examples below), if file `temp.h5` exists it will be overwritten and then deleted.

### example `LOSE.generator()` usage
for this example lets say that file has requested data in it and the model input/output layer names are present.
```python
import numpy as np
from lose import LOSE

l = LOSE()
l.fname = 'path/to/you/save/file.h5' # path to data

l.iterItems = [['x1', 'x2'], ['y']] # names of X and Y groups, all group names need to have batch dim the same and be present in the .h5 file
l.iterOutput = [['input_1', 'input_2'], ['dense_5']] # names of model's layers the data will be cast on, group.shape[1:] needs to match the layer's input shape
l.loopforever = True
l.batch_size = 20 # some batch size, can be bigger then the dataset, but won't output more data, it will just loop over or stop the iteration if LOSE.loopforever is False

l.limit = 10000 # lets say that the file has more data, but you only want to train on first 10000 samples

l.shuffle = True # enable data shuffling for the generator, costs memory and time

with l.generator() as gen:
	some_model.fit_generator(gen(), steps_per_epoch=50, epochs=1000, shuffle=False) # model.fit_generator() still can't shuffle the data, but LOSE.generator() can
```

### example `LOSE.make_generator(layerNames, limit=None, batch_size=1, shuffle=False, **kwards)` usage
for this example lets say the model's input/output layer names are present and shapes match with the data.
```python
import numpy as np
from lose import LOSE

l = LOSE()

num_samples = 1000

x1 = np.zeros((num_samples, 200)) #data for the model
x2 = np.zeros((num_samples, 150)) #data for the model
y = np.zeros((num_samples, 800)) #data for the model

with l.make_generator([['input_1', 'input_2'], ['dense_5']], batch_size=10, shuffle=True, input_2=x2, input_1=x1, dense_5=y) as gen:
	del x1 #remove from memory
	del x2 #remove from memory
	del y #remove from memory

	some_model.fit_generator(gen(), steps_per_epoch=100, epochs=10000, shuffle=False) # again data can't be shuffled by model.fit_generator(), shuffling should be done by the generator
```

# bugs/problems/issues
report them.