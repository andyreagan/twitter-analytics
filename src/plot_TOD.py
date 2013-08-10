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
  # convert a list [hour,minute,second] to a decimal hour in EST
  time_zone = -5.
  tmp = (time[0]+time[1]/60.+time[2]/3600.+time_zone) % 24
  return tmp

def readinput(json_files):
  # load the json module
  import simplejson as json
  from math import floor

  times=[]
  dates=[]
  # create bins for hours
  hour_count=[0 for i in range(24)] # bin the number
  hourly_text=['' for i in range(24)] # bin the text (long strings)
  for filename in json_files:
    # print filename
    # load the first file
    tmp_file = open(filename)
    tmp_file.seek(32,0) # skip the first line
    tmp_buffer = tmp_file.read()
    # import the json into a list
    tweets = json.loads(tmp_buffer)
    # first day of twitter: July 15, 2006
    # next line grabs [year, month, day] for each tweet
    year_month_day=[[int(tweets[i]['created_at'].split()[5]),tweets[i]['created_at'].split()[1],int(tweets[i]['created_at'].split()[2])] for i in range(len(tweets))]
    # next line graps the time in [float hr, float min, float sec] and combines that to a decimal hour (using timer)
    time = map(timer,[map(float,tweets[i]['created_at'].split()[3].split(':')) for i in range(len(tweets))])
    # next line grabs the text of each tweet
    texts = [tweets[i]['text'] for i in range(len(tweets))]
    times.extend(time)
    dates.extend(map(dater,year_month_day))
    for i in range(len(time)):
      hour_count[int(floor(time[i]))]+=1
      hourly_text[int(floor(time[i]))]+=texts[i]+'\n'
  
  return dates,times,textlist,hour_count,hourly_text

def plotscatter(dates,times,picname,hour_count):
  import matplotlib.pyplot as plt

  # create a figure, fig is now a matplotlib.figure.Figure instance
  fig = plt.figure()

  # plot the scatter
  ax1 = fig.add_axes([0.1,0.1,0.65,0.8]) #  [left, bottom, width, height]
  ax1.scatter(dates,times)
  ax1.set_xlabel('Days since twitter began (July 15, 2006)')
  ax1.set_ylabel('Hours of the day')
  buffer = 50
  ax1.set_xlim([min(dates)-buffer,max(dates)+buffer])
  ax1.set_ylim([0,24])
  ax1.set_title('Tweets by Time of Day')
#  plt.xticks((1266,1631,1996,2362),('2010','2011','2012','2013'))

  # now plot the histogram
  ax2 =  fig.add_axes([0.75,0.1,0.2,0.8])
  ax2.set_frame_on(False)
  ax2.set_yticks([])
  ax2.set_xticks([])
  ax2.barh(range(24),hour_count,color='b',height=1.0)
  ax2.set_ylim([0,24])

  plt.savefig(picname)
  
def happiness(tmpstr):
  from judge import readLabMT
  LabMT = readLabMT('000') # now LabMT is the dataset as a dict
#  print LabMT['laughter'][1] # verify it loaded correctly, should print 8.5
  score_list = []
  # build a list of words, splitting by almost everything, and stripping almost everything
  words = [x.lower().lstrip("?';:.$%&()\\!*[]{}|\"<>,^-_=+").rstrip("@#?';:.$%&()\\!*[]{}|\"<>,^-_=+") for x in tmpstr.split()]
  for word in words:
    if word in LabMT:
      score_list.append(float(LabMT[word][1]))
#  print score_list
  from numpy import mean,std
  happs = mean(score_list)
  happs_std = std(score_list)
  return happs,happs_std

def plothapps(happs,happs_std,picname):
  import matplotlib.pyplot as plt

  # create a figure, fig is now a matplotlib.figure.Figure instance
  fig = plt.figure()

  # plot the scatter
  ax1 = fig.add_axes([0.2,0.2,0.7,0.7]) #  [left, bottom, width, height]
  ax1.plot(range(24),happs)
  ax1.set_xlabel('Hours')
  ax1.set_ylabel('Happs')
#  ax1.set_xlim([min(dates)-buffer,max(dates)+buffer])
#  ax1.set_ylim([0,24])
  ax1.set_title('Happiness by hour of day')
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
  dates,times,texts,hour_count,hourly_text = readinput(json_files)
  print 'there are ' + str(len(dates)) + ' tweets'
  
  # plot it with matplotlib
  plotscatter(dates,times,username.split('/')[-1]+ '-TOD'  + '.png',hour_count)
  print 'picture saved to ' + username.split('/')[-1] + '-TOD' + '.png'
  
#  print 'dumping the hourly text from hour 00'
#  print hourly_text[0]
  
  # initialize the hourly happiness indices
  hourly_happs = [0 for i in range(24)]
  hourly_happs_std = [0 for i in range(24)]

  # compute the hourly happiness and std_dev
  print 'Here come happiness and standard deviation by hour'
  # at some point, i'll want to do shifts (gahh)
  for i in range(24):
    hourly_happs[i],hourly_happs_std[i] = happiness(hourly_text[i])
    print str(hourly_happs[i]) + ',' + str(hourly_happs_std[i])  

  plothapps(hourly_happs,hourly_happs_std,username.split('/')[-1]+ '-daily-happiness' + '.png')
  print 'Plotted hourly happiness to' + username.split('/')[-1]+ '-daily-happiness' + '.png'

if __name__ == '__main__':
  main()
