import boto3
import glob
import os

from config import config as _config
from metadata import bin_type_to_name_dict, name_to_bin_dict

class BinBuddy:

    def __init__(self, config=None):
        if config == None:
            self.config = _config
        else:
            self.config = config

        self.client = boto3.client('rekognition', aws_access_key_id=self.config['rekognition']['aws_access_key_id'], aws_secret_access_key=self.config['rekognition']['aws_secret_access_key'], region_name=self.config['rekognition']['region_name'])
    
    def detect_label_from_path(self, image_path):
        with open(image_path, 'rb') as image:
            response = self.client.detect_labels(Image={'Bytes': image.read()})

        print('Detected labels in ' + image_path)    
        for label in response['Labels']:
            print (label['Name'] + ' : ' + str(label['Confidence']))

        return response['Labels']

    def detect_label_from_byte(self, image_byte):
        response = self.client.detect_labels(Image={'Bytes': image_byte})
        for label in response['Labels']:
            print (label['Name'] + ' : ' + str(label['Confidence']))

        return response['Labels']

    def which_bin_to_thrash(self, image_byte):

        labels = self.detect_label_from_byte(image_byte)
        output_texts = list()
        for label in labels:
            detected_object = label['Name']
            detected_object = detected_object.lower()
            try:
                bin_type = bin_type_to_name_dict[name_to_bin_dict[detected_object]]
            except:
                continue
            text = 'ตรวจพบ "{}" เป็นขยะประเภท "{}"'.format(detected_object, bin_type)
            output_texts.append(text)

        return output_texts

if __name__ == "__main__":
    binbuddy = BinBuddy(config=_config)
    with open('test-image/test.jpg', 'rb') as image:
        labels = binbuddy.which_bin_to_thrash(image.read())
    print(labels)

