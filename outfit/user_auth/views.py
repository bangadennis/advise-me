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

##############################################################################################

def index(request):
    
    if request.user.is_authenticated():
        return HttpResponseRedirect('/auth/dash')
    
    return render(request, 'user_auth/base.html', {'active': 'active'})

##############################################################################################
#Dash/MyCloset
@login_required
def dash(request):
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        user=UserDetails.objects.get(user=request.user)
        cloths=ClothDescription.objects.all().filter(user=request.user).order_by('-id');
        if user.gender=="Female":
            category_1=["Top", "Shirt",]
            category_2=["Dress", "Mid-Length Dress", "Long Dress", "Mid-Length Skirt", "Long Skirt",
                        "Maxi Dress"]
            category_3=["Full Suit", "Suit Jacket"]
            category_4=["Jeans", "Pants", "Short"]
            category_5=["Rain Coat", "Blazer", "Cardigan", "Trench Coat", "Jacket", "Sweater"]
            category_6=["Scarf", "White Gloves", ""]
            
            clothobjects=[[],[],[],[],[],[],[]]
            for cloth in cloths:
                try:
                    usercloth=ClothFactBase.objects.get(cloth_id=cloth)
                    if usercloth.cloth_type in category_1:
                        clothobjects[0].append(cloth)
                    if usercloth.cloth_type in category_2:
                        clothobjects[1].append(cloth)
                    if usercloth.cloth_type in category_3:
                        clothobjects[2].append(cloth)
                    if usercloth.cloth_type in category_4:
                        clothobjects[3].append(cloth)
                    if usercloth.cloth_type in category_5:
                        clothobjects[4].append(cloth)
                    if usercloth.cloth_type in category_6:
                        clothobjects[5].append(cloth)
                          
                except:
                    clothobjects[6].append(cloth)  
            cloths=clothobjects
        else:
            #MALE
            category_1=["Shirt", "T-Shirt"]
            category_2=["Full Suit"]
            category_3=["Jeans", "Trouser", "Short"]
            category_4=["Rain Coat", "Blazer", "Cardigan", "Trench Coat", "Jacket", "Sweater"]
            category_5=["Scarf", "Gloves", ""]
            
            clothobjects=[[],[]]
            for cloth in cloths:
                try:
                    usercloth=ClothFactBase.objects.get(cloth_id=cloth)
                    if usercloth.cloth_type in category_1:
                        clothobjects[0].append(cloth)
                    if usercloth.cloth_type in category_2:
                        clothobjects[1].append(cloth)
                    if usercloth.cloth_type in category_3:
                        clothobjects[2].append(cloth)
                    if usercloth.cloth_type in category_4:
                        clothobjects[3].append(cloth)
                    if usercloth.cloth_type in category_5:
                        clothobjects[4].append(cloth)
                    if not usercloth.cloth_type:
                        clothobjects[6].append(cloth)    
                except:
                    pass
            cloths=clothobjects
            
        return render(request,
                      'user_auth/dash.html',
                      {'cloths': cloths, 'userdetails': user , 'active': 'home'})
    
##############################################################################################
#control panel-admin
@login_required
def admin_panel(request):
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        user=UserDetails.objects.get(user=request.user)
        if not request.user.is_superuser:
            messages.info(request, "Panel For Admins Only")
            return HttpResponseRedirect('/auth/dash')
            
            
        return render(request,
                      'user_auth/panel_reports.html',
                      {'userdetails': user , 'active': 'home'})
        



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

##############################################################################################
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
                last_logindate=user.last_login
                logintime=last_logindate.strftime("Date:%Y-%m-%d Time:%H:%M:%S")
                message="Last Login was at %s" %(logintime)
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
        return render(request, 'user_auth/login.html', {'active': 'login'})
            
        
##############################################################################################     
# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

##############################################################################################
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

##############################################################################################  
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
                      {"clothform": clothdetails, 'userdetails': userdetails
                       , 'active': 'upload' })

##############################################################################################
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

##############################################################################################
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
                      {"activitydetails": activitydetails, 'userdetails': userdetails
                       , 'active': 'add_activity'})

