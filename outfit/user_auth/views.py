from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin



from user_auth.forms import UserForm, UserDetailsForm, ClothDescriptionForm, UserActivityForm, ClothFactForm
from models import UserDetails, ClothDescription, UserActivity, ClothFactBase
#weather api
import yweather
#datetime
import datetime
#json
import urllib2, urllib, json
#os
import os
import random
#charts
from chartit import DataPool, Chart


baseurl_weather_api = "https://query.yahooapis.com/v1/public/yql?"
#Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#KnowledgeBase
KB=os.path.join(BASE_DIR, 'static/knowledgebase/kb.json')

##############################################################################################

def index(request):
    
    if request.user.is_authenticated():
        return HttpResponseRedirect('/auth/dash')
    
    return render(request, 'user_auth/base.html', {'active': 'home'})

##############################################################################################
#search closet
def search_closet(request):
    if request.method=='GET':
        search_name=request.GET['search_name']
        if search_name:
            temp=[]
            username=User.objects.get(username=request.user.username)
            user=UserDetails.objects.get(user=username)
            cloths=ClothDescription.objects.all().filter(user=username)
            results=cloths.filter(cloth_description__icontains=search_name)
            
            for cloth in results:
                temp.append(cloth)
            
            if True:
                for cloth in cloths:
                    
                    result=(cloth.clothfactbase_set.filter(cloth_material__icontains=search_name).exists() or
                            cloth.clothfactbase_set.filter(cloth_type__icontains=search_name).exists() or
                            cloth.clothfactbase_set.filter(cloth_print__icontains=search_name).exists() or
                            cloth.clothfactbase_set.filter(cloth_color__icontains=search_name).exists() )
                    if result:
                        temp.append(cloth)  
        return render(request,
                      'user_auth/search_dash_list.html',
                      {'cloths': temp})
#Dash/MyCloset
@login_required
def dash(request):
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        user=UserDetails.objects.get(user=request.user)
        cloths=ClothDescription.objects.all().filter(user=request.user).order_by('-id');
        countcloth=ClothDescription.objects.all().filter(user=request.user).count();
        if user.gender=="Female":
            category_1=["Top", "Shirt","Blouse", "Turtleneck"]
            category_2=["Dress", "Mid-Length Dress", "Long Dress", "Mid-Length Skirt", "Long Skirt",
                        "Maxi Dress"]
            category_3=["Full Suit", "Suit Jacket"]
            category_4=["Jeans", "Pants", "Short", "Khakis"]
            category_5=["Rain Coat", "Blazer", "Cardigan", "Trench Coat", "Jacket", "Sweater"]
            category_6=["Scarf", "White Gloves", ""]
            
            clothobjects=[[],[],[],[],[],[],[]]
            group=["Shirts,Tops", "Dresses/Skirts","Suits", "Pants", "Coat/Sweater","Scarf/Gloves","Uncategorized"]
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
            clothes=zip(clothobjects,group)
            
        else:
            #MALE
            
            category_1=["Shirt", "T-Shirt",'Polo Shirt', 'Dressy Shirt',"Turtleneck"]
            category_2=["Full Suit"]
            category_3=["Jeans", "Trouser", "Short","Khakis",]
            category_4=["Rain Coat", "Blazer", "Cardigan", "Trenchcoat", "Jacket", "Sweater",
                        "Sport Coat", "Waistcoat", "Tailcoat"]
            category_5=["Scarf","Gloves", "Hat"]
            
            clothobjects=[[],[],[],[],[],[]]
            group=["Shirts,T-Shirt", "Suits", "Pants", "Coat/Sweater", "Scarf/Gloves","Uncategorized"]
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
                        clothobjects[5].append(cloth)    
                except:
                    pass
            clothes=zip(clothobjects,group)
            
        return render(request,
                      'user_auth/dash.html',
                      {'cloths': clothes, 'userdetails': user ,"countcloth":countcloth, 'active': 'dash'})
    
