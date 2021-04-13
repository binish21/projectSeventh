from django.db import models

#City Model
class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

#Profession Model
class Profession(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


#User Model
class User(models.Model):
    name = models.CharField(max_length=120)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    contact = models.CharField(max_length=15)
    password = models.CharField(max_length=250)
    permanent_address = models.CharField(max_length=120, null=True)
    temporary_address = models.CharField(max_length=120, null=True)
    image = models.ImageField(upload_to = 'media/images')
    status = models.BooleanField(default=1)
    


    def __str__(self):
        return self.name
         
    #To return user if exists
    @staticmethod
    def get_user_by_email(email):
        try:
            return User.objects.get(email=email)
        except:
            return False

#Handyman Model
class Handyman(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)  
    description = models.CharField(max_length=500)
    rate = models.IntegerField()
    

    def __str__(self):
        return self.user.name


#Contract Model

class Contract(models.Model):
    handyman = models.ForeignKey(Handyman, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    house = models.CharField(max_length=200)
    customer_contact = models.CharField(max_length=200)
    date = models.DateField()
    estimated_hours = models.IntegerField()
    description = models.TextField()
    total_hours = models.IntegerField(null=True)
    isPaid = models.BooleanField(default=1)
    status = models.BooleanField(default=1)

    def __str__(self):
        return self.customer_name

    @staticmethod
    def get_contract_by_date(contract):
        try:
            return Contract.objects.get(date=contract.date, handyman = contract.handyman)
        except:
            return False






    
    
