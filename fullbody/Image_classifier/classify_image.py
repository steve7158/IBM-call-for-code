
import json
from ibm_watson import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '2019-07-28',

    iam_apikey="KPQzu2gGM267NaY_AIH12RyjlfT223gkbr3WlIZ559tg")

with open('./1.jpeg', 'rb') as images_file:
    classes = visual_recognition.classify(
        images_file,
        threshold='0.6',
	classifier_ids='DefaultCustomModel_1260232444').get_result()
print(json.dumps(classes['images'][0]['classifiers'][0]['classes'][0]['class'], indent=2))
