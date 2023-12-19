from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"

    class Meta:
        ordering = ("-created", "-updated")

    def __str__(self):
        return "{}".format(self.title)
