from django.db import models

# Create your models here.
class HypervisorInfo(models.Model):
    esxi_hostname = models.CharField(max_length=100)
    esxi_username = models.CharField(max_length=100)
    esxi_password = models.CharField(max_length=100)
