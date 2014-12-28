import os
from transloadit.TransloaditClient import TransloaditClient


client = TransloaditClient(os.environ['KEY'], os.environ['SECRET'])
file = open('data/image_sample_2.jpg')
steps = {
    "resize_to_250": {
        "robot": "/image/resize",
        "width": 250,
        "height": 250
    },
}

print client.upload(file, assembly_steps=steps)

print client.upload(file, template_id=os.environ['TEMPLATE_ID'])
