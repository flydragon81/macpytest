import os

file_path = "D:/test/testfile.py"
filepath, tempfilename = os.path.split(file_path)
filename, extension = os.path.splitext(file_path)
print(filepath, tempfilename, filename, extension)
print(os.path.splitext(file_path)[0] + '_output' + os.path.splitext(file_path)[1])