##############################################################################################
#control panel-admin
@login_required
def admin_panel(request):
    if not UserDetails.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/auth/userdetails')
    else:
        user=UserDetails.objects.get(user=request.user)
        all_activities=UserActivity.objects.all()
        if not request.user.is_superuser:
            messages.info(request, "Panel For Admins Only")
            return HttpResponseRedirect('/auth/dash')
        else:
            userslist=[]
            calculations={}
            now = datetime.datetime.now()
            date=now.strftime("%Y-%m-%d")
            users=User.objects.all()
            sumactivities=0
            sumtodays=0
            sumclothes=0
            count=0
            for userobj in users:
                user=UserDetails.objects.get(user=userobj)
                totalclothes=ClothDescription.objects.all().filter(user=userobj).count()
                print(totalclothes)
                totalactivities=UserActivity.objects.all().filter(user=userobj).count()
                todayactivities=UserActivity.objects.all().filter(user=userobj).filter(event_date=date).count()
                sumactivities=sumactivities+totalactivities
                sumtodays=sumtodays+todayactivities
                sumclothes=sumclothes+totalclothes
                print(todayactivities)
                panellist=[userobj, totalclothes, totalactivities, todayactivities, user]
                userslist.append(panellist)
                count=count+1
            averageactivities=sumactivities/count;
            averageclothes=sumclothes/count
            averagetoday=sumtodays/count
            
            
            calculations={"totalA": sumactivities, "totalT": sumtodays, "totalC": sumclothes,
                          "avgA": averageactivities, "avgT": averagetoday, "avgC": averageclothes,
                          }
    

        return render(request,
                      'user_auth/panel_reports.html',
                      {'userdetails': user ,'userslist':userslist,
                       "calculations": calculations, "all_activities":all_activities})
        

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
            invalid="Invalid login details"
            #return HttpResponse("Invalid login details supplied.")
            return render(request, 'user_auth/login.html', {"invalid": invalid})

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
                
                messages.info(request, "Welcome to Outfit!")
                return HttpResponseRedirect('/auth/dash')
                
            else:  
                print userdetails.errors
        else:
            userdetails=UserDetailsForm()
        
        #return render to response depending on the context
        return render(request,
                      "user_auth/userdetails.html",
                      {"userdetail": userdetails})

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
                       , 'active': 'closet_upload' })

##############################################################################################
#edit userdetails
class UserDetailsUpdate(SuccessMessageMixin,UpdateView):
    model=UserDetails
    form_class= UserDetailsForm
    success_url = reverse_lazy('trya')
    success_messsage="profile updated successfully"
    
    @method_decorator(login_required)
    def get(self, request, **kwargs):
        self.object = UserDetails.objects.get(user=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form, active='index')
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
                       , 'active': 'add_user_activity'})

############################################################################################## 
#view for activities 
@login_required
def user_activites(request):
    if not UserDetails.objects.filter(user=request.user).exists():
        messages.info(request, "Complete User Details")
        return HttpResponseRedirect('/auth/userdetails')
    else:
        user=UserDetails.objects.get(user=request.user)
        activities=UserActivity.objects.all().filter(user=request.user).order_by("start_time").order_by("-event_date")
        
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
                    
                    yql_query = "select * from weather.forecast where woeid=%s" %(weather_id)
                    yql_url = baseurl_weather_api + urllib.urlencode({'q':yql_query}) + "&format=json"
                    result = urllib2.urlopen(yql_url).read()
                    data = json.loads(result)
                    weather_st=data['query']['results']['channel']['item']
                    weather.append(weather_st)
        except:
            messages.error(request, "No Internet Connection!")
            return HttpResponseRedirect('/auth/dash')
        #Adding the active activities
        display=[]
        for activity in activities:
            if str(activity.event_date)==str(date):
                display.append("success")
            elif str(activity.event_date)>str(date):
                display.append("info")
            else:
                display.append("danger")
            
        activities=zip(activities, display)
        
        return render(request,
                      'user_auth/user_activity.html',
                      {'activities': activities, 'userdetails': user, 'weather_st':weather
                       , 'active': 'user_activities'})
    
##############################################################################################

#edit userdetails
class UserActivityUpdate(SuccessMessageMixin,UpdateView):
    model=UserActivity
    form_class= UserActivityForm
    template_name="user_auth/user_activity_form.html"
    success_url = reverse_lazy('user_activities')
    success_message="Activity/Event updated sucessfully"

    
    @method_decorator(login_required)
    def get(self, request, **kwargs):
        self.object = UserActivity.objects.get(activity_id=self.kwargs['pk'])
        userdetails=UserDetails.objects.get(user=request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form, userdetails=userdetails, active='user_activities')
        return self.render_to_response(context)

