#!/usr/bin/python
#
# going to parse my own twitter data into usable format
#
# written by Andy Reagan

def latlonparse(json_files):
  import json
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
  return [lat,lon]

def plotmap(lat,lon,picname):
  import matplotlib.pyplot as plt
  plt.scatter(lat,lon)

  plt.savefig(picname)

def main():
  import sys
  username = sys.argv[1]
  dataroot = username + '/data/js/tweets/'

  # load all the files in their tweet directory                                                       
  import subprocess
  json_files = [dataroot + tmp for tmp in  subprocess.Popen(['ls',dataroot],stdout = subprocess.PIPE,stderr = subprocess.STDOUT).communicate()[0].rstrip().split('\n')]

  lat,lon = latlonparse(json_files)
  print 'there were ' + str(len(lat)) + ' geo tagged tweets'  

  plotmap(lat,lon,username.split('/')[-1] + '-geo' + '.png')
  print 'picture saved to ' + username.split('/')[-1] + '-geo' + '.png'

if __name__ == '__main__':
  main()


