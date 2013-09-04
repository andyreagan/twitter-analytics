# main.py

import webapp2
from sys import path
path.append('python-modules/authomatic')
from authomatic import Authomatic
from authomatic.adapters import Webapp2Adapter
from config import CONFIG

# import my stuff
path.append('src')
from plot_TOD import timer,dater,happiness

# make instance of the Authomatic class and pass it the config, along with a random secret string
authomatic = Authomatic(config=CONFIG, secret='kajsdkjfhhihsdkfj23j4k23j')

# create request handler
# accept GET and POST http methods, recieve the provider_name URL variable
class Login(webapp2.RequestHandler):
    def any(self, provider_name):
        # log in the user by calling the Authomatic.login() method inside the handler
        # must pass it an adapter, and provider name
        result = authomatic.login(Webapp2Adapter(self), provider_name)
        
        # the login procedure is over when Authomatic.login() returns a Loginresult
        if result:
            self.response.write('<a href="..">Home</a>')
            if result.error:
                self.response.write('<h2>Damn that error: {}</h2>'.format(result.error.message))
            elif result.user:
                if not (result.user.name and result.user.id):
                    result.user.update()
                self.response.write('<h1>Hi {}</h1>'.format(result.user.name))
                self.response.write('<h2>Your id is: {}</h2>'.format(result.user.id))
                self.response.write('<h2>Your email is: {}</h2>'.format(result.user.email))
                # if we have credentials we can do more
                if result.user.credentials:
                    # if we're on FB
                    if result.user.name == 'fb':
                        self.response.write('You are logged in with FB.<br />')
                        url = 'https://graph.facebook.com/{}?fields=feed.limit(5)'
                        url = url.format(result.user.id)
                        response = result.provider.access(url)
                        if response.status == 200:
                            # parse response
                            statuses = response.data.get('feed').get('data')
                            error = response.data.get('error')
                            
                            if error:
                                self.response.write('Damn that error: {}'.format(error))
                            elif statuses:
                                self.response.write('Your 5 most recent statuses:<br />')
                                for message in statuses:
                                    
                                    text = message.get('message')
                                    date = message.get('created_time')

                                    self.response.write('<h3>{}</h3>'.format(text))
                                    self.response.write('Posted on: {}'.format(date))
                        else:
                            self.response.write('Damn that unknown error!<br />')
                            self.response.write('Status: {}'.format(response.status))
                    if result.provider.name == 'tw':
                        self.response.write('You are now logged in with Twitter.<br />')

                        # we'll get the 5 most recent tweets
                        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

                        # you can pass a dict of querystring parameters
                        response = result.provider.access(url, {'count': 5})

                        # parse response
                        if response.status == 200:
                            if type(response.data) is list:
                                # twitter returns tweets as a JSON list
                                self.response.write('Your 5 most recent tweets:')
                                
                                # begin working with the data and my stuff

                                # empty lists
                                times = []
                                dates = []
                                happs = []
                                alltext = ''

                                for tweet in response.data:
                                    text = tweet.get('text')
                                    date = tweet.get('created_at')
                                    
                                    # add the dates and times points to the lists
                                    #times.extend(timer(map(float,date.split()[3].split(':'))))
                                    #dates.extend(dater([int(date.split()[5]),date.split()[1],int(date.split()[2])]))
                                    #happs.extend(happiness(text)[0])

                                    alltext+=text

                                    self.response.write('<h3>{}</h3>'.format(text))
                                    self.response.write('Tweeted on: {}'.format(date))

                                av_happiness = happiness(alltext)[0]
                                # give some information back about that I just computed
                                self.response.write('<h3>Average happiness of your last 5 tweets was {}</h3>'.format(str(av_happiness)))

                            elif response.data.get('errors'):
                                self.response.write('Damn that error: {}!'.format(reponse.data.get('errors')))
                        else:
                            self.response.write('Damn that unknown error!<br />')
                            self.response.write('Status: {}'.format(response.status))

# so we don't have to write all of the URLs manually
class Home(webapp2.RequestHandler):
    def get(self):
        # create links to login handler
        self.response.write('Login with <a href="login/fb">Facebook</a>.<br />')
        self.response.write('Login with <a href="login/tw">Twitter</a>.<br />')

# create routes
ROUTES = [webapp2.Route(r'/login/<:.*>', Login, handler_method='any'),
          webapp2.Route(r'/', Home)]

# instantiate the wsgi application
app = webapp2.WSGIApplication(ROUTES, debug=True)