################################################################################################
 #delete activity
@login_required
def delete_activity(request):
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
                       'cloth': cloth_data, 'clothfacts': facts , 'active': 'dash'})
    
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
#Edit cloth's details
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
                       'cloth': cloth_data, 'active': 'dash'})
  

##############################################################################################  
@login_required()
def todays_outfit(request):
    if not UserDetails.objects.filter(user=request.user).exists():
        messages.info(request, "Complete User Details")
        return HttpResponseRedirect('/auth/userdetails')
    else:
        
        userdetails=UserDetails.objects.get(user=request.user)
        try:
            activities=UserActivity.objects.all().filter(user=request.user).order_by('start_time').order_by('event_date')
            results=knowledge_engine(activities, request.user, userdetails)
            clothobjs=results['clothresults']
            activities=results['activities']
            weatherdata=results['weatherdata']
            message=results['message']
            
            #formatting activities with date
            now = datetime.datetime.now()
            date=now.strftime("%Y-%m-%d")
            display=[]
            for activity in activities:
                if str(activity.event_date)==str(date):
                    display.append("panel-success")
                elif str(activity.event_date)>str(date):
                    display.append("panel-info")
                else:
                    pass
            
        
            datazip=zip(activities, clothobjs, weatherdata, display, message)   
                
        except:
            messages.error(request, "Unable to Connect to Yahoo Weather, Check Internet Connection")
            return HttpResponseRedirect('/auth/dash')
            
        #for displaying the selected clothes 3 objects per row
        list1=[(i)*3+1 for i in range(0,6)]
        list2=[i*3 for i in range(1,6)]
        ui_list=[list1, list2]
        
        return render(request,
                      "user_auth/index.html",
                      {"activities": datazip, 'userdetails':
                        userdetails, 'active': 'daysoutfit', "ui_list": ui_list })
            
        
        
        
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
        return False
    
    #Check the weather conditions   
        #check the weather conditions
    
    print(weather)
    #print(activitytypes)
    wcondition=[]
    for weather_data in weather:
        if (int(weather_data['temp'])>17):
            wcondition.append("hot")
        elif (int(weather_data['temp'])<=17 ):
            wcondition.append("cold")
        #to be changed
        elif("rain" in lower(weather_data['text'])) and (weather_data['temp']<25):
            wcondition.append("rainy")
        else:
             pass
    
        
         
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
    message=[]
    lock=True
    if userdetail.gender=="Female":
        try:
            count=0
            for activitytype in activitytypes:
                results=outfit_rules_male(clothobjects, wcondition[count], activitytype.category)
                print(results)
                message.append(results['message'])
                daysoutfits.append(results['clothobjs'])
                count=count+1
                #daysoutfits.append(outfit_rules_female(clothobjects, wcondition[count], activitytype.category))
                #count=count+1
        except:
            lock=False
            
    else:
        try:
            count=0
            message=[]
            for activitytype in activitytypes:
                results=outfit_rules_male(clothobjects, wcondition[count], activitytype.category)
                print(results)
                message.append(results['message'])
                daysoutfits.append(results['clothobjs'])
                count=count+1
        except:
            lock=False
    
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
            "weatherdata": weatherdata, "message":message }

