import json

import falcon
from falcon_ask import dispatch_request, FalconAskMiddleware, respond


def intent_fn(body):
    # "body" contains request POST data.
    return 'Congratulations! Your new alexa skill works great.'


class JarvisResource(object):
    # Dictionary mapping of "IntentRequest" to function.
    intent_maps = {
        'GreetingIntent': intent_fn,
    }

    # Message to return when "LaunchRequest" is received.
    welcome = 'Hi, welcome to your new alexa skill.'

    def on_post(self, req, resp):
        response = dispatch_request(req)
        resp.body = json.dumps(respond(response, end_session=False))


app = falcon.API(middleware=[
    # Do validation of request certificate and timestamp.
    FalconAskMiddleware(JarvisResource, validate=True),
])
app.add_route('/', JarvisResource())
