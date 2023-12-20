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
        verbose_name = "Notes"
        verbose_name_plural = "Notes"

    class Meta:
        ordering = ("-created", "-updated")

    def __str__(self):
        return "{}".format(self.title)


class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    class Meta:
        ordering = ("-due_date", "-created")

    def __str__(self):
        return "{}".format(self.title)


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    tasks = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = "-created"

    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todos"
