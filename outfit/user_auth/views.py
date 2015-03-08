from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator

from user_auth.forms import UserForm, UserDetailsForm, ClothDescriptionForm, UserActivityForm, ClothFactForm
from models import UserDetails, ClothDescription, UserActivity, ClothFactBase
#weather api
import yweather
#datetime
import datetime
#json
import json
#os
import os
#Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#KnowledgeBase
KB=os.path.join(BASE_DIR, 'static/knowledgebase/kb.json')

def index(request):
    
    if request.user.is_authenticated():
        return HttpResponseRedirect('/auth/dash')
    
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'message': "Welcome to Outfit.com", }

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'user_auth/base.html', context_dict)

#trial of google api
def google(request):
    return render(request, 'user_auth/google.html', {})



@login_required
def dash(request):
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        hello="Welcome, to Our Outfit Expert System:"
        user=UserDetails.objects.get(user=request.user)
        cloths=ClothDescription.objects.all().filter(user=request.user)
            
        return render(request,
                      'user_auth/dash.html',
                      {'cloths': cloths, 'userdetails': user})
    
    
#registration view
def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/auth/dash')
    
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
        return HttpResponseRedirect('/auth/dash')
    
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
                message="Last Login was at %s" %(user.last_login)
                messages.info(request, message)
                return HttpResponseRedirect('/auth/dash')
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
            return HttpResponseRedirect('/auth/dash')
    else:
        if request.method=="POST":
            
            userdetails=UserDetailsForm(data=request.POST)
            
            if userdetails.is_valid():
    
                profile=userdetails.save(commit=False)
                profile.user=request.user
                if 'profile_picture' in request.FILES:
                    profile.profile_picture=request.FILES['profile_picture']
                    
                profile.save()
                
                return HttpResponseRedirect('/auth/dash')
                
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
        messages.info(request, "Complete User Details")
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
                messages.info(request, "Cloth's Image and Description uploaded successfully")
                return HttpResponseRedirect('/auth/get_facts/{}/view'.format(cloth.id))
                
            else:
                
                print clothdetails.errors
        else:
            clothdetails=ClothDescriptionForm()
            
        userdetails=UserDetails.objects.get(user=request.user)
        #return render to response depending on the context
        return render(request,
                      "user_auth/closet_upload.html",
                      {"clothform": clothdetails, 'userdetails': userdetails})


#edit userdetails
class UserDetailsUpdate(UpdateView):
    model=UserDetails
    form_class= UserDetailsForm
    success_url = reverse_lazy('trya')
    
    @method_decorator(login_required)
    def get(self, request, **kwargs):
        self.object = UserDetails.objects.get(user=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)
    
    #@method_decorator(login_required)
    #def form_valid(self, form):
    #    messages.info(self.request, "updated profile successfully")
    #    return super(UserDetailsUpdate, self).form_valid(form)

#add activity details view
@login_required
def add_user_activity(request):
    #check if the user details are completed
    
    if not UserDetails.objects.filter(user=request.user).exists():
        messages.info(request, "Complete User Details")
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
        messages.info(request, "Complete User Details")
        return HttpResponseRedirect('/auth/userdetails')
    else:
        user=UserDetails.objects.get(user=request.user)
        activities=UserActivity.objects.all().filter(user=request.user).order_by("-event_date")
        
        if activities.count()==0:
            messages.info(request, "No Activities")
            return HttpResponseRedirect('/auth/dash')
        
        weather=[]
        now = datetime.datetime.now()
        date=now.strftime("%Y-%m-%d")
        for item in activities:
            client=yweather.Client()
            if str(item.event_date)==str(date):
                print(item.event_location)
                weather_id=client.fetch_woeid(item.event_location)
                print(weather_id)
                
                if weather_id is None:
                    weather_id=client.fetch_woeid('Nairobi,Kenya')
                weather_st=client.fetch_weather(weather_id)
                weather.append(weather_st)
                
        return render(request,
                      'user_auth/user_activity.html',
                      {'activities': activities, 'userdetails': user, 'weather_st':weather}) 
#delete activity
@login_required
def delete_activity(request, activity_id):
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        if activity_id:
            try:
                user=User.objects.get(username=request.user.username)
                activity=user.useractivity_set.get(activity_id=activity_id)
                activity.delete()
                
                messages.info(request, "Activity Deleted")
                return HttpResponseRedirect('/auth/user_activities')
            except:
                messages.info(request, "Invalid Delete Activity Option")
                return HttpResponseRedirect('/auth/user_activities/')   
    
    
#add cloth facts
@login_required
def add_cloth_facts(request, cloth_id):
    #check if the user details are completed
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        if cloth_id:
            user=User.objects.get(username=request.user.username)
            try :
                cloth_data=user.clothdescription_set.get(id=cloth_id)
            except:
                messages.error(request, "Invalid Option")
                return HttpResponseRedirect('/auth/dash') 
                
        else:
            return HttpResponseRedirect('auth/dash')
        if request.method=="POST":
            cloth_fact=ClothFactForm(data=request.POST)
            
            if cloth_fact.is_valid():
    
                cloth=cloth_fact.save(commit=False)
                cloth.cloth_id=cloth_data
                cloth.save()
                messages.info(request, "Cloth facts added successfully")
        
                return HttpResponseRedirect('/auth/dash')
                
            else:
                
                print cloth_fact.errors
        else:
            cloth_fact=ClothFactForm()
        
        userdetails=UserDetails.objects.get(user=request.user)
        data=ClothFactBase.objects.filter(cloth_id=cloth_id).exists()
        facts={}
        if data:
            facts=ClothFactBase.objects.get(cloth_id=cloth_id)
        
        #return render to response depending on the context
        return render(request,
                      "user_auth/add_cloth_facts.html",
                      {"clothform": cloth_fact, 'userdetails': userdetails,
                       'cloth': cloth_data, 'clothfacts': facts})
    

