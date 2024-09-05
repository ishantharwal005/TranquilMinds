from django.db import models

# Create your models here.

class UserModel(models.Model):
    userid = models.AutoField(primary_key=True, db_column='userid')
    username = models.CharField(max_length = 45, db_column = 'username', null = False, unique = True)
    password = models.CharField(max_length = 100, db_column = 'password', null = False, unique = True)
    email = models.CharField(max_length = 45, db_column = 'email', null = False, unique = True)
    usertype = models.CharField(max_length = 45, db_column = 'usertype', null = False)
    name = models.CharField(max_length = 45, db_column = 'name', null = False)
    contact = models.CharField(max_length = 45, db_column = 'contact', null = False, unique = True)
    dob = models.DateField(db_column = 'dob', null = False)
    active = models.BooleanField(db_column = 'active', null = False, default = True)

    def __str__(self):
        return str(self.userid)
    
    class Meta:
        managed = True
        db_table = 'user'