##############################################################################################
#Fuction to check if there is an activity and the weather conditions
def check_todays_activity(activities):
    """This function checks the day's activity"""
    now = datetime.datetime.now()
    todays_date=now.strftime("%Y-%m-%d")
    try:
        start_date=datetime.datetime.strptime(todays_date,"%Y-%m-%d")
        #Adding 5 days
        end_date= start_date+datetime.timedelta(days=5)
        
        start_date=datetime.datetime.strftime(start_date,"%Y-%m-%d")
        end_date=datetime.datetime.strftime(end_date,"%Y-%m-%d")
       
    except:
        pass
    
    activitytype=[]
    weather=[]
    weatherdata=[]
    
    for activity in activities:
        print(activity.category)
        if str(activity.event_date)==str(todays_date):
            client=yweather.Client()
            weather_id=client.fetch_woeid(activity.event_location)
            if weather_id is None:
                weather_id=client.fetch_woeid('Nairobi,Kenya')
            
            yql_query = "select * from weather.forecast where woeid=%s" %(weather_id)
            yql_url = baseurl_weather_api + urllib.urlencode({'q':yql_query}) + "&format=json"
            result = urllib2.urlopen(yql_url).read()
            data = json.loads(result)
            weather_st=data['query']['results']['channel']['item']
            weather.append(weather_st['condition'])
            weatherdata.append(weather_st)
            #append activity type
            activitytype.append(activity)
            
        elif (str(activity.event_date)>str(todays_date) and str(activity.event_date)<str(end_date)):
            client=yweather.Client()
            weather_id=client.fetch_woeid(activity.event_location)
            if weather_id is None:
                weather_id=client.fetch_woeid('Nairobi,Kenya')
            yql_query = "select * from weather.forecast where woeid=%s" %(weather_id)
            yql_url = baseurl_weather_api + urllib.urlencode({'q':yql_query}) + "&format=json"
            result = urllib2.urlopen(yql_url).read()
            data = json.loads(result)
            weather_st=data['query']['results']['channel']['item']
            print(weather_st)
            for forecast in weather_st['forecast']:
                #formating the date form d/m/Y to Y/m/d
                forecast_date=datetime.datetime.strptime(forecast['date'],"%d %b %Y")
                forecast_date=datetime.datetime.strftime(forecast_date,"%Y-%m-%d")
                if forecast_date==str(activity.event_date):
                    temp=forecast['low']
                    text=forecast['text']
                    date=forecast['date']
                    details={"temp": temp, "text": text, "date": date}
                    weather.append(details)
                    print("Okay")
            weatherdata.append(details)
            #append activity type
            activitytype.append(activity)
        else:
            pass
            
    print(activitytype)
    return {"weather": weather,"activitytype": activitytype, "weatherdata": weatherdata}
    
    
