from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest ,HttpResponse
from account.models import AcademyProfile
from .models import Branch ,Coach,Program ,TimeSlot ,ProgramImage,ProgramVideo
import NashaaSports.settings as settings 
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.contrib import messages
from django.db import transaction
from django.db.models.functions import Cast
from django.db.models import Avg ,IntegerField



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
    status=False
    program=Program.objects.get(pk=program_id)
    if request.method == "POST":
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        days = request.POST.getlist('days') 
        days_str = ''
        if start_time and end_time:
            # Ensure times are properly compared and not None
            if start_time >= end_time:
                messages.error(request, "بداية وقت البرنامج يجب أن تكون أقل من نهاية وقت البرنامج.")
            elif not days :
                 messages.error(request, "الرجاء تعبئة ايام عمل البرنامج", "red")
            else:
              days_str = ', '.join(days)  
              print(days_str)
                # Create the time slot for the program
              time_slot = TimeSlot(
                program=Program.objects.get(id=program_id),
                start_time=start_time,
                end_time=end_time,
                no_of_seats=request.POST['no_of_seats'],
                days=days_str
        )
              time_slot.save() 
              messages.success(request, "تم إضافة فترة البرنامج بنجاح.","green")
              status=True
 
    time_slots = TimeSlot.objects.filter(program=program)

    return render(request, "academy/add_program_time_slot.html", {'program': program, 'time_slots': time_slots,"days":TimeSlot.DayChoices.choices,"status":status})


def delete_time_slot_view(request:HttpResponse,time_slot_id):
    time_slot = get_object_or_404(TimeSlot, pk=time_slot_id)
    with transaction.atomic():
        time_slot.delete()
        messages.success(request,"تم حذف الفترة بنجاح","green")
    return redirect(request.GET.get('next'))
def upload_media_view(request, program_id):
    program=Program.objects.filter(id=program_id).first()
    program.is_active=True
    program.save()
    status=False
    image_urls = []
    video_urls = []
    if request.method == 'POST':
        images = request.FILES.getlist('images')  
        videos = request.FILES.getlist('videos')  

        if not images and not videos:
            messages.error(request, "يرجى رفع ملفات الصور أو الفيديو.","red")
        program = get_object_or_404(Program, id=program_id)

        with transaction.atomic():

            for image in images:
                img_instance = ProgramImage.objects.create(program=program, image=image)
                image_urls.append(img_instance.image.url)
            for video in videos:
                vid_instance = ProgramVideo.objects.create(program=program, video=video)
                video_urls.append(vid_instance.video.url)
                status=True
                

        images_str = ', '.join(image_urls) if image_urls else None
        videos_str = ', '.join(video_urls) if video_urls else None
        print(image_urls,video_urls)
        messages.success(request, f"تم رفع الصور والفيديوهات بنجاح", extra_tags="green")
        if 'save_project' in request.POST:
            return redirect('academy_dashboard_view',user_id=request.user)  
    return render(request, 'academy/add_media.html', {'program_id': program_id,"status":status,"image_urls":image_urls,"video_urls":video_urls})
def add_branch_view(request,user_id):
    # this how to render the branch location as map
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

def program_detail_view(request:HttpRequest,program_id):
    
    program= Program.objects.filter(pk=program_id).annotate(
        avg_review=Avg(Cast("review__rating", IntegerField()))
          ).first()
    time_slot=TimeSlot.objects.filter(program=Program.objects.get(pk=program_id))
    images=ProgramImage.objects.filter(program=Program.objects.get(pk=program_id))
    videos=ProgramVideo.objects.filter(program=Program.objects.get(pk=program_id))
    branch_id=program.branch.id
    branch = Branch.objects.get(id=branch_id)
    location_url = branch.branch_location  
    coordinates = location_url.split("q=")[-1]  
    google_maps_url = f"https://www.google.com/maps/embed/v1/place?key={settings.GOOGLE_API_KEY}&q={coordinates}&zoom=14"

    return render(request,"academy/program_detail.html",{'google_maps_url':google_maps_url,"program":program,"time_slots":time_slot,"images":images,"videos":videos})