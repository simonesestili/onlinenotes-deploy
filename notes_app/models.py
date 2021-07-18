from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, blank=True)
    content = models.TextField(null=True, blank=True)
    create_time = models.DateTimeField()
    last_save_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        print('title:', self.title)
        if self.title.strip() == '':
            self.title = 'Untitled Note'
        super(Note, self).save(*args, **kwargs)

    def get_pk(self):
        return self.pk

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-last_save_time']


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    enabled_dark = models.BooleanField(default=False)