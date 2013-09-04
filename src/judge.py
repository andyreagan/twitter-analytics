#!/usr/bin/python

# judge the happiness of tweets

def readLabMT(stopval):
  # read the labMT dataset into a dict, of the stopval
  fname = 'src/labMT1_' + stopval + '.txt'
  f = open(fname,'r')
  tmp = dict([(line.split('\t')[0],[x.rstrip() for x in line.split('\t')[1:]]) for line in f])
  return tmp

