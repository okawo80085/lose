import unittest as u
import os
from lose import LOSE
import numpy as np

class Tests(u.TestCase):
	def test_mk_group_write(self):
		if os.path.isfile('./temp.h5'):
			os.unlink('./temp.h5')

		l = LOSE('./temp.h5')
		check = True
		E = None

		try:
			l.newGroup(fmode='w', x=(15, 5), y=(2,))

		except Exception as e:
			check = False
			E = 'error was raised: ' + repr(e)

		finally:
			if os.path.isfile('./temp.h5'):
				os.unlink('./temp.h5')

		self.assertTrue(check, E)

	def test_mk_group_append(self):
		if os.path.isfile('./temp.h5'):
			os.unlink('./temp.h5')

		l = LOSE('./temp.h5')
		check = True
		E = None

		try:
			l.newGroup(fmode='a', y=(2,))
			l.newGroup(fmode='a', x=(15, 5))

		except Exception as e:
			check = False
			E = 'error was raised: ' + repr(e)

		finally:
			if os.path.isfile('./temp.h5'):
				os.unlink('./temp.h5')

		self.assertTrue(check, E)

	def test_mk_group_badmode(self):
		if os.path.isfile('./temp.h5'):
			os.unlink('./temp.h5')

		l = LOSE('./temp.h5')
		check = True
		E = None

		try:
			l.newGroup(fmode='t', y=(2,))

		except ValueError as e:
			check = False
			E = 'error was raised: ' + repr(e)

		finally:
			if os.path.isfile('./temp.h5'):
				os.unlink('./temp.h5')

		self.assertFalse(check, E)

	def test_save_valid(self):
		if os.path.isfile('./temp.h5'):
			os.unlink('./temp.h5')

		l = LOSE('./temp.h5')
		check = True
		E = None

		l.newGroup(fmode='w', x=(25, 4), y=(2,))

		try:
			l.save(x=np.zeros((10, 25, 4)), y=np.zeros((2, 2)))
			l.save(x=np.zeros((15, 25, 4)), y=np.zeros((5, 2)))
			l.save(x=np.zeros((50, 25, 4)), y=np.zeros((8, 2)))

		except Exception as e:
			check = False
			E = 'error was raised: ' + repr(e)

		finally:
			if os.path.isfile('./temp.h5'):
				os.unlink('./temp.h5')

		self.assertTrue(check, E)

	def test_save_invalid1(self):
		if os.path.isfile('./temp.h5'):
			os.unlink('./temp.h5')

		l = LOSE('./temp.h5')
		check = True
		E = None

		l.newGroup(fmode='w', x=(25, 4), y=(2,))

		try:
			l.save(x=np.zeros((25, 4)), y=np.zeros((2, 2)))

		except ValueError as e:
			check = False
			E = 'error was raised: ' + repr(e)

		finally:
			if os.path.isfile('./temp.h5'):
				os.unlink('./temp.h5')

		self.assertFalse(check, E)

	def test_save_invalid2(self):
		if os.path.isfile('./temp.h5'):
			os.unlink('./temp.h5')

		l = LOSE('./temp.h5')
		check = True
		E = None

		l.newGroup(fmode='w', x=(25, 4), y=(2,))

		try:
			l.save(x=np.zeros((10, 25, 4)), y=np.zeros((2, 5)))

		except ValueError as e:
			check = False
			E = 'error was raised: ' + repr(e)

		finally:
			if os.path.isfile('./temp.h5'):
				os.unlink('./temp.h5')

		self.assertFalse(check, E)

	def test_save_invalid3(self):
		if os.path.isfile('./temp.h5'):
			os.unlink('./temp.h5')

		l = LOSE('./temp.h5')
		check = True
		E = None

		l.newGroup(fmode='w', x=(25, 4), y=(2,))

		try:
			l.save(x='lul')

		except TypeError as e:
			check = False
			E = 'error was raised: ' + repr(e)

		finally:
			if os.path.isfile('./temp.h5'):
				os.unlink('./temp.h5')

		self.assertFalse(check, E)


	def test_oof(self):
		self.assertTrue(True, 'oof')

if __name__ == '__main__':
	u.main()