############################################################################################## 
#view for activities 
@login_required
def user_activites(request):
    if not UserDetails.objects.filter(user=request.user).exists():
        messages.info(request, "Complete User Details")
        return HttpResponseRedirect('/auth/userdetails')
    else:
        user=UserDetails.objects.get(user=request.user)
        activities=UserActivity.objects.all().filter(user=request.user).order_by("-event_date").order_by("start_time")
        
        if activities.count()==0:
            messages.info(request, "No Activities!, Add new activities")
            return HttpResponseRedirect('/auth/add_user_activity')
        
        weather=[]
        now = datetime.datetime.now()
        date=now.strftime("%Y-%m-%d")
        try:
            for item in activities:
                client=yweather.Client()
                if str(item.event_date)==str(date):
                    print(item.event_location)
                    weather_id=client.fetch_woeid(item.event_location)
                    print(weather_id)
                    
                    if weather_id is None:
                        weather_id=client.fetch_woeid('Nairobi,Kenya')
                    weather_st=client.fetch_weather(weather_id, metric=True)
                    weather.append(weather_st)
        except:
            messages.error(request, "No Internet Connection!")
            return HttpResponseRedirect('/auth/dash')
        #Adding the active activities
        display=[]
        for activity in activities:
            if str(activity.event_date)==str(date):
                display.append("active")
            elif str(activity.event_date)>str(date):
                display.append("info")
            else:
                display.append("danger")
            
        activities=zip(activities, display)
        
        return render(request,
                      'user_auth/user_activity.html',
                      {'activities': activities, 'userdetails': user, 'weather_st':weather
                       , 'active': 'activities'})
    
##############################################################################################
#delete activity
@login_required
def delete_activity(request):
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        if request.method=='GET':
            activity_id=request.GET['activity_id']
            if activity_id:
                user=User.objects.get(username=request.user.username)
                activity=user.useractivity_set.get(activity_id=activity_id)
                activity.delete()
                #messages.info(request, "Activity Deleted")
                #return HttpResponseRedirect('/auth/user_activities')
                return HttpResponse(activity_id)
    
############################################################################################## 
#add cloth facts
@login_required
def add_cloth_facts(request, cloth_id):
    #check if the user details are completed
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        userdetails=UserDetails.objects.get(user=request.user)
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
            cloth_fact=ClothFactForm(data=request.POST, user=userdetails)
            
            if cloth_fact.is_valid():
    
                cloth=cloth_fact.save(commit=False)
                cloth.cloth=cloth_data
                cloth.save()
                messages.info(request, "Cloth facts added successfully")
                return HttpResponseRedirect('/auth/dash')
                
            else:
                
                print cloth_fact.errors
        else:
            cloth_fact=ClothFactForm(user=userdetails)
        
        data=ClothFactBase.objects.filter(cloth_id=cloth_id).exists()
        facts={}
        if data:
            facts=ClothFactBase.objects.get(cloth_id=cloth_id)
        
        #return render to response depending on the context
        return render(request,
                      "user_auth/add_cloth_facts.html",
                      {'clothform': cloth_fact, 'userdetails': userdetails,
                       'cloth': cloth_data, 'clothfacts': facts , 'active': 'active'})
    
##############################################################################################
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

##############################################################################################
#Edit cloth details
@login_required
def update_cloth_facts(request, cloth_id):
    #check if the user details are completed
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        userdetails=UserDetails.objects.get(user=request.user)
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
            cloth_fact=ClothFactForm(data=request.POST, user=userdetails)
            
            if cloth_fact.is_valid():
                ClothFactBase.objects.get(cloth_id=cloth_id).delete()
                cloth=cloth_fact.save(commit=False)
                cloth.cloth=cloth_data
                cloth.save()
                messages.info(request, "Cloth facts updated successfully")
        
                return HttpResponseRedirect('/auth/dash')
                
            else:
                
                print cloth_fact.errors
        else:
            cloth_fact=ClothFactForm(user=userdetails)
        
        #return render to response depending on the context
        return render(request,
                      "user_auth/update_cloth_facts.html",
                      {"clothform": cloth_fact, 'userdetails': userdetails,
                       'cloth': cloth_data, })
  

