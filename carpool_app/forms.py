from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile, MemberCar, Ride

class DateTimePickerInput(forms.DateTimeInput):
        input_type = 'datetime'

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		#fields = '__all__'
		exclude = ['user']

class CarRegistrationForm(ModelForm):
	class Meta:
		model = MemberCar
		#fields = '__all__'
		#travel_start_time = forms.DateTimeField(widget=DateTimePickerInput)
		exclude = ['user_id']



class RideForm(ModelForm):
	class Meta:
		model = Ride
		#fields = '__all__'
		exclude = ['user_id']

	def __init__(self, *args, **kwargs):
		user_id = kwargs.pop('user_id')
		super(RideForm, self).__init__(*args, **kwargs)
		self.fields['member_car_id'].queryset = MemberCar.objects.filter(user_id=user_id)

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
