import torch
import torch.nn as nn
import numpy as np


"""
CNN structure 

input shape (batch,channels (features),length)

Out shape = ((Lin-(kernel -1) - 1)/stride+1)
"""


class CNN(nn.Module):
    def __init__(self,input_features=3,input_length=200,num_classes=5,dropout=0.1):
        super(CNN,self).__init__()
        # variables
        self.in_channels=input_features
        self.in_length=input_length
        self.num_classes=num_classes
        self.dropout=nn.Dropout(dropout)
        self.activation=nn.ReLU()
        # Architecture

        self.conv1=nn.Conv1d(in_channels=self.in_channels,out_channels=64,kernel_size=7,stride=1)
        self.lout1=self.in_length-6
        # lout1=194
        self.batchnorm1= nn.BatchNorm1d(num_features=64)
        
        self.conv2=nn.Conv1d(in_channels=64,out_channels=128,kernel_size=7,stride=1)
        self.lout2=self.lout1-6
        #lout2=188
        self.batchnorm2=nn.BatchNorm1d(num_features=128)

        self.conv3=nn.Conv1d(in_channels=128,out_channels=256,kernel_size=7,stride=1)
        self.lout3=self.lout2-6
        #lout3= 182
        self.batchnorm3=nn.BatchNorm1d(num_features=256)

        self.conv4=nn.Conv1d(in_channels=256,out_channels=512,kernel_size=9,stride=1)
        # lout = 174
        self.lout4=self.lout3-8
        self.maxpool1=nn.MaxPool1d(kernel_size=4,stride=2)
        # lout= 87
        self.lout4=(self.lout4-2)/2 + 1
        self.batchnorm4=nn.BatchNorm1d(num_features=512)

        self.conv5=nn.Conv1d(in_channels=512,out_channels=128,kernel_size=10,stride=1)
        # lout = 78 
        self.lout5= self.lout4-9

        self.maxpool2=nn.MaxPool1d(kernel_size=4,stride=2)
        # lout = 39
        self.lout6=(self.lout5-2)/2 + 1
        self.batchnorm5=nn.BatchNorm1d(num_features=128)


        self.dense1=nn.Linear(in_features=int(128*37),out_features=num_classes)


        self.softmax=nn.Softmax(dim=1)


        
    def forward(self,x):

        x=self.conv1(x)
        x=self.batchnorm1(x)
        x=self.activation(x)

        x=self.conv2(x)
        x=self.activation(x)

        x=self.conv3(x)
        x=self.batchnorm3(x)
        x=self.activation(x)

        x=self.conv4(x)
        x=self.maxpool1(x)
        x=self.activation(x)

        x=self.conv5(x)
        x=self.maxpool2(x)
        x=self.batchnorm5(x)
        x=self.activation(x)

        x=x.reshape((-1,x.shape[1]*x.shape[2]))
        x=self.dense1(x)

        

        return x


    def forward_run(self,x):
        x=torch.from_numpy(x.reshape(-1,self.input_size,self.input_length)).float()
        x=x.to(self.device)
        y=self.forward(x)
        
        return self.softmax(y)


        


        