##############################################################################################
#rules for females' outfit
def outfit_rules_female(clothobjects, weathercondition, activitytype):
    """Rules to Match Females Outfit"""
    selectedCloths=[]
    HotWeatherMaterial=['Silk', 'Linen', 'Ramie', 'Jute', "Denim",'Hemp', 'Bamboo',  'Cotton', 'Chiffon']
    cloth_colors=["Gray", "Black", "Navy", "Brown", "Blue","White"]
     
    print(weathercondition)
    for clothobj in clothobjects:
        if weathercondition in ["hot", 'cold', 'rainy']:
            #Material for Hot Weather
            if clothobj.cloth_material in HotWeatherMaterial:
                #Job Interview Occassion Cloths Type
                if (activitytype=="Job Interview" or activitytype=="School Event" or activitytype=="Business Formal" ):
                    #Check the appropiate cloth
                    if (clothobj.cloth_type=="Full Suit"):
                        selectedCloths.append(clothobj)
                    
                    if (clothobj.cloth_type=="Mid-Length Skirt" and clothobj.cloth_color in cloth_colors and clothobj.cloth_print=="Plain"
                       and clothobj.cloth_material not in ["Denim"]):
                        selectedCloths.append(clothobj)
                        
                    if (clothobj.cloth_type=="Pants" and clothobj.cloth_color in cloth_colors and clothobj.cloth_print=="Plain"):
                        selectedCloths.append(clothobj)
                        
                    if (clothobj.cloth_type=="Mid-length Dress" and clothobj.cloth_print=="Plain"):
                        selectedCloths.append(clothobj)
                        
                    if ((clothobj.cloth_type=="Blazer" or clothobj.cloth_type=="Suit Jacket") and
                    (clothobj.cloth_print=="Plain")):
                        selectedCloths.append(clothobj)
                        
                    if ((clothobj.cloth_type=="Blouse") and (clothobj.cloth_print=="Plain" or
                    clothobj.cloth_print=="Striped")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Top") and (clothobj.cloth_print=="Plain" or
                    clothobj.cloth_print=="Stripped")):
                        selectedCloths.append(clothobj)
                
                #Activity Shopping/ CasualDay Out
                if activitytype=="Shopping":
                    if (clothobj.cloth_type in ["Jeans", "Khakis","Short Skirt","Short"]):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type in "Top Turtleneck"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Cardigan"):
                        selectedCloths.append(clothobj)
                
                #Activity Date
                if activitytype=="Date":
                    if (clothobj.cloth_type in ["Top", "Blouse"]):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type in ["Jeans","Pants"]):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Mid-Length Dress"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Mid-Length Skirt" and
                        clothobj.cloth_material=="Denim"):
                        selectedCloths.append(clothobj)
                #Activity Wedding
                if activitytype=="Wedding":
                    if (clothobj.cloth_type in "Maxi Dress Long Dress"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Brim hat"):
                        selectedCloths.append(clothobj)
                
                #Activity Semi Formal/Cocktail
                if activitytype=="Cocktail":
                    if (clothobj.cloth_type=="Short Dress" and clothobj.cloth_color=="Black"):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Mid-Length Dress")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Blouse") and (clothobj.cloth_material=="Silk")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Pants")):
                        selectedCloths.append(clothobj)
    
                #Activity Formal/Black Tie
                if activitytype=="Black Tie":
                    if (clothobj.cloth_type=="Long Dress"):
                        selectedCloths.append(clothobj)
                #Activity White Tie
                if activitytype=="White Tie":
                    if (clothobj.cloth_type=="Long Dress"):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Gloves") and (clothobj.cloth_color=="White")):
                        selectedCloths.append(clothobj)
                #Activity  Church/Religious Events
                if activitytype=="Religious":
                    if (((clothobj.cloth_type in "Long Dress Maxi Dress") or (clothobj.cloth_type=="Mid-Length Dress"))
                    and((clothobj.cloth_color in ['Red', 'Orange', 'Blue', 'Pink', 'Peach','Multi-Color','Yellow'])
                    or (clothobj.cloth_print=="Floral"))):
                        selectedCloths.append(clothobj)
                    
                    if (((clothobj.cloth_type=="Long Skirt") or (clothobj.cloth_type=="Mid-Length Skirt"))
                    and (((clothobj.cloth_color in ['Red', 'Orange', 'Blue', 'Pink', 'Peach', 'Yellow'])
                    and (clothobj.cloth_print=="Floral") ))):
                        selectedCloths.append(clothobj)
                        
                    if ((clothobj.cloth_type in ["Blouse", "Top"]) and
                    (clothobj.cloth_color in ['Red', 'Orange', 'Blue', 'Pink', 'Peach', 'Yellow'])):
                        selectedCloths.append(clothobj)
                #Activity Business Casual
                
                if activitytype=="Business Casual":
                    if (clothobj.cloth_type in["Mid-Length Skirt", "Khakis", "Blouse"]):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Pants"):
                        selectedCloths.append(clothobj)
                #Funeral
                if activitytype=="Funeral":
                    if ((clothobj.cloth_type in
                         ["Pants","Full Suit","Top", "Turtleneck","Suit Jacket" ,
                          "Mid-Length Skirt", "Mid-length Dress"])
                    and (clothobj.cloth_color in ["Black", "Navy", "Brown"])):
                        selectedCloths.append(clothobj)
                    
               
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
    selectedCloths=sortclothes(selectedCloths, "Female")
    message="";
    if(len(selectedCloths))==0:
        message=suggest_male(activitytype)
        
    return {'clothobjs':selectedCloths, 'message':message}

