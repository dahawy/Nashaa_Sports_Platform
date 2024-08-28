from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest ,HttpResponse
from account.models import AcademyProfile, UserProfile
from .models import Branch, Coach, Program, TimeSlot, ProgramImage, ProgramVideo
from bookmark.models import ProgramBookmark
import NashaaSports.settings as settings 
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.contrib import messages
from django.db import transaction
from django.db.models.functions import Cast ,Round
from django.db.models import Avg ,IntegerField,FloatField ,Q
from django.db.models.functions import ExtractDay
from django.db.models import F, ExpressionWrapper
from enrollment.models import Enrollment
from review.models import Review
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from babel.dates import format_date
from datetime import datetime
from django.db.models import Count


def acadmey_dashboard_view(request:HttpRequest,user_id):
    if request.user.is_authenticated:
        # sport_categories_colors = generate_colors(len(sport_categories_labels))
        acadmey=AcademyProfile.objects.filter(user=User.objects.get(pk=user_id)).first()
        branches=Branch.objects.filter(academy=acadmey)
        programs=Program.objects.filter(branch__academy=acadmey)
        total_programs = programs.count()

    # Aggregate data: Count the number of programs per sport category
        sport_category_distribution = programs.values('sport_category').annotate(
            count=Count('id')
        ).order_by('sport_category')

        # Manually initialize the dictionary with all sport categories set to 0
        percentage_dict = {value: 0 for key, value in Program.SportChoices.choices}

        # Update the dictionary with actual counts from the sport_category_distribution
        for sport in sport_category_distribution:
            for key, value in Program.SportChoices.choices:
                if key == sport['sport_category']:
                    display_label = value
                    # Calculate the percentage
                    percentage_dict[display_label] = round((sport['count'] / total_programs) * 100, 2)

        # Filter out categories with a percentage of 0
        filtered_percentage_dict = {label: percentage for label, percentage in percentage_dict.items() if percentage > 0}

        # Convert the filtered dictionary to lists for use in the template
        summation = list(filtered_percentage_dict.values())
        labels = list(filtered_percentage_dict.keys())

        # Print debugging information
        


        coaches=Coach.objects.filter(branch__academy=acadmey)
        today = timezone.now().date()
        date_days_ago = today - timedelta(days=30)
        cart__payment__status=True,  #status=True means payment completed
        cart__payment__payment_date__range=[date_days_ago, today]
        subscriptions = Enrollment.objects.filter(Q(time_slot__program__branch__academy=acadmey) & Q(cart__status='Paid')&Q(cart__payment__payment_date__range=[date_days_ago, today]))
        
        aggregated_enrollments = subscriptions.values('cart__payment__payment_date').annotate(enrollment_count=Count('id') ).order_by('cart__payment__payment_date')
        aggregated_payments = subscriptions.values('cart__payment__payment_date').annotate(sales_total=Sum('program__fees')).order_by('cart__payment__payment_date')
        aggregated_payments = subscriptions.values('cart__payment__payment_date').annotate(sales_total=Sum('program__fees')).order_by('cart__payment__payment_date')
        
        salesList =[]
        salesList = [float(item['sales_total']) for item in aggregated_payments]
        total_income=sum(salesList)
        salesList = salesList if salesList else [0]
        datesList = [item['cart__payment__payment_date'].strftime('%d %B') for item in aggregated_payments]
        enrollmentList = [int(item['enrollment_count']) for item in aggregated_enrollments]
        total_enrollments = sum(enrollmentList)
        enrollmentList = enrollmentList if enrollmentList else [0]
        # 
        





        # 

# Format dates for the datesList
        enrollements_datesList = [item['cart__payment__payment_date'].strftime('%d %B') for item in aggregated_enrollments]
        enrollments=Enrollment.objects.filter(Q(program__branch__academy=acadmey) & Q(cart__status='Paid') )
        enrollments_ended=enrollments.filter(status="ended")
        enrollments_in_progress=enrollments.filter(status='in_progress')
        enrollments_pending=enrollments.filter(status="pending")
        if acadmey:
            if  request.user.id==int(user_id) and acadmey.approved==True: 
                context={"academy":acadmey,'programs':programs,'branches':branches,'enrollments':enrollments,'enrollments_ended':enrollments_ended,'enrollments_in_progress':enrollments_in_progress,'enrollments_pending':enrollments_pending,'coaches':coaches,'salesList':salesList,'datesList':datesList,'total_income':total_income,'total_enrollments':total_enrollments,'enrollements_datesList':enrollements_datesList,'enrollmentList':enrollmentList,'labels':labels,'summation':summation}
                return render(request,"academy/dashboard.html",context)
            else:
                return HttpResponse(f"غير مصرح لك")
        else:
            return HttpResponse(f"لم يتم اعتمادك من قبل منصة نشء! فضلا أنشئ ملف أكاديميتك وانتظر الاعتماد.")
        
    else:
        return HttpResponse("غير مصرح لك")

