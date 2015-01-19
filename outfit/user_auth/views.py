from django.shortcuts import render
from .forms import UserForm, UserProfileForm

def trya(request):
    return render(request,
                  'user_auth/trya.html',
                  {'message': 'Hello BOYS'})
#registration view
def register(request):
    
    registered=False
    
    if request.method=="POST":
        
        userform=UserForm(data=request.POST)
        userprofile=UserProfileForm(data=request.POST)
        
        if userform.is_valid() and userprofile.is_valid():
            
            #saving the user's form data in the databases
            user=userform.save()
            #hashing the password
            user.set_password(user.password)
            user.save()
            
            profile=userprofile.save(commit=False)
            profile.user=user
            
            #add the profile image if there is one
            if "picture" in request.FILES:
                profile.picture=request.FILES['picture']
            
            profile.save()
            
            registered=True
            
        else:
            
            print user_form.errors, profile_form.errors
    else:
        userform=UserForm()
        userprofileform=UserProfileForm()
    
    #return render to response depending on the context
    return render(request,
                  "user_auth/registeration.html",
                  {"userform": userform, "userprofileform": userprofileform, "registered": registered})
        
        
        
    
    
