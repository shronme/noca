import requests

ACCESS_TOKEN = "EAAYquG24IwkBAPigmNaZC7zKpnbmrjcxLinW9FZCKqmTkuuoN3Jaddb505v9FCWZAZBc5exqutYRKRWZBzoSmsohrpQ0K0qV621GTk4FGaISlky6qN9Gjx07sXXHVvg5HaVkj0ZBbEyyjnbmlZAILoc3kXR5HjV0XfUjabVyhtnAAZDZD"


def reply(user_id, msg):
	    data = {
	        "recipient": {"id": user_id},
	        "message": {"text": msg}
	    }
	    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	    print(resp.content)

def reply_with_buttons(user_id, button_list, text):
	data = {
		"recipient": {"id": user_id},
		"message": {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "button",
					"text": text,
					"buttons": [
									{
										"type":"web_url",
										"url":"https://petersapparel.parseapp.com",
										"title":"Show Website"
									},
									{
										"type":"postback",
										"title":"Start Chatting",
										"payload":"USER_DEFINED_PAYLOAD"
									}
								]
				}
			}
		}
	}

	print('message sent is: ',data)
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	print(resp.content)


	# data = {
# 	        "recipient": {"id": user_id},
# 	        'message': {
# 		        'attachment': {
# 		        	'type': "template",
# 		        	'payload': {
# 		        		'template_type': "generic",
# 		        		'elements': [{
# 			        		'title': "rift",
# 			        		'subtitle': "Next-generation virtual reality",
# 			        		'item_url': "https://www.oculus.com/en-us/rift/",
# 			        		'image_url': "http://messengerdemo.parseapp.com/img/rift.png",
# 			        		'buttons': [{
# 			        			'type': "web_url",
# 			        			'url': "https://www.oculus.com/en-us/rift/",
# 			        			'title': "Open Web URL"
# 		        			}, 
# 		        			{
# 		        				'type': "postback",
# 		        				'title': "Call Postback",
# 		        				'payload': "Payload for first bubble",
# 	    				}],
# 						}, 
# 						{
# 							'title': "touch",
# 							'subtitle': "Your Hands, Now in VR",
# 							'item_url': "https://www.oculus.com/en-us/touch/",
# 							'image_url': "http://messengerdemo.parseapp.com/img/touch.png",
# 							'buttons': [{
# 								'type': "web_url",
# 								'url': "https://www.oculus.com/en-us/touch/",
# 								'title': "Open Web URL"
# 							}, 
# 							{
# 								'type': "postback",
# 								'title': "Call Postback",
# 								'payload': "Payload for second bubble",
# 							}]
# 						}]
# 					}
# 				}
# 		    }
# 	    }
	

