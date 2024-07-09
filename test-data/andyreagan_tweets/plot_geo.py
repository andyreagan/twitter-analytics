#!/usr/bin/python
#
# going to parse my own twitter data into usable format
#
# written by Andy Reagan

# load the json module
import simplejson as json

json_files = ['data/js/tweets/' + line.rstrip('\n') for line in open('files.txt')]
#print json_files

lat=[]
lon=[]
for filename in json_files:
  # print filename
  # load the first file
  tmp_file = open(filename)
  tmp_file.seek(32,0)
  tmp_buffer = tmp_file.read()
  # import the json into a list
  tweets = json.loads(tmp_buffer)
  for i in range(len(tweets)):
    if tweets[i]['geo']:
      if tweets[i]['geo']['coordinates']:
        lon.extend([float(tweets[i]['geo']['coordinates'][0])])
        lat.extend([float(tweets[i]['geo']['coordinates'][1])])

import matplotlib.pyplot as plt
plt.scatter(lat,lon)
plt.savefig('Tweets_by_space_andyreagan.png')
