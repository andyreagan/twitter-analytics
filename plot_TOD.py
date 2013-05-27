#!/usr/bin/python
#
# plot times of day that I've tweeted
#
# written by Andy Reagan

def dater(year_month_day_list):
  # INPUTS: year as an integer, month as 3 letter string, day as an integer IN A LIST
  #
  # OUTPUT: number of days since July 15, 2006

  # a whole lot of constants to work with dates
  [year,month,day]=year_month_day_list
  days_in_month=[0,31,28,31,30,31,30,31,31,30,31,30,31]
  days_in_month_leap=[0,31,29,31,30,31,30,31,31,30,31,30,31]
  leap_years=[2008,2012] # of concern
  month_names=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  year_len=[0,169,365,366,365,365,365,365,366,365,365,365,365]
  i=0
  # search through the months to find a match
  for month_name in month_names:
    if month_name == month:
      # month has been found, figure out how many days passed
      if year in leap_years:
        ytd=sum(days_in_month_leap[0:i+1])
      else:
        ytd=sum(days_in_month[0:i+1])
    i+=1
  ytd+=day
  years_passed=year-2006+1
  date=ytd+sum(year_len[0:years_passed])
  if year == 2006:
    date+= -196
  return date

def timer(time):
  time_zone = -5.
  tmp = (time[0]+time[1]/60.+time[2]/3600.+time_zone) % 24
  return tmp

def readinput(json_files):
  # load the json module
  import simplejson as json
  
  times=[]
  dates=[]
  for filename in json_files:
    # print filename
    # load the first file
    tmp_file = open(filename)
    tmp_file.seek(32,0) # skip the first line
    tmp_buffer = tmp_file.read()
    # import the json into a list
    tweets = json.loads(tmp_buffer)
    # first day of twitter: July 15, 2006
    year_month_day=[[int(tweets[i]['created_at'].split()[5]),tweets[i]['created_at'].split()[1],int(tweets[i]['created_at'].split()[2])] for i in range(len(tweets))]
    time = [map(float,tweets[i]['created_at'].split()[3].split(':')) for i in range(len(tweets))]
    times.extend(map(timer,time))
    dates.extend(map(dater,year_month_day))
  return dates,times

def plotscatter(dates,times,picname):
  import matplotlib.pyplot as plt
  plt.scatter(dates,times)
  plt.xlabel('Days since twitter began (July 15, 2006)')
  plt.ylabel('Hours of the day')
  buffer = 50
  plt.xlim([min(dates)-buffer,max(dates)+buffer])
  plt.ylim([0,24])
#  plt.title("@andyreagan's tweetage by time of day")
#  plt.xticks((1266,1631,1996,2362),('2010','2011','2012','2013'))
  plt.savefig(picname)

def main():
  # run this in the level above the username, pass it the username

  import sys

  username = sys.argv[1]
  dataroot = username + '/data/js/tweets/'
  
  # load all the files in their tweet directory
  import subprocess
  json_files = [dataroot + tmp for tmp in  subprocess.Popen(['ls',dataroot],stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0].rstrip().split('\n')]

  # parse the tweets into just dates and times  
  dates,times = readinput(json_files)
  print 'there are ' + str(len(dates)) + ' tweets'

  # plot it with matplotlib
  plotscatter(dates,times,username.split('/')[-1] + '.png')
  print 'picture saved to ' + username.split('/')[-1] + '.png'

if __name__ == '__main__':
  main()
