from glob import glob
import os, shutil

files = glob("Temp/*")

for file in files:
    os.remove(file)


