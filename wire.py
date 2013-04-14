#!/usr/bin/python2

import os
import shutil
import subprocess
import sys
import tempfile


def main():

  pipes = {}
  commands = []

  # preprocess commands
  while True:
    try:
      line = raw_input()
      command = preprocess(line, sys.argv, pipes)
      commands.append(command)
    except EOFError:
      break

  # execute commands
  for command in commands:
    spawn(command)

  # delete temp dirs
  for name in pipes:
    path = pipes[name]
    shutil.rmtree( path[:-4] )    


def preprocess(line, args, pipes):
  command = []
  for token in line.split():
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
  return command


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
 