##############################################################################################  
@login_required()
def todays_outfit(request):
    if not UserDetails.objects.filter(user=request.user).exists():
        messages.info(request, "Complete User Details")
        return HttpResponseRedirect('/auth/userdetails')
    else:
        
        userdetails=UserDetails.objects.get(user=request.user)
        try:
            activities=UserActivity.objects.all().filter(user=request.user).order_by('start_time')
            results=knowledge_engine(activities, request.user, userdetails)
            clothobjs=results['clothresults']
            activities=results['activities']
            weatherdata=results['weatherdata']
            
            datazip=zip(activities, clothobjs, weatherdata)   
                
        except:
            messages.error(request, "Unable to Connect to Yahoo Weather, Check Internet Connection")
            return HttpResponseRedirect('/auth/dash')
            
        
        list1=[(i)*3+1 for i in range(0,6)]
        list2=[i*3 for i in range(1,6)]
        ui_list=[list1, list2]
        return render(request,
                      "user_auth/index.html",
                      {"activities": datazip, 'userdetails':
                        userdetails, 'active': 'index', "ui_list": ui_list })
            
        
        
        
##############################################################################################     
#Knowledge Engine
def knowledge_engine(activities, user, userdetail):
    """Knwoledge Engine"""
   # json_data = json.loads(open(KB).read())
    
    try:
        data=check_todays_activity(activities)
        weather=data["weather"]
        activitytypes=data["activitytype"]
        weatherdata=data["weatherdata"]
    except:
        messages.error(request, "Unable to Connect to Weather Server!")
        return HttpResponseRedirect('/auth/dash')
    
    #Check the weather conditions   
        #check the weather conditions
    print(weather)
    print(activitytypes)
    wcondition=[]
    for weather_data in weather:
        if int(weather_data['temp'])>=17:
            wcondition.append("hot")
        elif int(weather_data['temp'])<17:
            wcondition.append("cold")
        #to be changed
        elif lower(weather_data['text']) in ["rain", "rain and snow"] and weather_data['temp']<15:
            wcondition.append("rainy")
        else:
             pass
        #wcondition="hot"
        
            
    cloths=ClothDescription.objects.all().filter(user=user)
    clothobjects=[]
    
    #Fetching the cloths' facts
    for cloth in cloths:
                clothfactobj=cloth.clothfactbase_set.all()
                try:
                    usercloth=ClothFactBase.objects.get(cloth_id=cloth)
                    clothobjects.append(usercloth)
                except:
                    pass
                
    
    #Select Matching function to either male or female outfit
    daysoutfits=[]
    lock=True
    if userdetail.gender=="Female":
        try:
            count=0
            for activitytype in activitytypes:
                daysoutfits.append(outfit_rules_female(clothobjects, wcondition[count], activitytype.category))
                count=count+1
        except:
            lock=False
            
    else:
        count=0
        for activitytype in activitytypes:
            daysoutfits.append(outfit_rules_male(clothobjects, wcondition[count], activitytype.category))
            count=count+1
    
    #Getting the clothes' description
    clothresults=[]
    if lock:
        for dayoutfit in daysoutfits:
            temp=[]
            for outfit in dayoutfit:
                clothobj=ClothDescription.objects.get(id=outfit.cloth_id)
                temp.append(clothobj)
                print(outfit.cloth_id)
            clothresults.append(temp)
    
    
    return {"clothresults": clothresults, "activities": activitytypes,
            "weatherdata": weatherdata, }

##############################################################################################
#Fuction to check if there is an activity and the weather conditions
def check_todays_activity(activities):
    """This function checks the day's activity"""
    now = datetime.datetime.now()
    date=now.strftime("%Y-%m-%d")
    event=0
    activitytype=[]
    weather=[]
    count=0
    weatherdata=[]
    for activity in activities:
        print(activity.category)
        if str(activity.event_date)==str(date):
            client=yweather.Client()
            weather_id=client.fetch_woeid(activity.event_location)
            if weather_id is None:
                weather_id=client.fetch_woeid('Nairobi,Kenya')
            weather_st=client.fetch_weather(weather_id, metric=True)
            weather.append(weather_st['condition'])
            weatherdata.append(weather_st)
            #append activity type
            activitytype.append(activity)
            count=count+1
            event=1

    print(activitytype)
    return {"weather": weather,"activitytype": activitytype, "weatherdata": weatherdata}
    
    
