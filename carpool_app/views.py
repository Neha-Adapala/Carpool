from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from datetime import timedelta
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# Create your views here.
from .models import *
# from .forms import OrderForm, CreateUserForm
from .forms import CreateUserForm, ProfileForm, CarRegistrationForm, RideForm
# from .filters import OrderFilter

# The code below is to display the User Registration Page and capture the details in the database
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('request_ride')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'carpool/register.html', context)

# The code below is to display the User Login Page and do validations as well
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('request_ride')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('request_ride')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'carpool/login.html', context)

# The code below is to allow the user to logout
def logoutUser(request):
    logout(request)
    return redirect('login')

# The code below is to display the Request a ride page after logging in
@login_required(login_url='login')
def request_ride(request):
    user_id = request.user.id
    location = Location.objects.all()

    requested_rides = RequestRide.objects.filter(user_id=User.objects.get(id=user_id),  ride_id__isnull=False ).values_list('ride_id')
    #print(f"requested_rides: {requested_rides}")
    ridelist = Ride.objects.exclude(id__in=requested_rides).order_by('-record_created_on')
    #print(f"Ride List: {ridelist}")
    timestamp_format = '%Y-%m-%dT%H:%M'
    request_start_location = ""
    request_destination_location = ""
    request_start_timestamp = datetime.now().strftime(timestamp_format)

    if request.method == "POST":
        request_action = request.POST['action']

        if request_action == 'Search':
            request_start_location = request.POST['source_location_id']
            request_destination_location = request.POST['destination_location_id']
            request_start_timestamp = request.POST['travel_start_time']
            print(f"before request_start_timestamp: {request_start_timestamp}")
            # Get Current Time if the request_start_timestamp is not selected in HTML form
            if request_start_timestamp == '':
                request_start_timestamp = datetime.now().strftime(timestamp_format)
                print(f"request_start_timestamp: {request_start_timestamp}")

            request_start_timestamp_begin = datetime.strptime(request_start_timestamp, timestamp_format) - timedelta(hours=1)
            request_start_timestamp_end = datetime.strptime(request_start_timestamp, timestamp_format) + timedelta(hours=1)

            print(f"Search params for Ride List: {ridelist}")
            ridelist = ridelist.filter(source_location_id = request_start_location, destination_location_id=request_destination_location, travel_start_time__range=(request_start_timestamp_begin.strftime(timestamp_format), request_start_timestamp_end.strftime(timestamp_format)))
            print(f"Ride List: {ridelist}")
            context = {'location': location, 'ridelist': ridelist, 'selected_source_location_id':request_start_location, 'selected_destination_location_id':request_destination_location, 'selected_travel_start_time':request_start_timestamp}
            return render(request, 'carpool/request_ride.html', context)
        else:
            #print(f"Ride '{request_search}' Parameters: Start {request_start_location} - Destination {request_destination_location} - Start Timestamp {request_start_timestamp}")
            requestride = RequestRide(user_id=User.objects.get(id=user_id), ride_id=Ride.objects.get(id=request.POST['ride_id']), request_status='Submitted')
            requestride.save()
            return HttpResponseRedirect('/ride_status/')

    context = {'location': location, 'ridelist': ridelist, 'selected_source_location_id':request_start_location, 'selected_destination_location_id':request_destination_location, 'selected_travel_start_time':request_start_timestamp}
    return render(request, 'carpool/request_ride.html', context)


# The code below is to display the Ride Status page after logging in
@login_required(login_url='login')
def ride_status(request):
    requestridelist = RequestRide.objects.filter(user_id=request.user.id).order_by('-ride_id__id','-record_created_on')

    driver_ridelist = Ride.objects.filter(user_id=request.user.id).values_list('id')
    driver_requestridelist = RequestRide.objects.filter(ride_id__in=driver_ridelist).order_by('-ride_id__id','-record_created_on')

    print(f"requestridelist: {requestridelist}")

    context = {'requestridelist': requestridelist, 'driver_requestridelist': driver_requestridelist}
    return render(request, 'carpool/ride_status.html', context)

# The code below is to display the list of requested rides in order to allow the driver to accept/reject a ride after logging in
@login_required(login_url='login')
def accept_reject_ride(request):
    driver_ridelist = Ride.objects.filter(user_id=request.user.id).values_list('id')
    driver_requestridelist = RequestRide.objects.filter(ride_id__in=driver_ridelist,request_status="Submitted").order_by('-ride_id__id','-record_created_on')

    if request.method == "POST":
        requestride = RequestRide.objects.get(id=request.POST['requestride_id'])
        requestride.request_status = request.POST['accept_reject']+'ed'   # for storing 'Accept'+'ed' or 'Reject'+'ed'
        requestride.save()
        return HttpResponseRedirect('/ride_status/')

    context = {'driver_requestridelist': driver_requestridelist}
    return render(request, 'carpool/accept_reject_ride.html', context)

