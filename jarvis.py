import json

import falcon
from falcon_ask import dispatch_request, FalconAskMiddleware, respond, util


def deploy_fn(body):
    response = None
    end_session = False
    directives = [{'type': 'Dialog.Delegate'}]

    req = body.get('request', {})
    dialog_state = req.get('dialogState')
    intent_status = req.get('intent', {}).get('confirmationStatus')

    if dialog_state == 'COMPLETED':
        directives = []
        end_session = True
        response = 'OK! You can ask me to deploy your app again sometime.'
        if intent_status == 'CONFIRMED':
            response = "Yeehaw! You're app is now being deployed."

    return respond(response, end_session=end_session, directives=directives)


def unknown_fn(body):
    return respond(
        "You've found something I don't know yet. Try asking again sometime.",
        end_session=True
    )


class JarvisResource(object):
    intent_maps = {
        'DeployIntent': deploy_fn,
        'UnknownIntent': unknown_fn,
    }

    welcome = respond(
        "Howdy! I'm Jarvis, I can help you deploy your app.",
        end_session=False,
    )

    def on_post(self, req, resp):
        response = dispatch_request(req)
        resp.body = json.dumps(response)


app = falcon.API(middleware=[
    FalconAskMiddleware(JarvisResource, validate=True),
])
app.add_route('/', JarvisResource())
