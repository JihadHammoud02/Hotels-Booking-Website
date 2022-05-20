from django.db import models
from django.contrib.auth.models import User
# An instance of this class will be created each time a user buys a hotel, to prevent relisting a bought hotel
class Transactions(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) #User id
    Hotel_name=models.CharField(max_length=200) #Hotel name
    purchase_time=models.DateTimeField('date published')  #time of purchase of the hotel