def add_program_view(request:HttpRequest,user_id):


    academy=AcademyProfile.objects.filter(user=User.objects.get(pk=user_id)).first()
    if  request.user.id==int(user_id) and academy.approved==True: #should be True. False just for testing 
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
                            is_available= not is_available,
                            registration_end_date=registration_end_date,
                            is_active=False
                        )
                        program.save()
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
       
        messages.success(request, f"تم انشاء البرنامج بنجاح", extra_tags="green")
        if 'save_project' in request.POST:
            return redirect('academy_dashboard_view',user_id=request.user)  
    return render(request, 'academy/add_media.html', {'program_id': program_id,"status":status,"image_urls":image_urls,"video_urls":video_urls})
def add_branch_view(request,user_id):
    # this how to render the branch location as map
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

        return HttpResponse("not authraized")


def program_detail_view(request:HttpRequest,program_id):
    

    program = Program.objects.get(pk=program_id)
    reviews = program.review_set.all()
    rating_ranges = [range(int(review.rating)) for review in reviews]
    
    for index, review in enumerate(reviews):
        reviews[index].rating_range = range(int(review.rating))
    program = Program.objects.filter(pk=program_id).annotate(
    avg_rating=Round(Avg(Cast('review__rating', FloatField())), 1) 
    ).annotate(
        duration=ExpressionWrapper(
            (ExtractDay(F('end_date') - F('start_date'))) / 7,
            output_field=IntegerField()
        )  # Calculate program duration in weeks
    ).first()
    time_slot=TimeSlot.objects.filter(program=Program.objects.get(pk=program_id))
    images=ProgramImage.objects.filter(program=Program.objects.get(pk=program_id))
    videos=ProgramVideo.objects.filter(program=Program.objects.get(pk=program_id))
    branch_id=program.branch.id
    branch = Branch.objects.get(id=branch_id)
    location_url = branch.branch_location  
    coordinates = location_url.split("q=")[-1]  
    google_maps_url = f"https://www.google.com/maps/embed/v1/place?key={settings.GOOGLE_API_KEY}&q={coordinates}&zoom=14"
    if request.user.is_authenticated:
        user_profile=UserProfile.objects.filter(user=User.objects.get(pk=request.user.id)).first()

    is_bookmarked = ProgramBookmark.objects.filter(program=program, user=user_profile).exists() if request.user.is_authenticated else False
    



    return render(request,"academy/program_detail.html",{'google_maps_url':google_maps_url,"program":program,"time_slots":time_slot,"images":images,"videos":videos, "is_bookmarked":is_bookmarked,'reviews':reviews})


def academies_profile_view(request:HttpRequest,academy_id):
    academy=AcademyProfile.objects.get(pk=academy_id)
    branches=Branch.objects.filter(academy=academy)
    programs = Program.objects.filter(branch__in=branches)[:3]
    coach=Coach.objects.filter(branch__in=branches)
    return render(request,'academy/academies_profile.html',{"academy":academy,'branches':branches,"programs":programs,'coaches':coach})
def programs_list_view(request: HttpRequest):
    # Retrieve the academy for the logged-in user
    academy = AcademyProfile.objects.filter(user=request.user).first()
    
    # Get all branches related to the academy
    branches = Branch.objects.filter(academy=academy)
    
    # Start with all programs related to the branches
    programs = Program.objects.filter(branch__in=branches)
    
    # Handle search query
    search_query = request.GET.get('search')
    if search_query:
        programs = programs.filter(
            Q(name__icontains=search_query) |  # Search by program name
            Q(description__icontains=search_query)  # Search by program description
        )
    
    # Handle branch filter
    branch_filter = request.GET.get('branch')
    if branch_filter:
        programs = programs.filter(branch__branch_name=branch_filter)
    
    # Handle category filter
    category_filter = request.GET.get('category')
    if category_filter:
        programs = programs.filter(sport_category=category_filter)
    
    # Annotate the queryset with additional data
    programs = programs.annotate(
        avg_rating=Round(Avg(Cast('review__rating', FloatField())), 1),  # Average rating for each program
        start_days=ExtractDay(F('start_date')),  # Extract start day
        end_days=ExtractDay(F('end_date'))  # Extract end day
    ).annotate(
        duration=ExpressionWrapper(
            (ExtractDay(F('end_date') - F('start_date'))) / 7,
            output_field=IntegerField()
        )  # Calculate program duration in weeks
    )
    
    # Render the template with the filtered and annotated programs
    return render(request, 'academy/programs_list.html', {
        'programs': programs,
        'sport_choices': Program.SportChoices.choices,
        'branches': branches  # Pass branches for use in the template
    })