##############################################################################################
#rules to match Males'  outfit
def outfit_rules_male(clothobjects, weathercondition, activitytype):
    """Function to map male's clothes to activities"""
    selectedCloths=[]
    HotWeatherMaterial=['Silk', 'Linen', 'Ramie',"Denim", 'Jute', 'Hemp', 'Bamboo',  'Cotton', 'Chiffon']
    #formal colors
    cloth_colors=["Gray", "Black", "Navy", "Brown", "Blue","White"]
    
    for clothobj in clothobjects:
        print(clothobj,"In loop")
        if weathercondition in ["hot", "cold", "rainy"]:
            #Material for Hot Weather
            if clothobj.cloth_material in HotWeatherMaterial:
                #Job Interview Occassion Clothes Type
                if (activitytype=="Job Interview" or activitytype=="School Event" or activitytype=="Business Casual"
                    or activitytype=="Business Formal"):
                    #Check the appropiate cloth
                    if (clothobj.cloth_type=="Full Suit"):
                        selectedCloths.append(clothobj)
                    
                    if (clothobj.cloth_type=="Trouser" and clothobj.cloth_color in cloth_colors and clothobj.cloth_print=="Plain"):
                        selectedCloths.append(clothobj)
                        
                    if ((clothobj.cloth_type=="Blazer" or clothobj.cloth_type=="Suit Jacket") and
                    (clothobj.cloth_print=="Plain")):
                        selectedCloths.append(clothobj)
                        
                    if ((clothobj.cloth_type=="Shirt") and (clothobj.cloth_print=="Plain" or
                    clothobj.cloth_print=="Striped") and
                    (clothobj.cloth_color in cloth_colors)):
                        selectedCloths.append(clothobj)
                
                #Activity Shopping/ CasualDay Out
                if activitytype=="Shopping":
                    if (clothobj.cloth_type in ["Jeans","Short", "Khakis"]):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type in "T-Shirt Dressy Shirt Turtleneck Polo Shirt"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Cardigan"):
                        selectedCloths.append(clothobj)
                
                #Activity Date
                if activitytype=="Date":
                    if (clothobj.cloth_type in ["T-Shirt","Turtleneck" ,"Polo Shirt"]):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type in "Jeans Khakis"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Cardigan"):
                        selectedCloths.append(clothobj)
                #Activity Wedding
                if activitytype=="Wedding":
                    if (clothobj.cloth_type=="Trouser"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Full Suit"):
                        selectedCloths.append(clothobj)
                
                #Activity Cocktail
                if activitytype=="Cocktail":
                    if ((clothobj.cloth_type in ["Trouser", "Suit Jacket"])
                        and (clothobj.cloth_color=="Black")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Full Suit") and clothobj.cloth_color=="Black"):
                        selectedCloths.append(clothobj)
                    if (clothobj.cloth_type=="Shirt" and clothobj.cloth_print=="Plain"
                        and clothobj.cloth_color in cloth_colors):
                        selectedCloths.append(clothobj)
    
                #Activity Formal/Black Tie
                if activitytype=="Black Tie":
                    if ((clothobj.cloth_type in ["Suit Jacket","Waistcoat"]) and (clothobj.cloth_color=="Black")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Trouser") and (clothobj.cloth_color=="Black")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Shirt") and (clothobj.cloth_color=="White") and
                        (clothobj.cloth_print=="Plain")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Bow Tie") and (clothobj.cloth_color=="Black") and
                        (clothobj.cloth_material=="Slik")):
                        selectedCloths.append(clothobj)
                #Activity White Tie
                if activitytype=="White Tie":
                    if ((clothobj.cloth_type in ["Suit Jacket","Waistcoat"]) and (clothobj.cloth_color=="White")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Trouser") and (clothobj.cloth_color=="Black")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Tailcoat") and (clothobj.cloth_color=="Black")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Shirt") and (clothobj.cloth_color=="White") and
                        (clothobj.cloth_print=="Plain")):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type=="Bow Tie") and (clothobj.cloth_color=="White") and
                        (clothobj.cloth_material=="Slik")):
                        selectedCloths.append(clothobj)
                #Activity  Church/Religious Events
                if activitytype=="Religious":
                    if ((clothobj.cloth_type in ["Jeans", "Trouser"]) or
                        (clothobj.cloth_type in ["T-Shirt","Polo Shirt","Shirt", "Turtleneck"])):
                        selectedCloths.append(clothobj)
                #Activity Business Casual
                if activitytype=="Business Casual":
                    if (clothobj.cloth_type in["Khakis,Trousers"]) and (clothobj.cloth_print=="plain"):
                        selectedCloths.append(clothobj)
                    if ((clothobj.cloth_type in ["Shirt, Polo Shirt", "Turtleneck"]) and (clothobj.cloth_print=="plain")):
                        selectedCloths.append(clothobj)
                #Funeral
                if activitytype=="Funeral":
                    if ((clothobj.cloth_type in ["Trouser"," Shirt", "Turtleneck", "Polo Shirt", "Blazer"])
                    and (clothobj.cloth_color in ["Black", "Navy", "Brown"])):
                        selectedCloths.append(clothobj)
                    
                    
            #clothes for cold days
            if weathercondition=="cold":
                if ((clothobj.cloth_type in ['Cardigan', 'Sweater', 'Jacket', 'Scarf', 'Gloves','Trench Coat']) and
                (clothobj.cloth_material in ['Wool', 'Cashmere'])):
                    selectedCloths.append(clothobj)
            #clothes for rainy days
            if weathercondition=="rainy":
                  if (clothobj.cloth_type in ['Cardigan', 'Sweater', 'Jacket', 'Scarf', 'Gloves','Rain Coat']):
                    selectedCloths.append(clothobj) 
        
    
    selectedCloths=sortclothes(selectedCloths, "Male")
    
    message="";
    if(len(selectedCloths))==0:
        message=suggest_male(activitytype)
    
    return {'clothobjs':selectedCloths, 'message':message}







