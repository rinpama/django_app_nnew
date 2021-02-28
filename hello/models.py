from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.validators import MinLengthValidator
from django.core.validators import URLValidator,EmailValidator#引数無し
from django.core.validators import ProhibitNullCharactersValidator#null文字の禁止
from django.core.validators import RegexValidator#正規表現パターン

import re
from django.core.validators import ValidationError


def number_only(value):
    if (re.match(r'^[0-9]*$',value) == None):
        raise ValidationError(
    '%(value)s is not Number!',\
        params={'value':value,
        })

# Create your models here.
class Friend(models.Model):
    name= models.CharField(max_length=100, \
        validators=[MinLengthValidator(5),\
            RegexValidator(r'^[a-z*$')])
    mail= models.EmailField(max_length=200,\
        validators=[EmailValidator()])
    gender=models.BooleanField()
    age=models.IntegerField(validators=[ \
        MinValueValidator(0),\
            MaxValueValidator(150),\
                number_only])#★
    birthday=models.DateField()

    def __str__(self):
        return '<Friend:id='+ str(self.id)+ ','+ \
            self.name+ '('+ str(self.age)+ ')>'

class Message(models.Model):
    friend= models.ForeignKey(Friend,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    content= models.CharField(max_length=300)
    pub_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<Message:id'+ str(self.id)+ ','+ \
            self.title+ '('+ str(self.pub_date)+ ')>'

    class Meta:
        ordering=('pub_date',)
        