from django.shortcuts import render
from .forms import UserProfileForm, UserForm

def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'message': "Welcome to Outfit.com"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'user_auth/base.html', context_dict)

def trya(request):
    hello="Welcome, to Our Outfit Expert System:"
    return render(request,
                  'user_auth/trya.html',
                  {'message': hello})
#registration view
def register(request):
    
    registered=False
    
    if request.method=="POST":
        
        userform=UserForm(data=request.POST)
        userprofileform=UserProfileForm(data=request.POST)
        
        if userform.is_valid() and userprofileform.is_valid():
            
            #saving the user's form data in the databases
            user=userform.save()
            #hashing the password
            user.set_password(user.password)
            user.save()
            
            profile=userprofileform.save(commit=False)
            profile.user=user
            
            #add the profile image if there is one
            if "picture" in request.FILES:
                profile.picture=request.FILES['picture']
            
            profile.save()
            
            registered=True
            
        else:
            
            print userform.errors, userprofileform.errors
    else:
        userform=UserForm()
        userprofileform=UserProfileForm()
    
    #return render to response depending on the context
    return render(request,
                  "user_auth/registeration.html",
                  {"userform": userform, "userprofileform": userprofileform, "registered": registered})
        
        
        
    
    
