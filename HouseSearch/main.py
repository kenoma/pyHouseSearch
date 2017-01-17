import os
from time import localtime, strftime
import cian

class ObjDummy:
	pass

print('Started on')
print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
print('----------------------------')


env = ObjDummy()
env.dataDir = '%s\\data\\'%os.path.dirname(os.path.realpath(__file__))
env.imgOutput = '%s\\data\\imgs\\'%os.path.dirname(os.path.realpath(__file__))

cian.GoGrab(env, 1, False)

print('----------------------------')
print('Completed on')
print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
