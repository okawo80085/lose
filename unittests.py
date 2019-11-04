import unittest as u
import os
from lose import LOSE
import lose
import numpy as np

v = [int(i) for i in lose.__version__.split('.')]

class Tests(u.TestCase):
	def setUp(self):
		if os.path.isfile('./temp.h5'):
			os.unlink('./temp.h5')

		self.l = LOSE('./temp.h5')

	def test_mk_group_write(self):
		if os.path.isfile(self.l.fname):
			os.unlink(self.l.fname)

		self.l.newGroup(fmode='w', x=(15, 5), y=(2,))

	def test_mk_group_append(self):
		if os.path.isfile(self.l.fname):
			os.unlink(self.l.fname)

		self.l.newGroup(fmode='a', y=(2,))
		self.l.newGroup(fmode='a', x=(15, 5))

	def test_mk_group_invalid1(self):
		if os.path.isfile(self.l.fname):
			os.unlink(self.l.fname)

		with self.assertRaises(ValueError):
			self.l.newGroup(fmode='t', y=(2,))

	def test_save_valid(self):
		if os.path.isfile(self.l.fname):
			os.unlink(self.l.fname)

		check = True
		E = None

		self.l.newGroup(fmode='w', x=(25, 4), y=(2,))

		self.l.save(x=np.zeros((10, 25, 4)), y=np.zeros((2, 2)))
		self.l.save(x=np.zeros((15, 25, 4)), y=np.zeros((5, 2)))
		self.l.save(x=np.zeros((50, 25, 4)), y=np.zeros((8, 2)))

	def test_save_invalid1(self):
		if os.path.isfile(self.l.fname):
			os.unlink(self.l.fname)

		self.l.newGroup(fmode='w', x=(25, 4), y=(2,))

		with self.assertRaises(ValueError):
			self.l.save(x=np.zeros((25, 4)), y=np.zeros((2, 2)))

	def test_save_invalid2(self):
		if os.path.isfile(self.l.fname):
			os.unlink(self.l.fname)

		self.l.newGroup(fmode='w', x=(25, 4), y=(2,))

		with self.assertRaises(ValueError):
			self.l.save(x=np.zeros((10, 25, 4)), y=np.zeros((2, 5)))

	def test_save_invalid3(self):
		if os.path.isfile(self.l.fname):
			os.unlink(self.l.fname)

		self.l.newGroup(fmode='w', x=(25, 4), y=(2,))

		with self.assertRaises(TypeError):
			self.l.save(x='lul')

	def test_load_valid(self):
		if os.path.isfile(self.l.fname):
			os.unlink(self.l.fname)

		X = np.zeros((10, 5, 10))
		Y = np.zeros((10, 5))

		self.l.newGroup(fmode='w', x=X.shape[1:], y=Y.shape[1:])
		self.l.save(x=X, y=Y)

		a, b = self.l.load('x', 'y')

		self.assertEqual(np.all(a==X), np.all(b==Y), 'should be equal')

	@u.skipIf(v < [0, 6, 0], 'unsupported version')
	def test_load_valid2(self):
		if os.path.isfile(self.l.fname):
			os.unlink(self.l.fname)

		X = np.zeros((10, 5, 10))
		Y = np.zeros((10, 5))

		self.l.newGroup(fmode='w', x=X.shape[1:], y=Y.shape[1:])
		self.l.save(x=X, y=Y)

		a, b = self.l.load('x', 'y', batch_obj=':5')

		self.assertEqual(np.all(a==X[:5]), np.all(b==Y[:5]), 'should be equal')

	@u.skipIf(v > [0, 5, 0], 'version 0.5.0 and below only')
	def test_load_valid2_old(self):
		if os.path.isfile(self.l.fname):
			os.unlink(self.l.fname)

		X = np.zeros((10, 5, 10))
		Y = np.zeros((10, 5))

		self.l.newGroup(fmode='w', x=X.shape[1:], y=Y.shape[1:])
		self.l.save(x=X, y=Y)

		a, b = self.l.load('x', 'y', batch_obj='[:5]')

		self.assertEqual(np.all(a==X[:5]), np.all(b==Y[:5]), 'should be equal')

	def tearDown(self):
		if os.path.isfile(self.l.fname):
			os.unlink(self.l.fname)

if __name__ == '__main__':
	u.main()
