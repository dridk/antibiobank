from django.db import models
# ------------------------------------------------------

class Bactery(models.Model):
	generic_name = models.CharField(max_length=255)
	specfic_name = models.CharField(max_length=255)
	def __str__(self):
		return self.generic_name+" "+self.specfic_name

# ------------------------------------------------------

class Service(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name

# ------------------------------------------------------

class Specimen(models.Model):
	name = models.CharField(max_length=64)
	def __str__(self):
		return self.name
# ------------------------------------------------------

class Antibiotic(models.Model):
	name 	  = models.CharField(max_length=255)
	def __str__(self):
		return self.name

# ------------------------------------------------------

class Record(models.Model):
	bactery    = models.ForeignKey(Bactery)
	service    = models.ForeignKey(Service)
	specimen   = models.ForeignKey(Specimen)
	date       = models.DateField()
 	patient    = models.CharField(max_length=10)
	birthday   = models.DateField()
	sensibility= models.ManyToManyField(Antibiotic, through='Resistance')


# ------------------------------------------------------

class Resistance(models.Model):
	record     = models.ForeignKey(Record)
	antibiotic = models.ForeignKey(Antibiotic)
	value      = models.CharField(max_length=3) 
