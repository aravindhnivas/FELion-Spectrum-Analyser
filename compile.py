#!/usr/bin/python3

import compileall
import os

my_path = os.getcwd()
compileall.compile_dir(my_path+'/modules/', force=True)