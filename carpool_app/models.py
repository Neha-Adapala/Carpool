from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.
from datetime import datetime

class Car(models.Model):
	class MakeYear(models.IntegerChoices):
		TWENTY_TWENTYTWO = 2022, '2022'
		TWENTY_TWENTYONE = 2021, '2021'
		TWENTY_TWENTY = 2020, '2020'
		TWENTY_NINETEEN = 2019, '2019'
		TWENTY_EIGHTEEN = 2018, '2018'
		TWENTY_SEVENTEEN = 2017, '2017'
		TWENTY_SIXTEEN = 2016, '2016'
		TWENTY_FIFTEEN = 2015, '2015'
		TWENTY_FOURTEEN = 2014, '2014'
		TWENTY_THIRTEEN = 2013, '2013'
		TWENTY_TWELVE = 2012, '2012'
		TWENTY_ELEVEN = 2011, '2011'
	class MaxPassengers(models.IntegerChoices):
		ONE = 1, '1'
		TWO = 2, '2'
		THREE = 3, '3'
		FOUR = 4, '4'
		FIVE = 5, '5'
		SIX = 6, '6'


	name = models.CharField(max_length=50, null=False)
	make = models.CharField(max_length=50, null=True)
	model = models.CharField(max_length=50, null=True)
	make_year = models.IntegerField(default=MakeYear.TWENTY_TWENTYTWO, choices=MakeYear.choices)
	max_passengers = models.IntegerField(default=MaxPassengers.ONE, choices=MaxPassengers.choices)

	def __str__(self):
		return self.name



class Location(models.Model):
	location = models.CharField(max_length=100, null=False)
	county_or_state = models.CharField(max_length=100, null=False)
	country = models.CharField(max_length=100, null=False)

	def __str__(self):
		return self.location

class LuggageSize(models.Model):
	DESCRIPTION = (
						('Light', 'Light'),
						('Medium', 'Medium'),
						('Heavy', 'Heavy'),
						)
	description = models.CharField(max_length=100, null=False, choices=DESCRIPTION)

	def __str__(self):
		return self.description

class Profile(models.Model):
	class DrivingLicense(models.IntegerChoices):
		TWENTY_TWENTYTWO = 2022, '2022'
		TWENTY_TWENTYONE = 2021, '2021'
		TWENTY_TWENTY = 2020, '2020'
		TWENTY_NINETEEN = 2019, '2019'
		TWENTY_EIGHTEEN = 2018, '2018'
		TWENTY_SEVENTEEN = 2017, '2017'
		TWENTY_SIXTEEN = 2016, '2016'
		TWENTY_FIFTEEN = 2015, '2015'
		TWENTY_FOURTEEN = 2014, '2014'
		TWENTY_THIRTEEN = 2013, '2013'
		TWENTY_TWELVE = 2012, '2012'
		TWENTY_ELEVEN = 2011, '2011'
		TWENTY_TEN = 2010, '2010'
		TWENTY_NINE = 2009, '2009'
		TWENTY_EIGHT = 2008, '2008'
		TWENTY_SEVEN = 2007, '2007'
		TWENTY_SIX = 2006, '2006'
		TWENTY_FIVE = 2005, '2005'
		NONE = 0 , 'N/A'

	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	contact_number = models.CharField(max_length=15, null=True)
	driving_license_number = models.CharField(max_length=50, null=True)
	driving_license_valid_from = models.IntegerField(choices=DrivingLicense.choices, null=True)

	def __str__(self):
		return self.user.username


class MemberCar(models.Model):
	user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	car_id = models.ForeignKey(Car, null=True, on_delete=models.SET_NULL)
	car_registration_number = models.CharField(max_length=10, null=False)
	car_colour = models.CharField(max_length=15, null=False)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['user_id', 'car_registration_number'],
									name='unique car registration number constraint')
		]

	def __str__(self):
		return self.car_registration_number

class Ride(models.Model):
	class SeatsOffered(models.IntegerChoices):
		ONE = 1, '1'
		TWO = 2, '2'
		THREE = 3, '3'
		FOUR = 4, '4'
		FIVE = 5, '5'
		SIX = 6, '6'

	user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	member_car_id = models.ForeignKey(MemberCar, null=True, on_delete=models.SET_NULL)
	record_created_on = models.DateTimeField(auto_now_add=True, null=False)
	travel_start_time = models.DateTimeField(null=False)
	source_location_id = models.ForeignKey(Location, related_name='source_location', null=True, on_delete=models.SET_NULL)
	destination_location_id = models.ForeignKey(Location, related_name='destination_location', null=True, on_delete=models.SET_NULL)
	seats_offered = models.IntegerField(default=SeatsOffered.FOUR, choices=SeatsOffered.choices)
	contribution_per_head = models.FloatField(null=False)
	luggage_size_id = models.ForeignKey(LuggageSize, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.member_car_id.car_registration_number+'-'+self.source_location_id.location+'-'+self.destination_location_id.location+'-'+self.travel_start_time.strftime("%d/%m/%Y %H:%M:%S")

class RequestRide(models.Model):
	CHOSEN= (
		('Submitted', 'Submitted'),
		('Accepted', 'Accepted'),
		('Rejected', 'Rejected'),
	)
	user_id = models.ForeignKey(User, related_name='user_id', null=True, on_delete=models.SET_NULL)
	ride_id = models.ForeignKey(Ride, related_name='ride_id', null=True, on_delete=models.SET_NULL)
	record_created_on = models.DateTimeField(auto_now_add=True, null=False)
	request_status = models.CharField(max_length=15, null=False, choices=CHOSEN)




