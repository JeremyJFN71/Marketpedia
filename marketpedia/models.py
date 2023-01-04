from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', default='profile_images/default.png')
    fullname = models.CharField(max_length=50)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('G', '-----Gender-----'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    mobile_phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self) -> str:
        return f'{self.user.username} Profile'


class Market(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, primary_key=True)
    image = models.ImageField(upload_to='market_images')
    mobile_phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self) -> str:
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    image = models.ImageField(upload_to='product_images')
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(Market, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.seller}, {self.name}'