from django.shortcuts import render,redirect
from django.http import HttpRequest ,HttpResponse
from account.models import AcademyProfile
from .models import Branch ,Coach,Program
import NashaaSports.settings as settings 
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.contrib import messages



def acadmey_dashboard_view(request:HttpRequest,user_id):
    if request.user.is_authenticated:
        acadmey=AcademyProfile.objects.filter(user=User.objects.get(pk=user_id)).first()
        if  request.user.id==int(user_id) and acadmey.approved==False: #should be True. False just for testing 
            context={"acadmey":acadmey}
            return render(request,"academy/dashboard.html",context)
        else:
            return HttpResponse(f"not authraized ")
        
    else:
        return HttpResponse("not authraized")

def add_program_view(request:HttpRequest,user_id):

    academy=AcademyProfile.objects.filter(user=User.objects.get(pk=user_id)).first()
    if  request.user.id==int(user_id) and academy.approved==False: #should be True. False just for testing 
            branches=Branch.objects.filter(academy=academy)
            context={"branches":branches,"programs_list":Program.SportChoices.choices}
            if request.method=="POST":
                
                if 'registration_end_date' not in request.POST or not request.POST['registration_end_date'].strip():
                    
                    start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
                    registration_end_date = start_date - timedelta(days=1)
                else:
                    # Use the provided 'registration_end_date'
                    registration_end_date = datetime.strptime(request.POST['registration_end_date'], '%Y-%m-%d')
                is_available = True if 'is_available' in request.POST else False
                print(is_available)

                program=Program(
                    branch=Branch.objects.filter(id=request.POST['branch']).first(),
                    program_name=request.POST['program_name'],
                    description=request.POST['description'],
                    fees=request.POST['fees'],
                    start_date=request.POST['start_date'],
                    end_date=request.POST['end_date'],
                    no_of_seats=request.POST['no_of_seats'],
                    min_age=request.POST['min_age'],
                    max_age=request.POST['max_age'],
                    sport_category=request.POST['sport_category'],
                    is_available=is_available  # Default to 'FALSE' if not checked
,
                    registration_end_date=registration_end_date

                               )
                program.save()
                print("save")
            return render(request,"academy/add_program.html",context)
    return HttpResponse("Not authraized")
def add_program_time_slot_view(request:HttpResponse):
    return render(request,"academy/add_program_time_slot.html")


def add_branch_view(request,user_id):
    # this how to render the branch location as map brothers
    # f"https://maps.googleapis.com/maps/api/geocode/json?address={branch.location}&key={settings.GOOGLE_API_KEY}"
    try: 
        acadmey=AcademyProfile.objects.filter(user=User.objects.get(pk=user_id)).first()
        if acadmey.approved==False and request.user.id==int(user_id): #should be True/ 
            if request.method == "POST":
                location = request.POST.get('location')
                branch_city = request.POST.get('branch_city')
                branch_name = request.POST.get('branch_name')
                register_no = request.POST.get('register_no')

                if location and branch_city and branch_name and register_no:
                    branch = Branch(
                        branch_location=location,
                        branch_city=branch_city,
                        branch_name=branch_name,
                        register_no=register_no,
                        academy=acadmey
                    )
                    branch.save()
                    return redirect("academy:academy_dashboard_view", user_id=request.user.id)
            return render(request,"academy/add_branch.html",{'google_maps_api_key': settings.GOOGLE_API_KEY,"cities":Branch.Cities.choices})   
        else:
            return HttpResponse("Not authraized")
            
    except Exception as e:
        print(e)
        return HttpResponse(f"some thing went wrong{e}")

             
def add_coach_view(request:HttpRequest,user_id):
    academy=AcademyProfile.objects.filter(user=User.objects.get(pk=user_id)).first()
    if request.user.id==int(user_id)and academy.approved==False:    #should be True .. for testig it's false
        try:
            branches=Branch.objects.filter(academy=academy) #the user should select one of the branches to add the coach to it.
            if request.method=="POST":
                date_str = request.POST.get('birth_date')
                birth_date = datetime.strptime(date_str, '%m/%d/%Y').date()
                branch=Branch.objects.get(pk=request.POST['branch'])
                branch=Coach(

                             branch=branch,
                             name=request.POST['name'],
                             birth_date=birth_date,
                             email=request.POST['email'],
                             phone=request.POST['phone'],
                             experience=request.POST['experience'],
                             nationality=request.POST['nationality'],
                             gender=request.POST['gender'],
                             avatar=request.FILES['avatar']
                             
                             )
                branch.save()
        except Exception as e:
            print(e)
        context={"genders":Coach.Gender.choices,"nationality":Coach.Nationality.choices,"branches":branches}
        return render(request,'academy/add_coach.html',context)
    else:
        return HttpResponse("not authraized")
