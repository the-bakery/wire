#!/usr/bin/python2

import os
import shutil
import subprocess
import sys
import tempfile


def main():

  pipes = {}

  while True:
    try:
      line = raw_input()
      command = process_line(line, sys.argv, pipes)
    except EOFError:
      break

  # delete temp dirs
  for name in pipes:
    path = pipes[name]
    shutil.rmtree( path[:-4] )    


def process_line(line, args, pipes):
  tokens = line.split()

  command = []
  for token in tokens:
    first = token[0]
    name = token[1:]
    if first == '@':
      if name not in pipes:
	pipes[name] = new_pipe()
      command.append( pipes[name] )
    elif first == '$':
      try:
        index = int(name)
        command.append( args[index] )
      except Exception:
        command.append(token)
    else:
        command.append(token)

  spawn(command)


def new_pipe():
  dir = tempfile.mkdtemp()
  path = os.path.join(dir, 'pipe')
  os.mkfifo(path)
  return path


def spawn(command):
  # print ' '.join(command)
  try:
    if os.fork() == 0:
      subprocess.call(command)
      sys.exit(0)
  except OSError as error:
    print error

 
if __name__=='__main__':
  main()
 