#Function to Sort the selected clothes
def sortclothes(selectedclothes, gender):
   
    if gender=="Female":
        #sort through the clothes
        category_1=["Top", "Shirt",]
        category_2=["Dress", "Mid-Length Dress", "Long Dress", "Mid-Length Skirt", "Long Skirt",
                    "Maxi Dress", "Short Skirt"]
        category_3=["Full Suit"]
        category_4=["Jeans", "Pants", "Short", "Khakis"]
        category_5=["Blazer", "Cardigan", "Trench Coat", "Jacket", "Sweater","Suit Jacket"]
        category_6=["Scarf", "Gloves","Rain Coat", "Brim Hat"]
        
        selected_category_1,selected_category_2, selected_category_3,selected_category_4,selected_category_5, selected_category_6=[],[],[],[],[],[]
        selected=[]
        
        print("Start test in female")
        print(selectedclothes)
        for clothobj in selectedclothes:
            print(clothobj.cloth_type)
            if clothobj.cloth_type in category_1:
                selected_category_1.append(clothobj)
            if clothobj.cloth_type in category_2:
                selected_category_2.append(clothobj)
            if clothobj.cloth_type in category_3:
                selected_category_3.append(clothobj)
            if clothobj.cloth_type in category_4:
                selected_category_4.append(clothobj)
            if clothobj.cloth_type in category_5:
                selected_category_5.append(clothobj)
            if clothobj.cloth_type in category_6:
                selected_category_6.append(clothobj)
            
        if selected_category_4:
            selected.append(random.choice(selected_category_1))
        if selected_category_1:
            selected.append(random.choice(selected_category_1))
        if selected_category_2:
            selected.append(random.choice(selected_category_2))
        if selected_category_3:
            selected.append(random.choice(selected_category_3))
        if selected_category_5:
            selected.append(random.choice(selected_category_5))
        if selected_category_6:
            selected.append(random.choice(selected_category_5))
            
    else:
        ######################################################################################
        ############################ MALE ###################################################
        ######################################################################################
        print("Start--->>>>male")
        #MALE
        #sort through the clothes
        category_1=["Shirt", "T-Shirt",'Polo Shirt', 'Dressy Shirt',"Turtleneck"]
        category_2=["Full Suit"]
        category_3=["Jeans", "Trouser", "Short","Khakis",]
        category_4=["Rain Coat", "Blazer", "Cardigan", "Trenchcoat", "Jacket", "Sweater",
                        "Sport Coat", "Waistcoat", "Tailcoat"]
        category_5=["Scarf","Gloves", "Hat"]
        
        selected_category_1,selected_category_2, selected_category_3,selected_category_4,selected_category_5=[],[],[],[],[]
        selected=[]
        
        print("Start test in male")
        print(selectedclothes)
        for clothobj in selectedclothes:
            print(clothobj.cloth_type)
            if clothobj.cloth_type in category_1:
                selected_category_1.append(clothobj)
            if clothobj.cloth_type in category_2:
                selected_category_2.append(clothobj)
            if clothobj.cloth_type in category_3:
                selected_category_3.append(clothobj)
            if clothobj.cloth_type in category_4:
                selected_category_4.append(clothobj)
            if clothobj.cloth_type in category_5:
                selected_category_5.append(clothobj)
            
        if selected_category_1:
            selected.append(random.choice(selected_category_1))
        if selected_category_3:
            selected.append(random.choice(selected_category_3))
        if selected_category_2:
            selected.append(random.choice(selected_category_2))
        if selected_category_4:
            selected.append(random.choice(selected_category_4))
        if selected_category_5:
            selected.append(random.choice(selected_category_5))
       
    print("Test return", selected)
    return selected     
        

