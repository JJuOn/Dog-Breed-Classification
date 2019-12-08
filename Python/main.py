from torchvision import transforms, datasets, models
import torch
from torch import optim, cuda
from torch.utils.data import DataLoader, random_split
import torch.nn.functional as F
import torch.nn as nn
from PIL import Image
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import sys

model=models.inception_v3(pretrained=True)
model.aux_logits=False
n_classes = 120
n_inputs = model.fc.in_features
model.fc = nn.Sequential(
    nn.Linear(n_inputs, 1024),
    nn.ReLU(),
    nn.Dropout(0.4),
    nn.Linear(1024, n_classes),
    nn.LogSoftmax(dim=1))
model.load_state_dict(torch.load('../Python/model.pt')['state_dict'])
classes=[
    'Chihuahua',
    'Japanese_Spaniel',
    'Maltese_Dog',
    'Pekinese',
    'Shih-Tzu',
    'Blenheim_Spaniel',
    'Papillon',
    'Toy_Terrier',
    'Rhodesian_Ridgeback',
    'Afghan_Hound',
    'Basset',
    'Beagle',
    'Bloodhound',
    'Bluetick',
    'Black-and-Tan_Coonhound',
    'Walker_Hound',
    'English_Foxhound',
    'Redbone',
    'Borzoi',
    'Irish_Wolfhound',
    'Italian_Greyhound',
    'Whippet',
    'Ibizan_Hound',
    'Norwegian_Elkhound',
    'Otterhound',
    'Saluki',
    'Scottish_Deerhound',
    'Weimaraner',
    'Staffordshire_Bullterrier',
    'American_Staffordshire_Terrier',
    'Bedlington_Terrier',
    'Border_Terrier',
    'Kerry_Blue_Terrier',
    'Irish_Terrier',
    'Norfolk_Terrier',
    'Norwich_Terrier',
    'Yorkshire_Terrier',
    'Wire-Haired_Fox_Terrier',
    'Lakeland_Terrier',
    'Sealyham_Terrier',
    'Airedale',
    'Cairn',
    'Australian_Terrier',
    'Dandie_Dinmont',
    'Boston_Bull',
    'Miniature_Schnauzer',
    'Giant_Schnauzer',
    'Standard_Schnauzer',
    'Scotch_Terrier',
    'Tibetan_Terrier',
    'Silky_Terrier',
    'Soft-Coated_Wheaten_Terrier',
    'West_Highland_White_Terrier',
    'Lhasa',
    'Flat-Coated_Retriever',
    'Curly-Coated_Retriever',
    'Golden_Retriever',
    'Labrador_Retriever',
    'Chesapeake_Bay_Retriever',
    'German_Short-Haired_Pointer',
    'Vizsla',
    'English_Setter',
    'Irish_Setter',
    'Gordon_Setter',
    'Brittany_Spaniel',
    'Clumber',
    'English_Springer',
    'Welsh_Springer_Spaniel',
    'Cocker_Spaniel',
    'Sussex_Spaniel',
    'Irish_Water_Spaniel',
    'Suvasz',
    'Schipperke',
    'Groenendael',
    'Malinois',
    'Briard',
    'Kelpie',
    'Komondor',
    'Old_English_Sheepdog',
    'Shetland_Sheepdog',
    'Collie',
    'Border_Collie',
    'Bouvier_Des_Flandres',
    'Rottweiler',
    'German_Shepherd',
    'Doberman',
    'Miniature_Pinscher',
    'Greater_Swiss_Mountain_Dog',
    'Bernese_Mountain_Dog',
    'Appenzeller',
    'EntleBucher',
    'Boxer',
    'Bull_Mastiff',
    'Tibetan_Mastiff',
    'French_Bulldog',
    'Great_Dane',
    'Saint_Bernard',
    'Eskimo_Dog',
    'Malamute',
    'Siberian_Husky',
    'Affenpinscher',
    'Basenji',
    'Pug',
    'Leonberg',
    'Newfoundland',
    'Great_Pyrenees',
    'Samoyed',
    'Pomeranian',
    'Chow',
    'Keeshond',
    'Brabancon_Griffon',
    'Pembroke',
    'Cardigan',
    'Toy_Poodle',
    'Miniature_Poodle',
    'Standard_Poodle',
    'Mexican_Hairless',
    'Dingo',
    'Dhole',
    'African_Hunting_Dog'
]
model.cuda()
model.eval()
img=Image.open(os.path.join('..','Node','uploads',sys.argv[1]))
img=img.resize((299,299))
ToTensor_trans=transforms.ToTensor()
Normalize_trans=transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
outputs=model(Normalize_trans(ToTensor_trans(img)).unsqueeze(0).cuda())
outputs=F.softmax(outputs,dim=1)
outputs,idx=outputs.unsqueeze(0).topk(2)
sys.stdout.flush()
for i,o in zip(idx.tolist()[0][0],outputs.tolist()[0][0]):
    print('{},{:.4f}'.format(classes[i],o*100))
sys.stdout.flush()