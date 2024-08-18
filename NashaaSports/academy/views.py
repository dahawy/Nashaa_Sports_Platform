from django.shortcuts import render,redirect
from django.http import HttpRequest ,HttpResponse
from account.models import AcademyProfile
from .models import Branch ,Coach,Program ,TimeSlot
import NashaaSports.settings as settings 
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.contrib import messages
from django.db import transaction



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
                    
                    registration_end_date = datetime.strptime(request.POST['registration_end_date'], '%Y-%m-%d')
                is_available = True if 'is_available' in request.POST else False

                min_age = int(request.POST['min_age'])
                max_age = int(request.POST['max_age'])
                start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
                end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')

                if max_age < min_age:
                    messages.error(request, "يجب أن يكون الحد الأقصى للعمر مساويًا أو أكبر من الحد الأدنى للعمر.", "red")
                elif start_date >= end_date:
                    messages.error(request, "يجب أن يكون تاريخ البدء قبل تاريخ الانتهاء.", "red")
                elif registration_end_date > end_date:
                    messages.error(request, "يجب أن يكون تاريخ انتهاء التسجيل مساويًا أو قبل تاريخ الانتهاء.", "red")
                else:

                 try:
                    
                        program = Program(
                            branch=Branch.objects.filter(id=request.POST['branch']).first(),
                            program_name=request.POST['program_name'],
                            description=request.POST['description'],
                            fees=request.POST['fees'],
                            start_date=start_date,
                            end_date=end_date,
                            no_of_seats=request.POST['no_of_seats'],
                            min_age=min_age,
                            max_age=max_age,
                            sport_category=request.POST['sport_category'],
                            is_available=is_available,
                            registration_end_date=registration_end_date,
                            is_active=False
                        )
                        program.save()
                        messages.success(request, "تم إنشاء البرنامج بنجاح!", "green")
                        return redirect("academy:add_program_time_slot_view",program_id=program.id)
                    
                 except Exception as e:
                    messages.error(request, f"Error creating program: {str(e)}", "red")
                    
            return render(request,"academy/add_program.html",context)
    return HttpResponse("Not authraized")
def add_program_time_slot_view(request:HttpResponse,program_id):
    program=Program.objects.get(pk=program_id)
    if request.method == "POST":
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        days = request.POST.getlist('days')
        days_str = ', '.join(days) 

        if start_time and end_time:
            # Ensure times are properly compared and not None
            if start_time >= end_time:
                messages.error(request, "بداية وقت البرنامج يجب أن تكون أقل من نهاية وقت البرنامج.")
            else:
                # Create the time slot for the program
              time_slot = TimeSlot(
                program=Program.objects.get(id=program_id),
                start_time=start_time,
                end_time=end_time,
                days=days_str
        )
            time_slot.save()
                
            messages.success(request, "تم إضافة فترة البرنامج بنجاح.","green")
    if 'next_step' in request.POST:
            return redirect('add_video', program_id=program_id)

    # Get all added time slots for this program to display them
    time_slots = TimeSlot.objects.filter(program=program)

    return render(request, "academy/add_program_time_slot.html", {'program': program, 'time_slots': time_slots})



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