################################################
#suggestions male
def suggest_male(activitytype):
    #Job Interview Occassion Clothes Type
    if (activitytype=="Job Interview" or activitytype=="School Event" or activitytype=="Business Casual"
                 or activitytype=="Business Formal"):
            message="Suggestion, add; Full suit, Plain Trousers, Plain Blazer/Suit Jacket or Plain Shirt to your closet"
    if activitytype=="Shopping":
        message="We suggest adding; Jeans, T-Shirt, Light jacket or cardigan to your closet"
    
    if activitytype=="Date":
        message="Suggestion, add; Jeans, T-Shirt, Light jacket or cardigan to your closet"
    
    if activitytype=="Wedding":
        message="Suggestion, add; a Full Suit, Plain Trouser or Khaki Pants to your closet"
    
    if activitytype=="Black Tie":
        message="Suggestion, add; Black tuxedo, dress shirt and black trousers to your closet."
    
    if activitytype=="White Tie":
        message="Suggestion, add; white bow tie, white shirt, white waistcoat and a black tailcoat and black trousers to your closet"
        
    if activitytype=="Cocktail":
        message="Suggestion, add; dark suit, white shirt and  silk tie to your closet"
        
    if activitytype=="Religious":
        message="Suggestion, add; Full suit, Plain Trousers, Plain Blazer/Suit Jacket or Plain Shirt to your closet"
    
    if activitytype=="Business Casual":
        message="Suggestion, add; Sport coat or blazer, Slacks or Khakis Pants, Dress shirt, Casual button-down shirt, open-collar or polo shirt to your closet"
    
    if activitytype=="Funeral":
        message="Suggestion; add; clothing that is black and other dark tones like navy, brown, and forest green to your closet"
        
    
    return message
        

################################################
#suggestions female
def suggest_female(activitytype):
    #Job Interview Occassion Clothes Type
    if (activitytype=="Job Interview" or activitytype=="School Event" or activitytype=="Business Casual"
                 or activitytype=="Business Formal"):
            message="Suggestion, add; Full Suit, Mid-length Skirt, Official Pants, Blazer/Suit jacket or striped blouse or Mid-length dress to your closet. Suggested colours; plain grey, black, brown or navy."
    if activitytype=="Shopping":
        message="Suggestion, add; Jeans, Leggings, Tank tops or Sundresses to your closet"
    
    if activitytype=="Date":
        message="Suggestion, add; Midi dresses, Skinny Jeans or V-neked tops to your closet"
    
    if activitytype=="Wedding":
        message="Suggestion, add Maxi dress, floral dress or wide brim hat to your closet"
    
    if activitytype=="Black Tie":
        message="Suggestion, add; floor-length gown to your closet."
    
    if activitytype=="White Tie":
        message="Suggestion, add; floor-length dress and long white gloves to your closet."
        
    if activitytype=="Cocktail":
        message="Suggestion, add; floor-length evening gown, Dressy cocktail dress or short black dress to your closet"
        
    if activitytype=="Religious":
        message="Suggestion, add; long dress, mid-length dress, long Skirt, mid-length skirt or blouse to your closet. Colours; red, orange, blue, pink, peach, yellow, Floral prints"
    
    if activitytype=="Business Casual":
        message="Suggestion, add; Skirt, Khakis pants, Open-collar shirt, knit shirt, sweater or Sheath dress to your closet"
    
    if activitytype=="Funeral":
        message="Suggestion; add; clothing that is black and other dark tones like navy, brown, and forest green to your closet"
        
    
    return message
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   