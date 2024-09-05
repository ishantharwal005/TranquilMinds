from django.db import models

# Create your models here.

class TherapistModel(models.Model):
    therapistid = models.AutoField(primary_key=True, db_column='therapistid')
    userid = models.IntegerField(db_column='userid', null = False, unique = True)
    bio = models.CharField(max_length = 45, db_column = 'bio', null = True)
    specialization = models.CharField(max_length = 45, db_column = 'specialiazation', null = True)
    experience = models.CharField(max_length = 45, db_column = 'experience', null = True)
    education = models.CharField(max_length = 45, db_column = 'education', null = True)
    active = models.BooleanField(db_column = 'active', null = False, default = True)

    def __str__(self):
        return str(self.therapistid)
    
    class Meta:
        managed = True
        db_table = 'therapist'