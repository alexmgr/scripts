#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import with_statement
import argparse
import binascii
import io
import sys

def parse_arguments():

  def str_repr(str_):
    if str_.startswith("0x"):
      # Only preserve hex portion
      return str_[2:]
    if str_.startswith("\\x"):
      # Transform "\x41\x03" to a hex string 4103
      return "".join([str_[i:i+2] for i in range(0, len(str_), 2) if str_[i:i+2] != "\\x"])
    if len(str_) == 1:
      return hex(ord(str_))[2:]
    raise argparse.ArgumentTypeError("Invalid value. Must be either hex value (i.e: 0x12abcd), a hex formatted string (i.e: \\x12\\xef) or a single char (i.e: 'A')")

  def positive_int(int_):
    try:
      positive_int = abs(int(int_))
    except:
      raise argparse.ArgumentTypeError("Invalid value. Must be a positive number, got [%s]" % int_)
    return positive_int
 
  parser = argparse.ArgumentParser(description="A tool to perform an xor against the content of a file")
  parser.add_argument("filename", help="The filename against which to perform the xor, or stdin", type=str, default='-', nargs='?')
  parser.add_argument("-x", "--xor", help="The hex value to xor against the file", type=str_repr, required=True)
  parser.add_argument("-b", "--bin", help="Output the xor stream as binary instead of hex. Default is False", action="store_true")
  parser.add_argument("-o", "--offset", help="Offset at which to start xoring. Default 0", type=positive_int, default=0)
  return parser

def to_data_len(pad, len_):
  if (len_ < 0):
    raise ValueError("Pad length must be positive")
  pad_len = len(pad)
  if len_ < pad_len:
    pad_aligned = pad[:len_]
  elif len_ > pad_len:
    pad_aligned = pad*(len_ // pad_len) + pad[:len_ % pad_len]
  else:
    pad_aligned = pad
  return pad_aligned
  
def xor_stream(stream, pad, offset=0):
  data = stream.read()
  pad_bin = binascii.unhexlify(pad)
  # Prepend with zeros to match starting offset
  pad_bin = "\x00"*offset + pad_bin
  # Repeat the pad to match data length if needed
  pad_aligned = to_data_len(pad_bin, len(data))
  # xor each single byte together
  return "".join(map(lambda x, y: chr(ord(x) ^ ord(y)), data, pad_aligned))
 
if __name__ == "__main__":
  parser = parse_arguments()
  args = parser.parse_args()

  if args.filename != '-':
    stream = open(args.filename, "rb")
  else:
    #stream = io.open(sys.stdin.fileno())
    stream = sys.stdin

  try:
    xored_stream = xor_stream(stream, args.xor, args.offset)
    if (args.bin):
      sys.stdout.write(xored_stream)
    else:
      print(binascii.hexlify(xored_stream))
  except (binascii.Error, TypeError) as be:
    print("Invalid hex string: %s" % be, file=sys.stderr)
    exit(1)

  if stream is not None:
    stream.close()
  exit(0)