#delete a cloth
@login_required
def delete_cloth(request, cloth_id):
    #check if the user details are completed
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        if cloth_id:
            user=User.objects.get(username=request.user.username)
            try :
                cloth_data=user.clothdescription_set.get(id=cloth_id)
                cloth_data.delete()
                messages.info(request, "Cloth deleted")
                return HttpResponseRedirect('/auth/dash') 
                
            except:
                messages.error(request, "Invalid Option")
                return HttpResponseRedirect('/auth/dash') 


#Edit cloth details
@login_required
def update_cloth_facts(request, cloth_id):
    #check if the user details are completed
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        
        if cloth_id:
            user=User.objects.get(username=request.user.username)
            try :
                cloth_data=user.clothdescription_set.get(id=cloth_id)
            except:
                messages.error(request, "Invalid Option")
                return HttpResponseRedirect('/auth/dash') 
                
        else:
            return HttpResponseRedirect('auth/dash')
        
        if request.method=="POST":
            cloth_fact=ClothFactForm(data=request.POST)
            
            if cloth_fact.is_valid():
                ClothFactBase.objects.get(cloth_id=cloth_id).delete()
                cloth=cloth_fact.save(commit=False)
                cloth.cloth_id=cloth_data
                cloth.save()
                messages.info(request, "Cloth facts updated successfully")
        
                return HttpResponseRedirect('/auth/dash')
                
            else:
                
                print cloth_fact.errors
        else:
            cloth_fact=ClothFactForm()
        userdetails=UserDetails.objects.get(user=request.user)
        #return render to response depending on the context
        return render(request,
                      "user_auth/update_cloth_facts.html",
                      {"clothform": cloth_fact, 'userdetails': userdetails,
                       'cloth': cloth_data, })
    
@login_required()
def todays_outfit(request):
    if not UserDetails.objects.filter(user=request.user).exists():
        messages.info(request, "Complete User Details")
        return HttpResponseRedirect('/auth/userdetails')
    else:
        
        userdetails=UserDetails.objects.get(user=request.user)
        activities=UserActivity.objects.all().filter(user=request.user)
        try:
            clothobj=knowledge_engine(activities, request.user, userdetails)
        except:
            messages.error(request, "Unable to Connect to Yahoo Weather, Check Internet Connection")
            return HttpResponseRedirect('/auth/dash')
            
        
        return render(request,
                      "user_auth/index.html",
                      {"cloths": clothobj, 'userdetails': userdetails})
            
        
        
        
        
#Knowledge Engine
def knowledge_engine(activities, user, userdetail):
    """Knwoledge Engine"""
   # json_data = json.loads(open(KB).read())
    
    try:
        data=check_todays_activity(activities)
    except:
        pass
       # messages.error(request, "No Event/Unable to Connect to Yahoo Weather, Check Internet Connection")
       # return HttpResponseRedirect('/auth/dash')
         
    
    #Check the weather conditions   
    if not data:
        daysoutfit={}
    else:
        weather_data=data["weather"]
        activitytype=data["activitytype"]
        
        if int(weather_data['temp'])>=69:
            wcondition="hot"
        elif int(weather_data['temp'])<69:
            wcondition="hot"
        elif weather_data['text']=="rainy":
            wcondition="rainy"
        else:
            wcondition="hot"
        
            
    cloths=ClothDescription.objects.all().filter(user=user)
    clothobjects=[]
    clothresults=[]
    for cloth in cloths:
                clothfactobj=cloth.clothfactbase_set.all()
                try:
                    usercloth=ClothFactBase.objects.get(cloth_id=cloth)
                    print(usercloth.cloth_type)
                    clothobjects.append(usercloth)
                except:
                    pass
    
    if userdetail.gender=="Female": 
        daysoutfit=outfit_rules_male(clothobjects, wcondition, activitytype);
        print("HeLLOO")
        for outfit in daysoutfit:
            clothobj=ClothDescription.objects.get(id=outfit.cloth_id)
            clothresults.append(clothobj)
            print(outfit.cloth_id)
    else:
        pass
    
    return clothresults
    

#rules for males' outfit
def outfit_rules_male(clothobjects, weathercondition, activitytype):
    selectedCloths=[]
    for clothobj in clothobjects:
       # print(clothobj.cloth_print)
        if weathercondition=="hot":
            if activitytype:
                print("dddddddd")
                if clothobj.cloth_print in ["plain",]:
                    print(clothobj.cloth_id)
                    selectedCloths.append(clothobj);
    
    return selectedCloths
        

#Fuction to check if there is an activity and the weather conditions
def check_todays_activity(activities):
    """This function checks the day's activity"""
    now = datetime.datetime.now()
    date=now.strftime("%Y-%m-%d")
    event=0
    activitytype=[]
   
    for activity in activities:
        if str(activity.event_date)==str(date):
            client=yweather.Client()
            weather_id=client.fetch_woeid(activity.event_location)
            if weather_id is None:
                weather_id=client.fetch_woeid('Nairobi,Kenya')
            weather_st=client.fetch_weather(weather_id)
            weather=weather_st['condition']
            activitytype.append(activity.category)
            event=1
            break;
    
    if event:
        return {"weather": weather,"activitytype": activitytype}
    else:
        ret
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   