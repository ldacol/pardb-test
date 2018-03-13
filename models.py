from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class peeringdbnodes(models.Model):
	companyname = models.CharField(max_length=48)
	asn = models.CharField(max_length=6)
	peeringnode = models.CharField(max_length=48)
	ipv4addr = models.CharField(max_length=16, unique=True)
	ipv6addr = models.CharField(max_length=40, unique=True)
	
	def __str__(self):
		return '%s %s %s' % (self.peeringnode, self.ipv4addr, self.ipv6addr)
