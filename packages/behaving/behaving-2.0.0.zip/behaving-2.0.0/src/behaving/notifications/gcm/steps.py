from behave import step
from behaving.personas.persona import persona_vars
import ast
import json

try:
    from urllib2 import Request, urlopen, HTTPError
except ImportError:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError


def extract(dict_in, dict_out):
    for key, value in dict_in.items():
        if isinstance(value, dict):
            extract(value, dict_out)
        else:
            dict_out[key] = value
    return dict_out


def match(data, query):
    for key, value in query.items():
        if key not in data or data[key] != value:
            return False
    return True


@step(u'I should receive a gcm notification at "{device_id}" containing "{message}"')
@persona_vars
def should_receive_gcm_with_message(context, device_id, message):
    query = ast.literal_eval(message)
    q_items = extract(query, {})
    notifications = context.gcm.user_messages(device_id)
    for notification in notifications:
        data = json.loads(notification)
        d_items = extract(data, {})
        if match(d_items, q_items):
            return
    assert False, "Message not Found"


@step(u'I should not have received any gcm notifications at "{device_id}"')
@persona_vars
def should_not_have_received_gcm(context, device_id):
    notifications = context.gcm.user_messages(device_id)
    assert len(notifications) == 0, "Have received notifications"


@step('I send a gcm message "{message}"')
def send_gcm_notification(context, message):

    url = "http://localhost:8200"
    req = Request(url, message.encode("utf-8"))

    try:
        urlopen(req)
    except (HTTPError,):
        assert False, u"Unable to send gcm message"