def delete_program_view(request:HttpRequest, program_id):
        program=Program.objects.get(pk=program_id)
        program.delete()
        messages.success(request,"deleted successfully") 
        return redirect(request.GET.get('next','/'))
def update_programs_info_view(request:HttpRequest,program_id):
    program=Program.objects.get(pk=program_id)
    academy=AcademyProfile.objects.filter(user=User.objects.get(pk=request.user.id)).first()
    branches=Branch.objects.filter(academy=academy)
    context={"branches":branches,"programs_list":Program.SportChoices.choices,'program':program}
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
                    
                        
                            program.branch=Branch.objects.filter(id=request.POST['branch']).first()
                            program.program_name=request.POST['program_name']
                            program.description=request.POST['description']
                            program.fees=request.POST['fees']
                            program.start_date=start_date
                            program.end_date=end_date
                            program.min_age=min_age
                            program.max_age=max_age
                            program.sport_category=request.POST['sport_category']
                            program.is_available= not is_available
                            program.registration_end_date=registration_end_date
                        
                            program.save()
                            messages.success(request, "تم إنشاء البرنامج بنجاح!", "green")
                            return redirect("academy:update_time_slot_view",program_id=program.id)
                 except Exception as e:
                     messages.error(request, f"Error creating program: {str(e)}", "red")


    return render(request,'academy/update_info.html',context)

def update_time_slot_view(request:HttpRequest,program_id):
    program=Program.objects.get(pk=program_id)
    academy=program.branch.academy
    status=True
    context={"program":program,"academy":academy,"days":TimeSlot.DayChoices.choices,"status":status}

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


    
    return render(request,'academy/update_time_slot.html',context)
def update_media_view(request:HttpResponse,program_id):
    program=Program.objects.filter(id=program_id).first()
    status=False
    image_urls = []
    video_urls = []
    prev_imgs=ProgramImage.objects.filter(program=program)
    prev_vids=ProgramVideo.objects.filter(program=program)
    for image in prev_imgs:
                image_urls.append(image)
    for vide in prev_vids:
                video_urls.append(vide)
                
    if request.method == 'POST':
        images = request.FILES.getlist('images')  
        videos = request.FILES.getlist('videos')  

        if not images and not videos:
            messages.error(request, "يرجى رفع ملفات الصور أو الفيديو.","red")
        program = get_object_or_404(Program, id=program_id)
        
        with transaction.atomic():
            
            for image in images:
                img_instance = ProgramImage.objects.create(program=program, image=image)
                image_urls.append(img_instance)
            for video in videos:
                vid_instance = ProgramVideo.objects.create(program=program, video=video)
                video_urls.append(vid_instance)
                status=True
            
        
        if 'save_project' in request.POST:
            messages.success(request, f"تم انشاء البرنامج بنجاح", extra_tags="green")
            return redirect('academy_dashboard_view',user_id=request.user)  

    return render(request, 'academy/update_media.html', {'program_id': program_id,"status":status,"image_urls":image_urls,"video_urls":video_urls} )
def branches_list_view(request:HttpRequest,user_id):
    if request.user.is_authenticated:
        academy=AcademyProfile.objects.get(user=User.objects.get(pk=user_id))
        branches=Branch.objects.filter(academy=AcademyProfile.objects.get(pk=academy.id))
        subscriber_count = Enrollment.objects.filter(time_slot__program__branch__in=branches).count()


    
    return render(request,'academy/branches_list.html',{"branches":branches,'subscriber_count':subscriber_count})
def delete_branch_view(request:HttpRequest,branch_id):
    try:
        branch=Branch.objects.get(pk=branch_id)
        branch.delete()
        messages.success(request,"تم الحذف بنجاح")
        return redirect(request.GET.get('next','/'))
    except Exception as e:
        messages.error(request,"هناك مشكلة في الحذف حاول مرة اخرى")

def update_branch_view(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)

    if request.method == "POST":
        branch.branch_city = request.POST.get('branch_city')
        branch.branch_name = request.POST.get('branch_name')
        branch.register_no = request.POST.get('register_no')
        
        # Get the full Google Maps URL from the form
        map_url = request.POST.get('map_url')
        
        if map_url:
            branch.branch_location = map_url
        
        branch.save()
        messages.success(request, 'تم تحديث الفرع بنجاح')
        

    # Extract coordinates from the current URL if it exists
    lat, lng = 0.0, 0.0
    if branch.branch_location:
        try:
            query = branch.branch_location.split('?q=')[-1]
            lat, lng = map(float, query.split(','))
        except (ValueError, IndexError):
            lat, lng = 0.0, 0.0

    return render(request, 'academy/update_branch.html', {
        'branch': branch,
        'lat': lat,
        'lng': lng,
        'google_maps_api_key': settings.GOOGLE_API_KEY,
        'cities':Branch.Cities.choices
    })

