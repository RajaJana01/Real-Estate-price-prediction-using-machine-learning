from django.db import models

# Create your models here.
class RealEstate(models.Model):
    location=models.CharField(max_length=400)
    area=models.CharField(max_length=400)
    park=models.CharField(max_length=400)
    bed=models.CharField(max_length=400)
    sqft=models.CharField(max_length=400)
    bath=models.CharField(max_length=400)
    balcony=models.CharField(max_length=400)
    price=models.CharField(max_length=400)
    def __str__(self):
        return f"Prediction Price{self.Price}:{self.location}"
    
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=10)
    cpassword = models.CharField(max_length=10)
    def __str__(self):
        return self.email
    class AboutUs(models.Model):
        description=models.TextField()
    
    