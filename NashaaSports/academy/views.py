from django.shortcuts import render,redirect
from django.http import HttpRequest ,HttpResponse
from account.models import AcademyProfile
from .models import Branch ,Coach,Program
import NashaaSports.settings as settings 
from django.contrib.auth.models import User
from datetime import datetime



def acadmey_dashboard_view(request:HttpRequest,user_id):
    if request.user.is_authenticated:
        acadmey=AcademyProfile.objects.filter(user=User.objects.get(pk=user_id)).first()
        if acadmey:
            if  request.user.id==int(user_id) and acadmey.approved==True: 
                context={"acadmey":acadmey}
                return render(request,"academy/dashboard.html",context)
            else:
                return HttpResponse(f"غير مصرح لك")
        else:
            return HttpResponse(f"لم يتم اعتمادك من قبل منصة نشء! فضلا أنشئ ملف أكاديميتك وانتظر الاعتماد.")
        
    else:
        return HttpResponse("غير مصرح لك")

def add_program_view(request:HttpRequest,user_id):
# branch
# program_name
# description
# fees
# start_date
# end_date
# no_of_seats
# age_group
    acadmey=AcademyProfile.objects.filter(user=User.objects.get(pk=user_id)).first()
    if  request.user.id==int(user_id) and acadmey.approved==True: #should be True. False just for testing 
            if request.method=="POST":
                program=Program(
                    branch=Branch.objects.get(pk=request.POST['branch']),
                    program_name=request.POST['program_name'],
                    description=request.POST['description'],
                    fees=request.POST['fees'],
                    start_date=request.POST['start_date'],
                    end_date=request.POST['end_date'],
                    no_of_seats=request.POST['no_of_seats'],
                    age_group=request.POST['age_group'],
                               )
                program.save()
            return render(request,"academy/add_program.html")
    return HttpResponse("غير مصرح لك")


def add_branch_view(request,user_id):
    # this how to render the branch location as map brothers
    # f"https://maps.googleapis.com/maps/api/geocode/json?address={branch.location}&key={settings.GOOGLE_API_KEY}"
    try: 
        acadmey=AcademyProfile.objects.filter(user=User.objects.get(pk=user_id)).first()
        if acadmey.approved==True and request.user.id==int(user_id): #should be True/ 
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
            return HttpResponse("غير مصرح لك")
            
    except Exception as e:
        print(e)
        return HttpResponse(f"some thing went wrong{e}")

             
def add_coach_view(request:HttpRequest,user_id):
    academy=AcademyProfile.objects.filter(user=User.objects.get(pk=user_id)).first()
    if request.user.id==int(user_id)and academy.approved==True:    #should be True .. for testig it's false
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
        return HttpResponse("غير مصرح لك")
