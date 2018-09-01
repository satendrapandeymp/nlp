from glob import glob
import os, shutil

def clearAll():
    shutil.rmtree("Results")
    shutil.rmtree("Tutorials")

if __name__ == "__main__":
    clearAll()
