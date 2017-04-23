import datetime
import boto3
import random
import string
from mongoengine import *

class User(Document):
    fb_id = StringField(required=True, unique=True)
    state = StringField(required=True)
    name = StringField()
    date_modified = DateTimeField(default=datetime.datetime.now)
    address = DictField()
    state_dict = DictField()
    attempt_counter = IntField()


    def authenticate_user(self, image):

    	rnd_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    	
		image_name = '{user}/auth/transaction_{rnd}.jpeg'.format(user=user.name, rnd=rnd_str)
		s3 = boto3.resource('s3')
		rek = boto3.client('rekognition', region_name='eu-west-1')
		s3.Bucket('noca-auth-library').put_object(Key=image_name, Body=image)
		target_obj = s3.Object('noca-auth-library',image_name).wait_until_exists()
		face_detect = rek.detect_faces(
			Image={
				'S3Object': {
					'Bucket': 'noca-auth-library',
					'Name': image_name
				}
			},
			Attributes=['DEFAULT']
		)
		print('face detect: ', face_detect)
		if len(face_detect['FaceDetails']) > 0:
			if face_detect['FaceDetails'][0]['Confidence'] > 50:
				source_image_name = '{name}/source/{name}-source.jpeg'.format(name=user.name)
				print('source name: ', source_image_name)
				print('target name: ', image_name)
				
				response = rek.compare_faces(
					SimilarityThreshold=0,
					SourceImage={
						'S3Object': {
							'Bucket': 'noca-auth-library',
							'Name': source_image_name
						}
					}, 
					TargetImage={
						'S3Object': {
							'Bucket': 'noca-auth-library', 
							'Name': image_name
						}
					}
				)
				print('rek response: ', response)
				try:
					similarity = response['FaceMatches'][0]['Similarity']
					print('found faces')
					if similarity > 85:
						reply(sender, 'Your FaceID was authenticated successfully')
					else:
						reply(sender, 'We didn\'t manage to authenticate your FaceID, please try again')

				except IndexError:
					print('Did not find a face in the image')
					reply(sender, 'We didn\'t manage to authenticate your FaceID, please try again')
			else:
				reply(sender, 'We didn\'t manage to find a face in the image')	
		else:
			reply(sender, 'We didn\'t manage to find a face in the image')