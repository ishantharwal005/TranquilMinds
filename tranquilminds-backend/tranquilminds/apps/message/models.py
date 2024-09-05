# Create your models here.

from django.db import models

class Message(models.Model):
    recno = models.AutoField(primary_key=True, db_column='recno')
    senderid = models.IntegerField(db_column='senderid')
    recipientid = models.IntegerField(db_column='recipientid')
    content = models.TextField(db_column='content')
    timestamp = models.DateTimeField(db_column='timestamp', auto_now_add=True)

    def __str__(self):
        return str(self.recno)
    
    class Meta:
        managed = True
        db_table = 'message'