# The code below is to display the aggregated counts of accepted rides and the rides that the driver accepted after logging in
@login_required(login_url='login')
def leader_board(request):
    # As a Passenger, how many rides you have booked
    my_accepted_requestridelist = RequestRide.objects.filter(user_id=request.user.id, request_status='Accepted')
    my_accepted_requestridelist_count = my_accepted_requestridelist.count()

    # As a Driver, how many rides others have booked and the ones you have accepted
    my_driver_ridelist = Ride.objects.filter(user_id=request.user.id).values_list('id')
    my_driver_accepted_requestridelist = RequestRide.objects.filter(ride_id__in=my_driver_ridelist, request_status='Accepted')
    my_driver_accepted_requestridelist_count = my_driver_accepted_requestridelist.count()

    # How many rides each passenger has booked
    accepted_requestridelist = RequestRide.objects.filter(request_status='Accepted').values('user_id__username').annotate(
        total=Count('user_id__username')).order_by('-total')

    # How many rides each drives has accepted
    driver_accepted_requestridelist = RequestRide.objects.filter(request_status='Accepted').values(
        'ride_id__user_id__username').annotate(total=Count('ride_id__user_id__username')).order_by('-total')

    print(f"accepted_requestridelist: {accepted_requestridelist}")
    print(f"driver_accepted_requestridelist: {driver_accepted_requestridelist}")

    context = {'accepted_requestridelist': accepted_requestridelist,
               'driver_accepted_requestridelist': driver_accepted_requestridelist,
               'my_accepted_requestridelist_count': my_accepted_requestridelist_count,
               'my_driver_accepted_requestridelist_count': my_driver_accepted_requestridelist_count
               }
    return render(request, 'carpool/leader_board.html', context)

# The code below is to register the car details after logging in
@login_required(login_url='login')
def car_registration(request):
    membercarlist = MemberCar.objects.filter(user_id=request.user.id)
    error_message = ""
    form = CarRegistrationForm()
    if request.method == "POST":
        form = CarRegistrationForm(request.POST)
        try:
            if form.is_valid():
                #form.save()
                obj = form.save(commit=False)
                obj.user_id = User.objects.get(id=request.user.id)
                obj.save()
                form = CarRegistrationForm()
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                error_message = "This Car Registration Number Is Already Used By You"

    context = {'car_registration_form': form, 'membercarlist': membercarlist, 'error_message': error_message}
    return render(request, 'carpool/car_registration.html', context)

# The code below is to update the car details after logging in
@login_required(login_url='login')
def car_registration_update(request, pk):

    membercar = MemberCar.objects.get(id=pk,user_id=request.user.id)

    membercarlist = MemberCar.objects.filter(user_id=request.user.id)
    form = CarRegistrationForm(instance=membercar)
    if request.method == "POST":
        print(f"pk: {pk}, Update Member Car: {membercar}")
        form = CarRegistrationForm(request.POST, instance=membercar)
        if form.is_valid():
            form.save()
            form = CarRegistrationForm()
            return HttpResponseRedirect('/car_registration/')

    context = {'car_registration_form': form, 'membercarlist': membercarlist}
    return render(request, 'carpool/car_registration_update.html', context)

# The code below is to delete the car details after logging in
@login_required(login_url='login')
def car_registration_delete(request, pk):
    membercar = MemberCar.objects.get(id=pk, user_id=request.user.id)
    membercarlist = MemberCar.objects.filter(user_id=request.user.id)
    if request.method == "POST":
        print(f"pk: {pk}, Delete Member Car: {membercar}")
        membercar.delete()
        membercarlist = MemberCar.objects.filter(user_id=request.user.id)
        return HttpResponseRedirect('/car_registration/')

    context = {'membercar': membercar, 'membercarlist': membercarlist}
    return render(request, 'carpool/car_registration_delete.html', context)

# The code below is to insert the ride details after logging in
@login_required(login_url='login')
def ride_insert(request):
    ridelist = Ride.objects.filter(user_id=request.user.id).order_by('-record_created_on')
    error_message = ""
    form = RideForm(user_id=request.user.id)
    if request.method == "POST":
        form = RideForm(request.POST, user_id=request.user.id)
        try:
            if form.is_valid():
                #form.save()
                obj = form.save(commit=False)
                obj.user_id = User.objects.get(id=request.user.id)
                obj.save()
                form = RideForm(user_id=request.user.id)
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                error_message = "This Car Registration Number Is Already Used By You"

    context = {'ride_form': form, 'ridelist': ridelist, 'error_message': error_message}
    return render(request, 'carpool/ride_insert.html', context)

# The code below is to update the ride details after logging in
@login_required(login_url='login')
def ride_update(request, pk):

    ride = Ride.objects.get(id=pk,user_id=request.user.id)

    ridelist = Ride.objects.filter(user_id=request.user.id).order_by('-record_created_on')
    form = RideForm(instance=ride, user_id=request.user.id)
    if request.method == "POST":
        print(f"pk: {pk}, Update Ride: {ride}")
        form = RideForm(request.POST, instance=ride, user_id=request.user.id)
        if form.is_valid():
            form.save()
            form = RideForm(user_id=request.user.id)
            return HttpResponseRedirect('/ride_insert/')

    context = {'ride_form': form, 'ridelist': ridelist}
    return render(request, 'carpool/ride_update.html', context)

# The code below is to delete the ride details after logging in
@login_required(login_url='login')
def ride_delete(request, pk):
    ride = Ride.objects.get(id=pk, user_id=request.user.id)
    ridelist = Ride.objects.filter(user_id=request.user.id).order_by('-record_created_on')
    if request.method == "POST":
        print(f"pk: {pk}, Delete Ride: {ride}")
        ride.delete()
        ridelist = Ride.objects.filter(user_id=request.user.id)
        return HttpResponseRedirect('/ride_insert/')

    context = {'ride': ride, 'ridelist': ridelist}
    return render(request, 'carpool/ride_delete.html', context)

# The code below is to capture additional details of the user profile after logging in
@login_required(login_url='login')
def member_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # obj = form.save(commit=False)
            # obj.user_id = User.objects.get(id=request.user.id)
            # obj.save()
    # else:
    #     form = ProfileForm()

    context = {'form': form}
    return render(request, 'carpool/member_profile.html', context)

# The code below is to display instructions on the usage of this website
def instructions(request):
    return render(request, 'carpool/instructions.html')

