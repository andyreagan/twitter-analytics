# config.py

from authomatic.providers import oauth1, oauth2

CONFIG = {

    'tw': { # internal providor name

        # provider class
        'class_': oauth1.Twitter,

        # also need
        'consumer_key': 'sfLrlFcocDtftJJLVK1ig',
        'consumer_secret': 'UiDGdG7vcscnPzpZz3lZrqOaK2xQHRlXlxnYQhJb2Qk',
        },

    'fb': {

        'class_': oauth2.Facebook,

        'consumer_key': '652937514718034',
        'consumer_secret': '5cdbec39750c89ebcb745d865d015174',
        }
}

