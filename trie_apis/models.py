from django.db import models
from django.contrib.postgres.fields import ArrayField


class LocationTrieDb(models.Model):
    node_id = models.CharField(max_length=50, blank=False, null=False, primary_key=True)
    is_end = models.BooleanField(blank=False, null=False)
    children = ArrayField(models.CharField(max_length=50, null=False), blank=True, null=True)
    node_value = models.CharField(max_length=1, blank=True, null=True)
    popularity = models.BigIntegerField(blank=True, null=True)
