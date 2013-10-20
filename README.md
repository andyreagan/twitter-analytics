going to follow the tutorial on authomatic on
http://peterhudec.github.io/authomatic/examples/simple.html
code for this is at
https://github.com/peterhudec/authomatic/tree/master/examples/gae/simple

could try the more advanced tutorial on his page

he has a live version running on google app engine at
http://authomatic-example.appspot.com
with code at
https://github.com/peterhudec/authomatic/tree/master/examples/gae/showcase

google's webapp2 documentation is at
https://developers.google.com/appengine/docs/python/gettingstartedpython27/usingwebapp
i did this at some point, and had the hello world app going live

i then tried to get the django example on authomatic going, i think, but didn't get django to play nice with google's app engine
then it was all hopeless
i need to find out whether the zoo server supports wsgi for little python vacc app to work
the google app engine dashboard is at
https://appengine.google.com/dashboard?&app_id=s~computationalstorylabhedo

okay so I've got the thing working following the authomatic basic demo
no posting of tweets or anything yet

I think the next step is to make it look nice, and add the pictures
-> the pictures can be made in matplotlib, but that means I have to add it
-> also don't want to have to add numpy, that's too huge of a libarary

2013-10-20

Now I want to use this app to also save the user's authentication information, and we'll use it to hit the REST API to scrape the first two years of twitter.

I built a scraping app using python and the twython module.
I think that I would need to save the OAUTH_TOKEN{,_SECRET}.

Then I could use them again later? I would think so.
Would want to save them in some sort of database.

But really this whole thing is a data acquisition exercise.

IT'S NOT SCIENCE
and I also don't think it will get me a web design job.
I'm just printing text...!

It would be nice to be able to easily make matplotlib-like graphs in javascript...I wonder if there is some sort of thing.
I don't know javascript, so I'm probably not going to be the one to write it.
Jake is making the storyfinder stuff in R, and R does have a web framework...maybe it is easier to use than pythons!
Turns out...this is exactly what Shiny is.
Looks like you need to run your own server for it to work though.