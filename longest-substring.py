#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse

def parse_arguments():
  parser = argparse.ArgumentParser(description="A tool to find the longest substring wihtin 2 files")
  parser.add_argument("-f1", "--file1", help="First input file to search", type=argparse.FileType('r'), required=True)
  parser.add_argument("-f2", "--file2", help="Second input file to search", type=argparse.FileType('r'), required=True)
  return parser

def longest_common_substring(s1, s2):
  m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
  longest, x_longest = 0, 0
  for x in xrange(1, 1 + len(s1)):
    for y in xrange(1, 1 + len(s2)):
      if s1[x - 1] == s2[y - 1]:
        m[x][y] = m[x - 1][y - 1] + 1
        if m[x][y] > longest:
          longest = m[x][y]
          x_longest = x
      else:
        m[x][y] = 0
  return s1[x_longest - longest: x_longest], x_longest - longest

if __name__ == "__main__":
  parser = parse_arguments()
  args = parser.parse_args()

  s1 = args.file1.read()
  args.file1.close()
  s2 = args.file2.read()
  args.file2.close()

  match, index = longest_common_substring(s1, s2)
  if match == "":
    print("No longest match found!")
    exit(1)
  else:
    print("%d: %s" % (index, match))
    exit(0)