def coach_list_view(request:HttpRequest, academy_id):
    if request.user.is_authenticated:
        academy=AcademyProfile.objects.filter(user=User.objects.get(pk=academy_id)).first()
        if academy:
            coaches = Coach.objects.filter(branch__academy=academy).all()
            return render(request,'academy/coaches_list.html',{'coaches':coaches})
        else:
           return HttpResponse("غير مصرح لك بالدخول الى هذه الصفحة")
    else:
        return HttpResponse("غير مصرح لك")
def delete_coach_view(request: HttpRequest, coach_id: int):
    if request.user.is_authenticated:
       
        user_academy = AcademyProfile.objects.filter(user=request.user).first()
        
        # Fetch the coach object
        coach = get_object_or_404(Coach, id=coach_id)
        
        # Check if the coach belongs to the user's academy
        if coach.branch.academy == user_academy:
            # Perform the deletion
            coach.delete()
            messages.success(request,'تم الحذف بنجاح') 
            return redirect(request.GET.get('next','/'))
        else:
            return HttpResponse("You are not allowed to delete this coach.")
    else:
        return messages.error('لست مصرحا تحتاج الى تسجيل الدخول')

def update_coach_view(request:HttpResponse,coach_id):
    if request.user.is_authenticated:
       
        user_academy = AcademyProfile.objects.filter(user=request.user).first()
        
        # Fetch the coach object
        coach = get_object_or_404(Coach, id=coach_id)
        
        # Check if the coach belongs to the user's academy
        if coach.branch.academy == user_academy:
            coach=get_object_or_404(Coach,pk=coach_id)
            branches=Branch.objects.filter(academy=user_academy)

            if request.method=="POST":
                date_str = request.POST.get('birth_date')
                birth_date = datetime.strptime(date_str, '%m/%d/%Y').date()
                coach.name = request.POST['name']
                coach.birth_date = birth_date
                coach.email = request.POST['email']
                coach.phone = request.POST['phone']
                coach.experience = request.POST['experience']
                coach.nationality = request.POST['nationality']
                coach.gender = request.POST['gender']
                coach.avatar = request.FILES['avatar']
                coach.save()
                messages.success(request,"تم التحديث بنجاح","green")
                return redirect(request.GET.get('next','/'))
            return render(request,'academy/update_coach.html',{'coach':coach,"genders":Coach.Gender.choices,"nationality":Coach.Nationality.choices,"branches":branches})
        else:
            return HttpResponse("غير مصرح لك")
    else:
            return HttpResponse("غير مصرح لك")


def subscribers_view(request, user_id):
    if request.user.is_authenticated:
        academy = AcademyProfile.objects.filter(user=User.objects.get(pk=user_id)).first()
        if academy:

            if request.user.id == int(user_id) and academy.approved:
                # Get search term and status from GET parameters
                search_term = request.GET.get('search', '')
                selected_status = request.GET.get('status', '')

                # Build the base query
                query = Q(time_slot__program__branch__academy=academy) & Q(cart__status='Paid')

                # Apply status filter if it's not 'all'
                if selected_status and selected_status != 'all':
                    query &= Q(status=selected_status)

            if  request.user.id==int(academy.user.id) and academy.approved==True: 
                subscribers = Enrollment.objects.filter(Q(time_slot__program__branch__academy=academy) & Q(cart__status='Paid'))

                
                # Apply search filter if search term is provided
                if search_term:
                    query &= (
                        Q(first_name__icontains=search_term) |
                        Q(father_name__icontains=search_term) |
                        Q(last_name__icontains=search_term)
                    )

                # Apply the filters
                subscribers = Enrollment.objects.filter(query)

                # Render the template with filtered results
                return render(request, "academy/subscribers.html", {'subscribers': subscribers})
            else:
                return HttpResponse("غير مصرح لك")
        else:
            return HttpResponse("لم يتم اعتمادك من قبل منصة نشء! فضلا أنشئ ملف أكاديميتك وانتظر الاعتماد.")
    else:
        return HttpResponse("غير مصرح لك")
    
def delete_video(request:HttpRequest,video_id):
    video=ProgramVideo.objects.get(pk=video_id)
    video.delete()
    return redirect(request.GET.get('next','/'))
def delete_image(request:HttpRequest,image_id):
    image=ProgramImage.objects.get(pk=image_id)
    image.delete()
    return redirect(request.GET.get('next','/'))
