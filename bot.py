from webexteamssdk import WebexTeamsAPI, ApiError, Webhook
from creds import access_token, wehbook_host
import json

help_text = "Hello. I'm the Webhook Echo bot. I'm here to demonstrate what a message sent to a wehbook looks like." \
            "Just send me a message and I will echo back the webhook that I receive."


def post_message(message, space):
    try:
        # Initialize the webex teams API with our token
        wbxt_api = WebexTeamsAPI(access_token=access_token)

        message = wbxt_api.messages.create(roomId=space, markdown=message)
        return {'success': True,
                'messages': 'Successfully sent message {}'.format(message.id),
                'response': ''}

    except ApiError as e:
        # Return any API error that may have been raised
        return {'success': False,
                'messages': 'API Error encountered',
                'response': '{}'.format(e)}


def set_up_webhooks():
    try:
        memberships_found = False
        messages_found = False
        rooms_found = False
        attachment_actions_found = False

        target_url = wehbook_host + '/webhook'

        wbxt_api = WebexTeamsAPI(access_token=access_token)
        webhooks = wbxt_api.webhooks.list()
        for webhook in webhooks:
            if webhook.targetUrl != target_url:
                wbxt_api.webhooks.delete(webhook.id)
            else:
                if webhook.resource == 'memberships':
                    memberships_found = True
                elif webhook.resource == 'messages':
                    messages_found = True
                elif webhook.resource == 'rooms':
                    rooms_found = True
                elif webhook.resource == 'attachmentActions':
                    attachment_actions_found = True

        if not messages_found:
            result = wbxt_api.webhooks.create(name='Echo Bot Messages Webhook',
                                              targetUrl=target_url,
                                              resource='messages',
                                              event='created')
        if not memberships_found:
            result = wbxt_api.webhooks.create(name='Echo Bot Memberships Webhook',
                                              targetUrl=target_url,
                                              resource='memberships',
                                              event='created')
        if not rooms_found:
            result = wbxt_api.webhooks.create(name='Echo Bot Rooms Webhook',
                                              targetUrl=target_url,
                                              resource='rooms',
                                              event='created')
        if not attachment_actions_found:
            result = wbxt_api.webhooks.create(name='Echo Bot attachmentActions Webhook',
                                              targetUrl=target_url,
                                              resource='attachmentActions',
                                              event='created')

        result = True
    except Exception as e:
        print(e)
        result = False

    return result


def handle_webhook(request_data):
    try:
        wbxt_api = WebexTeamsAPI(access_token=access_token)

        print("\n")
        print("WEBHOOK POST RECEIVED:")
        print(request_data)
        print("\n")

        webhook_obj = Webhook(request_data)
        print(webhook_obj)

        me = wbxt_api.people.me()
        my_org = me.orgId
        print(me)

        if webhook_obj.resource == 'memberships':
            if webhook_obj.data.personId == me.id:
                room = wbxt_api.rooms.get(webhook_obj.data.roomId)                    # Get the room details
                post_message(help_text, room.id)
        elif webhook_obj.resource == 'messages':
            room = wbxt_api.rooms.get(webhook_obj.data.roomId)                    # Get the room details
            message = wbxt_api.messages.get(webhook_obj.data.id)                  # Get the message details
            person = wbxt_api.people.get(message.personId)                        # Get the sender's details

            print("NEW MESSAGE IN ROOM '{}'".format(room.title))
            print("FROM '{}'".format(person.displayName))
            print("MESSAGE '{}'\n".format(message.text))
            print(message)

            # if person.orgId == my_org: <--- Can filter on who is allowed to send here if necessary
            if True:
                if message.personId == me.id:
                    return 'OK'
                else:
                    request = message.text

                    if message.mentionedPeople is not None and me.id in message.mentionedPeople:
                        request = request.replace(me.displayName, '', 1)
                        if request == message.text:
                            request = request.replace(me.nickName, '', 1)

                    request = request.strip()

                    if request.lower() == 'help':
                        post_message(help_text, room.id)
                    elif "http://adaptivecards.io/schemas/adaptive-card.json" in request.lower():
                        post_message("Detected Card Data - Attempting to Render Card Below", room.id)
                        try:
                            card_json = json.loads(message.text)
                            wbxt_api.messages.create(
                                room.id,
                                text="Your Webex client cannot display this card",
                                attachments=[{
                                    "contentType": "application/vnd.microsoft.card.adaptive",
                                    "content": card_json
                                }]
                            )
                        except ValueError:
                            post_message("Invalid JSON detected", room.id)
                    else:
                        wbxt_api.messages.create(
                            room.id,
                            markdown=f"**New Webhook POST received. Payload:**\n"
                                     f"```\n{json.dumps(webhook_obj._json_data, indent=4)}\n```\n"
                                     f"**Room decodes to:** {room.title}\n"
                                     f"**From decodes to:** {person.displayName}\n"
                                     f"**Message text decodes to:** {message.text}\n")

        elif webhook_obj.resource == 'attachmentActions':
            room = wbxt_api.rooms.get(webhook_obj.data.roomId)                      # Get the room details
            message = wbxt_api.messages.get(webhook_obj.data.messageId)             # Get the message details
            person = wbxt_api.people.get(message.personId)                          # Get the sender's details
            attachment_action = wbxt_api.attachment_actions.get(webhook_obj.data.id)     # Get attachment actions

            print("NEW ATTACHMENT ACTION IN ROOM '{}'".format(room.title))
            print("FROM '{}'".format(person.displayName))
            print("MESSAGE '{}'\n".format(message.text))
            print(message)

            wbxt_api.messages.create(
                room.id,
                markdown=f"**New Webhook POST received. Payload:**\n"
                         f"```\n{json.dumps(webhook_obj._json_data, indent=4)}\n```\n"
                         f"**Room decodes to:** {room.title}\n"
                         f"**From decodes to:** {person.displayName}\n"
                         f"**Message text decodes to:** {message.text}\n")
            wbxt_api.messages.create(
                room.id,
                markdown=f"**New Attachment Action in Room:** {room.title}\n"
                         f"**From:** {person.displayName}\n"
                         f"**Payload:**\n"
                         f"```\n{json.dumps(attachment_action._json_data, indent=4)}\n```\n")
    except Exception as e:
        print(e)

    return 'OK'
