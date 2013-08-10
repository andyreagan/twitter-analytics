# Create your views here.

# example/simple/views.py

from django.http import HttpResponse
from authomatic import Authomatic
from authomatic.adapters import DjangoAdapter

from config import CONFIG

authomatic = Authomatic(CONFIG, 'supersecretnonrandomstring')

def home(request):
    return HttpResponse('''
        Login with <a href="login/fb">Facebook</a>.<br />
        Login with <a href="login/tw">Twitter</a>.<br />
    ''')

def login(request, provider_name):
    response = HttpResponse()
    
    result = authomatic.login(DjangoAdapter(request,response), provider_name)
    
    if result:
        response.write('<a href="..">Home</a>')

        if result.error:
            response.write('<h2>Damn that error: {}</h2>'.format(result.error.message))
        elif result.user:
            if not (result.user.name and result.user.id):
                result.user.update()

            response.write('<h1>Hi {}</h1>'.format(result.user.name))
            response.write('<h2>Your id is: {}</h2>'.format(result.user.id))
            response.write('<h2>Your email is: {}</h2>'.format(result.user.email))

            if result.user.credentials:
                if result.provider.name == 'fb':
                    response.write('You are now logged in with Evilbook.<br >')
                    url = 'https://graph.facebook.com/{}?fields=feed.limit(5)'
                    url = url.format(result.user.id)

                    access_response = result.provider.access(url)

                    if access_response.status == 200:
                        # parse
                        statuses = access_response.data.get('feed').get('data')
                        error = access_response.data.get('error')

                        if error:
                            response.write('Damn that error: {}!'.format(error))
                        elif statuses:
                            response.write('Your 5 most recent statuses:<br />')
                            for message in statuses:
                                text = message.get('message')
                                date = message.get('created_time')
                                response.write('<h3>{}</h3>'.format(text))
                                response.write('Posted on: {}'.format(date))
                    else:
                        response.write('Damn that unknown error!<br />')
                        response.write('Status: {}'.format(response.status))

                if result.provider.name == 'tw':
                    response.write('You are now logged in with Twitter.<br />')
                    # we will get the 5 most recent statuses
                    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
                    
                    # you can pass a dictionary of querystring parameters
                    access_response = result.provider.access(url, {'count': 5})

                    # parse response
                    if access_response.status == 200:
                        if type(access_response.data) is list:
                            response.write('Your five most recent tweets:')
                            for tweet in access_response.data:
                                text = tweet.get('text')
                                date = tweet.get('created_at')

                                response.write('<h3>{}</h3>'.format(text))
                                response.write('Tweeted on: {}'.format(date))
                        elif response.data.get('errors'):
                            response.write('Damn that error: {}!'.format(response.data.get('errors')))
                    else:
                        response.write('Damn that unknown error!<br />')
                        response.write('Status: {}'.format(response.status))

    return response
                
                        
