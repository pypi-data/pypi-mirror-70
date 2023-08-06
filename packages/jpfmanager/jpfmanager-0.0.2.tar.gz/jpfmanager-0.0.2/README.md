You can use jpf manager to help in saving / getting objects to / from file using either json or pickle 
------------------------------------------------------------------------------------------------------
Exemple:

file test_jpf.py:
-----------------

from pathlib import Path
from jpfmanager.jpf import FileManager
from toti_class import toti


if __name__ == "__main__":
    x = toti(5,6)
    pathi = str((Path(__file__).parent / 'test1.tst').absolute())
    FileManager.save(x,pathi)
    newX = FileManager.get(pathi)
    print(newX)

------------------------------------------------------------------

File toti_class.py
------------------
class toti(object):
    def __init__(self, val1, val2):
        self.Val1 = val1
        self.Val2 = val2
-----------------------------------

FileManager.save(object, path, method = None)
    Args:
        path: provide a string path to where the file will be saved
        object: provide the object you want to save in that file
        method: save using either json or pickle, json is set by default
    Returns:
        bool representing if the save operation succedded

FileManager.get(path, method = None):       
    Args:
        path: provide a string path to where the file is saved           
        method: save using either json or pickle, json is set by default
    Returns:
        False if the path is not correct or it is not a file path
        the content txt file in case of using json method and object in case of using the pickle method
[json pickle file manager repo](https://github.com/IbrahimABBAS85/jpf)