##############################################################################################
#rules for females' outfit
def outfit_rules_female(clothobjects, weathercondition, activitytype):
    """Rules to Match Females Outfit"""
    selectedCloths=[]
    HotWeatherMaterial=['Silk', 'Linen', 'Ramie', 'Jute', 'Hemp', 'Bamboo',  'Cotton', 'Chiffon']
    print(weathercondition)
    for clothobj in clothobjects:
        if weathercondition in ["hot", 'cold', 'rain']:
            #Material for Hot Weather
            if clothobj.cloth_material in HotWeatherMaterial:
                #Job Interview Occassion Cloths Type
                if (activitytype=="Job Interview" or activitytype=="School Event" or activitytype=="Business Formal" ):
                    cloth_colors=["Gray", "Black", "Navy", "Brown", "Blue"]
                    #Check the appropiate cloth
                    if (clothobj.cloth_type=="Full Suit"):
                        selectedCloths.append(clothobj)
                    
                    if (clothobj.cloth_type=="Mid-Length Skirt" and clothobj.cloth_color in cloth_colors and clothobj.cloth_print=="Plain"):
                        selectedCloths.append(clothobj)
                        
                    if (clothobj.cloth_type=="Pants" and clothobj.cloth_color in cloth_colors and clothobj.cloth_print=="Plain"):
                        selectedCloths.append(clothobj)
                        
                    if (clothobj.cloth_type=="Mid-length Dress" and clothobj.cloth_print=="Plain"):
                        selectedCloths.append(clothobj)
                        
                    if ((clothobj.cloth_type=="Blazer" or clothobj.cloth_type=="Suit Jacket") and
                    (clothobj.cloth_print=="Plain")):
                        selectedCloths.append(clothobj)
                        
                    if ((clothobj.cloth_type=="Blouse") and (clothobj.cloth_print=="Plain" or
                    clothobj.cloth_print=="Stripped")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Top") and (clothobj.cloth_print=="Plain" or
                    clothobj.cloth_print=="Stripped")):
                        selectedCloths.append(clothobj)
                
                #Activity Shopping/ CasualDay Out
                if activitytype=="Shopping":
                    if (clothobj.cloth_type=="Jeans"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Top"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Cardigan"):
                        selectedCloths.append(clothobj)
                
                #Activity Date
                if activitytype=="Date":
                    if (clothobj.cloth_type=="Top"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Jeans"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Mid-Length Dress"):
                        selectedCloths.append(clothobj)
                #Activity Wedding
                if activitytype=="Wedding":
                    if (clothobj.cloth_type=="Maxi Dress"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Brim hat"):
                        selectedCloths.append(clothobj)
                
                #Activity Semi Formal/Cocktail
                if activitytype=="Cocktail":
                    if ((clothobj.cloth_type=="Short Dress") and (clothobj.cloth_color=="Black")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Mid-Length Dress")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Blouse") and (clothobj.cloth_material=="Silk")):
                        selectedCloths.append(clothobj)
    
                #Activity Formal/Black Tie
                if activitytype=="Black Tie":
                    if (clothobj.cloth_type=="Long Dress"):
                        selectedCloths.append(clothobj)
                #Activity White Tie
                if activitytype=="White Tie":
                    if (clothobj.cloth_type=="Long Dress"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="White Gloves"):
                        selectedCloths.append(clothobj)
                #Activity  Church/Religious Events
                if activitytype=="Religious":
                    if (((clothobj.cloth_type=="Long Dress") or (clothobj.cloth_type=="Mid-Length Dress"))
                    and((clothobj.cloth_color in ['Red', 'Orange', 'Blue', 'Pink', 'Peach','Multi-Color','Yellow'])
                    or (clothobj.cloth_print=="Floral"))):
                        selectedCloths.append(clothobj)
                    
                    if (((clothobj.cloth_type=="Long Skirt") or (clothobj.cloth_type=="Mid-Length Skirt"))
                    and (((clothobj.cloth_color in ['Red', 'Orange', 'Blue', 'Pink', 'Peach', 'Yellow'])
                    and (clothobj.cloth_print=="Floral") ))):
                        selectedCloths.append(clothobj)
                        
                    if (clothobj.cloth_type in ["Blouse", "Top"]):
                        selectedCloths.append(clothobj)
                #Activity Business Formal
               
               
               
         #########################################
            #clothes for cold days
            if weathercondition=="cold":
                if ((clothobj.cloth_type in ['Cardigan', 'Sweater', 'Jacket', 'Scarf', 'Gloves','Trench Coat']) and
                (clothobj.cloth_material in ['Wool', 'Cashmere'])):
                    selectedCloths.append(clothobj)
            #clothes for rainy days
            if weathercondition=="rainy":
                  if (clothobj.cloth_type in ['Cardigan', 'Sweater', 'Jacket', 'Scarf', 'Gloves','Rain Coat']):
                    selectedCloths.append(clothobj)
                   
    print(selectedCloths)   
    return selectedCloths

