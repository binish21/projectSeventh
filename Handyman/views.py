from django.shortcuts import render, redirect
from django.views import View
from .models import City, Profession, User, Handyman,  Contract
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

class index(View):
    def get(self, request):
        cities = City.objects.all()
        professions = Profession.objects.all()
        allHandymans = Handyman.objects.all()[0:5]

        context ={
            'cities': cities,
            'professions': professions,
            'allHandymans' : allHandymans
        } 
        return render(request, 'Handyman/index.html', context)
    
    def post(self, request):
        city_id = request.POST.get('city')
        profession_id = request.POST.get('profession')

        cities = City.objects.all()
        professions = Profession.objects.all()

        handymans = Handyman.objects.filter(profession=profession_id, user__city=city_id)
        context = {
            'handymans': handymans,
            'cities': cities,
            'professions': professions
        }
        return render(request, 'Handyman/index.html', context)


class register(View):
    def get(self, request):
        cities = City.objects.all()
        professions = Profession.objects.all()
        print(cities)
        context = {
        'cities': cities,
        'professions' : professions
        }   
        return render(request, 'Handyman/register.html', context )

    def post(self, request):
        name =  request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        password = request.POST.get('password')

        profession = request.POST.get('profession')
        rate = request.POST.get('rate')
        city = request.POST.get('city')
        permanent_address = request.POST.get('permanent_address')
        temporary_address = request.POST.get('temporary_address')
        image = request.FILES.get('image')

        values = {
            'name' : name,
            'email': email,
            'contact' : contact,
            'rate': rate,
            'permanent_address' : permanent_address,
            'temporary_address' : temporary_address
        }

        user = User(
            name = name,
            contact = contact,
            email = email,
            password = password,
            permanent_address = permanent_address,
            temporary_address = temporary_address,
            image = image
        )

        error_message = validateRegisterForm(user)
        rate_error = None
        if not rate:
            rate_error = "Invalid hourly rate !"

        if not error_message and not rate_error:
            selectedProfession = Profession.objects.get(id=profession)
            selectedCity = City.objects.get(id=city)
            user.city = selectedCity
            user.password = make_password(user.password)
            user.save()

            handyman = Handyman(
                rate = rate,
                profession = selectedProfession,
                user = user                
            )
            handyman.save()
            return redirect('index')
        else:
            cities = City.objects.all()
            professions = Profession.objects.all()
            context = {
                'error_message' : error_message,
                'values': values,
                'rate_error' : rate_error,
                'professions' : professions,
                'cities' : cities
            }
            return render(request, 'Handyman/register.html', context)



class login(View):
    def get(self, request):
        return render(request, 'Handyman/login.html', {})
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        getUser = User.get_user_by_email(email)
        if getUser:
            getPassword = check_password(password, getUser.password)
            if getPassword:
                request.session['user'] = getUser.id
                #print("Session id",request.session.get('user'))
                return redirect('dashboard', id=getUser.id)
            else:
                error_message = "Username and password dont match !"
        else:
            error_message = "Username and password dont match !"
        values = {'email' : email}
        context = {
            'error_message' : error_message,
            'values' : values
        }
        return render(request, 'Handyman/login.html', context)
    


# class search(View):
#     def get(self, request):
#         cities = City.objects.all()
#         professions = Profession.objects.all()

#         context ={
#             'cities': cities,
#             'professions': professions
#         } 
#         return render(request, 'Handyman/index.html', context)


class profile(View):
    def get(self, request, id):
        handyman = Handyman.objects.get(id=id)
        context = {
            'handyman' : handyman
        }
        return render(request, 'Handyman/profile.html', context)

    def post(self, request, id):
        name = request.POST.get('name')
        address = request.POST.get('address')
        house = request.POST.get('house')
        contact = request.POST.get('contact')
        date = request.POST.get('date')
        estimated_hours = request.POST.get('estimated_hours')
        description = request.POST.get('description')

        values  = {
            'name' : name,
            'address':address,
            'house': house,
            'contact': contact,
            'estimated_hours': estimated_hours,
        }

        handyman_to_hire = Handyman.objects.get(id=id)

        contract = Contract(
            handyman = handyman_to_hire,
            customer_name = name,
            address = address,
            house = house,
            customer_contact = contact,
            date = date,
            estimated_hours = estimated_hours,
            description = description
        )

        error_message = validateContractForm(contract)

        if not error_message:
            contract.save()

            #Setting up Email body

            subject = "Service contract recieved"
            message = "Hey "+ handyman_to_hire.user.name + ", you recieved a service request from "+ name + " at " + date +" ."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [handyman_to_hire.user.email,]
            send_mail(subject, message, email_from, recipient_list)

            success_message = "Congrats "+ handyman_to_hire.user.name+ " has been booked for "+ contract.date +"."
            context ={
                'success_message': success_message
            }
            return render(request, 'Handyman/hire_success.html', context)
        else:
            context = {
                'values': values,
                'error_message':error_message,
            }
            messages.error(request, error_message)
            return redirect("profile", id=id)


def validateRegisterForm(user):
    error_message = None

    if(not user.name):
        error_message = "Name cannot be blank !"
    elif(not user.contact):
        error_message = "Contact number cannot be blank !"
    elif(not user.email):
        error_message = "Email cannot be blank !"
    elif(not user.password):
        error_message = "Password cannot be blank !"
    elif(not user.image):
        error_message = "You must upload an image !"

    getEmail = User.objects.filter(email=user.email)

    if getEmail:
        error_message = "Email is already registered !"
    return error_message


def validateContractForm(contract):
    error_message = None

    if(not contract.customer_name):
        error_message = "Name cannot be blank !"
    elif(not contract.address):
        error_message = "Address cannot be blank !"
    elif(not contract.house):
        error_message = "House number cannot be blank !"
    elif(not contract.customer_contact):
        error_message = "Contact cannot be blank !"
    elif(not contract.date):
        error_message = "You must choose a date !"
    elif(not contract.estimated_hours):
        error_message = "Please mention estimated hours !"
    
    checkContractByDate = Contract.get_contract_by_date(contract)
    if checkContractByDate:
        error_message = "Sorry ! Handy is already booked on that day !"
    return error_message



class dashboard(View):
    def get(self, request, id):
        profile = Handyman.objects.get(id=id)
        user = User.objects.get(id=id)
        contracts = Contract.objects.filter(handyman=profile)
        context = {
            'profile':profile,
            'contracts' : contracts
        }
        return render(request, 'Handyman/dashboard.html', context)



class contract(View):
    def get(self, request, id):
        contract = Contract.objects.get(id=id)
        context = {
            'contract':contract
        }
        return render(request, 'Handyman/contract.html', context)