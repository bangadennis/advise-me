from django.shortcuts import render
from user_auth.forms import UserForm, UserDetailsForm, ClothDescriptionForm, UserActivityForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from models import UserDetails, ClothDescription, UserActivity

def index(request):
    
    if request.user.is_authenticated():
        return HttpResponseRedirect('/auth/try')
    
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'message': "Welcome to Outfit.com", }

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'user_auth/base.html', context_dict)



@login_required
def trya(request):
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        hello="Welcome, to Our Outfit Expert System:"
        user=UserDetails.objects.get(user=request.user)
        cloths=ClothDescription.objects.all().filter(user=request.user)
            
        return render(request,
                      'user_auth/trya.html',
                      {'cloths': cloths, 'userdetails': user})
    
    
#registration view
def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/auth/try')
    
    if request.method=="POST":
        
        userform=UserForm(data=request.POST)
        
        if userform.is_valid():
            
            #saving the user's form data in the databases
            user=userform.save()
            #hashing the password
            user.set_password(user.password)
            user.save()
            #login a new user
            username=request.POST['username']
            password=request.POST['password']
            
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user=authenticate(username=username, password=password)
            login(request, new_user)
            
            return HttpResponseRedirect('/auth/userdetails')
            
        else:
            
            print userform.errors
    else:
        userform=UserForm()
    
    #return render to response depending on the context
    return render(request,
                  "user_auth/registeration.html",
                  {"userform": userform})


#login view
def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/auth/try')
    
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        
        user=authenticate(username=username, password=password)
        
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/auth/try')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Outfit account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            #return HttpResponse("Invalid login details supplied.")
            return render(request, 'user_auth/login.html', {"invalid": True})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'user_auth/login.html', {})
            
        
        
# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

@login_required
def completeuserdetails(request):
    #check if the user details are completed
    if UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/try')
    else:
        if request.method=="POST":
            
            userdetails=UserDetailsForm(data=request.POST)
            
            if userdetails.is_valid():
    
                profile=userdetails.save(commit=False)
                profile.user=request.user
                if 'profile_picture' in request.FILES:
                    profile.profile_picture=request.FILES['profile_picture']
                    
                profile.save()
                
                return HttpResponseRedirect('/auth/try')
                
            else:
                
                print userdetails.errors
        else:
            userdetails=UserDetailsForm()
        
        #return render to response depending on the context
        return render(request,
                      "user_auth/userdetails.html",
                      {"userdetails": userdetails})
   
#closet upload cloth images
@login_required
def closet_upload(request):
    #check if the user details are completed
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        if request.method=="POST":
            
            clothdetails=ClothDescriptionForm(request.POST, request.FILES)
            
            if clothdetails.is_valid():
                
                cloth=clothdetails.save(commit=False)
                cloth.user=request.user
                if 'cloth_image' in request.FILES['cloth_image']:
                    cloth.cloth_image=request.FILES['cloth_image']
                cloth.save()
                messages.info(request, "Cloth Image and Description uploaded successfully")
                return HttpResponseRedirect('/auth/try')
                
            else:
                
                print clothdetails.errors
        else:
            clothdetails=ClothDescriptionForm()
            
        userdetails=UserDetails.objects.get(user=request.user)
        #return render to response depending on the context
        return render(request,
                      "user_auth/closet_upload.html",
                      {"clothform": clothdetails, 'userdetails': userdetails})




#add activity details view
@login_required
def add_user_activity(request):
    #check if the user details are completed
    
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        if request.method=="POST":
            
            activitydetails=UserActivityForm(data=request.POST)
            
            if activitydetails.is_valid():
    
                useractivity=activitydetails.save(commit=False)
                useractivity.user=request.user
                useractivity.save()
                messages.info(request, "Activity added successfully")
        
                return HttpResponseRedirect('/auth/user_activities')
                
            else:
                
                print activitydetails.errors
        else:
            activitydetails=UserActivityForm()
        
        userdetails=UserDetails.objects.get(user=request.user)
        
        #return render to response depending on the context
        return render(request,
                      "user_auth/add_user_activity.html",
                      {"activitydetails": activitydetails, 'userdetails': userdetails})
    
#view for activities 
@login_required
def user_activites(request):
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        user=UserDetails.objects.get(user=request.user)
        activities=UserActivity.objects.all().filter(user=request.user)
            
        return render(request,
                      'user_auth/user_activity.html',
                      {'activities': activities, 'userdetails': user})    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   