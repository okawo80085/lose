import numpy as np
import tables as t
import os
from contextlib import contextmanager


class LOSE:
	def __init__(self):
		self.fname = None
		self.fmode = 'r'
		self.atom = t.Float32Atom()

		self.batch_size = 1

		self.iterItems = None
		self.iterOutput = None
		self.loopforever = False
		self.limit = None
		self.shuffle = False

		self._a = []
		self._b = []

		self.batch_obj = '[:]'

	def __repr__(self):
		messsage = '<hdf5 data handler, fname={}, fmode=\'{}\', atom={}>'.format(self.fname, self.fmode, self.atom)
		messsage += '\ngenerator parameters: iterItems={}, iterOutput={}, batch_size={}, limit={}, loopforever={}, shuffle={}'.format(self.iterItems, self.iterOutput, self.batch_size, self.limit, self.loopforever, self.shuffle)
		if self.fname is not None:
			try:
				with t.open_file(self.fname, mode=self.fmode) as f:
					messsage += '\nhdf5 file structure: {}'.format(f.__repr__())

			except Exception as e:
				messsage += '\nfailed to open file at \'{}\':{}, make sure it\'s a not corrupted hdf5 file and is a real file'.format(self.fname, e)

		return messsage

	def newGroup(self, **kwards):
		with t.open_file(self.fname, mode=self.fmode) as f:
			for key, val in kwards.items():
				f.create_earray(f.root, key, self.atom, val)
				#print ([key], val)

			#print (f)

	def save(self, **kwards):
		with t.open_file(self.fname, mode=self.fmode) as f:
			for key, val in kwards.items():
				x = eval('f.root.{}'.format(key))
				x.append(val)

	def load(self, *args):
		out = []
		with t.open_file(self.fname, mode='r') as f:
			for key in args:
				x = eval('f.root.{}{}'.format(key, self.batch_obj))
				out.append(x)

		return *out

	def get_shape(self, arrName):
		with t.open_file(self.fname, mode='r') as f:
			return eval('f.root.{}.shape'.format(arrName))

	def _iterator_init(self):
		if self.iterItems is None or self.iterOutput is None or self.fname is None:
			raise ValueError('self.iterItems and/or self.iterOutput and/or self.fname is empty')

		if len(self.iterItems) != 2 or len(self.iterOutput) != 2:
			raise ValueError('self.iterItems or self.iterOutput has wrong dimensions, self.iterItems is [[list of x array names], [list of y array names]] and self.iterOutput is the name map for them')

		dataset_limit = self.get_shape(self.iterItems[0][0])[0]
		#print (dataset_limit)
		index = 0

		while 1:
			self._a.append(index)
			self._b.append(index+self.batch_size)

			index += self.batch_size

			if self.limit is not None:
				if index >= self.limit or index >= dataset_limit:
					break

			elif index >= dataset_limit:
				break

	def _iterator(self):
		if self.iterItems is None or self.iterOutput is None or self.fname is None:
			raise ValueError('self.iterItems and/or self.iterOutput and/or self.fname is empty')

		if len(self.iterItems) != 2 or len(self.iterOutput) != 2:
			raise ValueError('self.iterItems or self.iterOutput has wrong dimensions, self.iterItems is [[list of x array names], [list of y array names]] and self.iterOutput is the name map for them')

		if self.shuffle:
			np.random.seed(None)
			st = np.random.get_state()
			np.random.set_state(st)
			np.random.shuffle(self._a)
			np.random.set_state(st)
			np.random.shuffle(self._b)

		index = 0

		with t.open_file(self.fname, mode='r') as f:
			while 1:
				if self.shuffle:
					np.random.seed(None)
					st = np.random.get_state()

				stepX = {}
				stepY = {}
				for name, key in zip(self.iterItems[0], self.iterOutput[0]):
					x = eval('f.root.{}[{}:{}]'.format(name, self._a[index], self._b[index]))
					if self.shuffle:
						np.random.set_state(st)
						np.random.shuffle(x)

					stepX[key] = x

				for name, key in zip(self.iterItems[1], self.iterOutput[1]):
					y = eval('f.root.{}[{}:{}]'.format(name, self._a[index], self._b[index]))
					if self.shuffle:
						np.random.set_state(st)
						np.random.shuffle(y)

					stepY[key] = y

				yield (stepX, stepY)

				index += 1

				if index >= len(self._a):
					index = 0
					if self.loopforever != True:
						raise StopIteration

					elif self.shuffle:
						np.random.seed(None)
						st = np.random.get_state()
						np.random.set_state(st)
						np.random.shuffle(self._a)
						np.random.set_state(st)
						np.random.shuffle(self._b)

	@contextmanager
	def generator(self):
		try:
			self._iterator_init()
			gen = self._iterator

			yield gen

		except:
			raise

	@contextmanager
	def make_generator(self, layerNames, limit=None, batch_size=1, shuffle=False, **kwards):
		try:
			if os.path.isfile('./temp.h5'):
				os.unlink('./temp.h5')
			self.fname = 'temp.h5'
			self.fmode = 'a'
			self.iterItems = layerNames
			self.iterOutput = layerNames
			self.limit = limit
			self.batch_size = batch_size
			self.shuffle = shuffle

			d= {layerName: (0, *val.shape[1:]) for layerName, val in kwards.items()}

			self.newGroup(**d)
			self.save(**kwards)

			del d
			del kwards

			self.fmode = 'r'

			self._iterator_init()
			gen = self._iterator

			yield gen

		except:
			raise

		finally:
			os.unlink('./temp.h5')
