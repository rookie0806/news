from django.db import models
from rookie.users import models as user_models
from taggit.managers import TaggableManager

# Create your models here.
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class NewsPaper(models.Model):
    Office_name = models.CharField(max_length=100,default="")
    Percentage = models.FloatField(default=0)
    date = models.CharField(max_length=100,default="")
    Progress = models.BooleanField(default=False)
    
    def __str__(self):
        return '{}-{}'.format(self.Office_name, self.Percentage, self.date)

class Word(models.Model):
    Word = models.CharField(max_length=100,default="")
    Count = models.IntegerField(default=0)
    Progress = models.BooleanField(default=False)
    date = models.CharField(max_length=100,default="")