##############################################################################################
#rules to match Males'  outfit
def outfit_rules_male(clothobjects, weathercondition, activitytype):
    selectedCloth=[]
    HotWeatherMaterial=['Silk', 'Linen', 'Ramie', 'Jute', 'Hemp', 'Bamboo',  'Cotton', 'Chiffon']
    
    for clothobj in clothobjects:
        if weathercondition in ["hot", "cold"]:
            #Material for Hot Weather
            if clothobj.cloth_material in HotWeatherMaterial:
                #Job Interview Occassion Clothes Type
                if (activitytype=="Job Interview"or activitytype=="School Event" or activitytype=="Business Casual"
                    or activitytype=="Business Formal"):
                    cloth_colors=["Gray", "Black", "Navy", "Brown", "Blue"]
                    #Check the appropiate cloth
                    if (clothobj.cloth_type=="Full Suit"):
                        selectedCloths.append(clothobj)
                    
                    if (clothobj.cloth_type=="Trouser" and clothobj.cloth_color in cloth_colors and clothobj.cloth_print=="Plain"):
                        selectedCloths.append(clothobj)
                        
                    if ((clothobj.cloth_type=="Blazer" or clothobj.cloth_type=="Suit Jacket") and
                    (clothobj.cloth_print=="Plain")):
                        selectedCloths.append(clothobj)
                        
                    if ((clothobj.cloth_type=="Shirt") and (clothobj.cloth_print=="Plain" or
                    clothobj.cloth_print=="Stripped")):
                        selectedCloths.append(clothobj)
                
                #Activity Shopping/ CasualDay Out
                if activitytype=="Shopping":
                    if (clothobj.cloth_type in ["Jeans","Short"]):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="T-Shirt"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Cardigan"):
                        selectedCloths.append(clothobj)
                
                #Activity Date
                if activitytype=="Date":
                    if (clothobj.cloth_type=="T-Shirt"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Jeans"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Cardigan"):
                        selectedCloths.append(clothobj)
                #Activity Wedding
                if activitytype=="Wedding":
                    if (clothobj.cloth_type=="Trouser"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Full Suit"):
                        selectedCloths.append(clothobj)
                
                #Activity Semi Formal/Cocktail
                if activitytype=="Cocktail":
                    if ((clothobj.cloth_type=="Short Dress") and (clothobj.cloth_color=="Black")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Full Suit")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Shirt") and (clothobj.cloth_print=="plain")):
                        selectedCloths.append(clothobj)
    
                #Activity Formal/Black Tie
                if activitytype=="Black Tie":
                    if (clothobj.cloth_type=="Long Dress"):
                        selectedCloths.append(clothobj)
                #Activity White Tie
                if activitytype=="White Tie":
                    if ((clothobj.cloth_type=="Full Suit") and
                    (clothobj.color_=="Black")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Shirt") and
                    (clothobj.cloth_color=="White")):
                        selectedCloths.append(clothobj)
                #Activity  Church/Religious Events
                if activitytype=="Religious":
                    if ((clothobj.cloth_type=="Jeans") or (clothobj.cloth_type=="T-Shirt")):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type in ["Trouser", "Cardigan"]):
                        selectedCloths.append(clothobj)
                #Activity Business Formal
                   
    #print(selectedCloths)   
    return selectedCloths

#Function to Sort the selected clothes
def sortclothes(selectedclothes):
    #sort throught the clothes
    pass
        


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   