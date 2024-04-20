# Create your models here.
from django.db import models
from django.contrib.auth.models import User

#for front-end
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True) #upload_to='user_images/',
    favorite_stocks = models.JSONField(default=list, blank=True)
    plans = models.TextField(blank=True)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.user.username


#for backend data
class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.symbol

class StockData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE) #we are using foreign key
    Date = models.DateTimeField()
    Open = models.FloatField()
    High = models.FloatField()
    Low = models.FloatField()
    Close = models.FloatField()
    Volume = models.IntegerField()
    Dividends = models.FloatField()
    Stock_Splits = models.FloatField()

    def __str__(self):
        return f"{self.stock} - {self.Date}"