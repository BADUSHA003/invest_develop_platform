from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUserdb(AbstractUser):
    full_name=models.CharField(max_length=60,null=False)
    mobile=models.PositiveBigIntegerField(null=False)
    country=models.CharField(max_length=60,null=True,blank=True)
    designation=models.CharField(max_length=200,null=True,blank=True)
    proff_bio=models.CharField(max_length=300,null=True,blank=True)
    twitter=models.URLField(blank=True,null=True)
    dob= models.DateField(null=True, blank=True) 
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender=models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    address=models.TextField(null=True)
    instagram=models.CharField(max_length=200,null=True)
    linkedin=models.URLField(blank=True,null=True)
    web=models.URLField(blank=True,null=True)
    Location=models.CharField(max_length=300,null=True,blank=True)
    is_innovator=models.BooleanField(default=False)
    is_investor=models.BooleanField(default=False)
    profile_pic=models.ImageField(upload_to='files',blank=True,null=True)

    def __str__(self):
        return self.full_name

class Categorydb(models.Model):
    c_name=models.CharField(max_length=30)

class Projectdb(models.Model):
    project_name=models.CharField(max_length=40)
    description=models.TextField(max_length=500)
    category=models.ForeignKey(Categorydb,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    inovator=models.ForeignKey(CustomUserdb,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True,null=True)
    end_date=models.DateField(null=True)
    image=models.ImageField(upload_to='project_files',blank=True,null=True)
    status = models.BooleanField(default=False,null=True)
    
    # active = models.BooleanField(default=True)

    # def can_delete(self):
    #     return not self.transaction_set.exists()
    

class projectupdatedb(models.Model):
    project_name=models.ForeignKey(Projectdb,on_delete=models.CASCADE,null=True)
    update_message=models.CharField(max_length=300)
    date_time=models.DateTimeField(auto_now=True)

class Messagedb(models.Model):
    sender=models.ForeignKey(CustomUserdb,on_delete=models.CASCADE,null=True,related_name='sent_messages')
    receiver=models.ForeignKey(CustomUserdb,on_delete=models.CASCADE,null=True,related_name='received_messages')
    message=models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

class Notificationdb(models.Model):
    sender=models.ForeignKey(CustomUserdb,on_delete=models.CASCADE,null=True,related_name='send')
    receiver=models.ForeignKey(CustomUserdb,on_delete=models.CASCADE,null=True,related_name='receive')
    project=models.ForeignKey(Projectdb,on_delete=models.CASCADE,null=True)
    Is_there=models.BooleanField(default=False,null=True)
    date_time=models.DateTimeField(auto_now=True,null=True)

class Investeddb(models.Model):
    project_name = models.ForeignKey(Projectdb, on_delete=models.CASCADE, null=True)
    investor = models.ForeignKey(CustomUserdb, on_delete=models.CASCADE, null=True)
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,null=True)
    date_invested = models.DateTimeField(auto_now_add=True,null=True)

    def _str_(self):
        return f"{self.investor.full_name} invested {self.amount_invested} in {self.project_name.project_name}"

    def get_total_invested(self):
        return Investeddb.objects.filter(investor=self.investor, project_name=self.project_name).aggregate(
            total=models.Sum('amount_invested')
        )['total']

    def get_balance_due(self):
        total_invested = self.get_total_invested() or 0
        return self.project_name.amount - total_invested

class Paymentmodel(models.Model):
    user = models.ForeignKey(CustomUserdb,on_delete=models.CASCADE)
    project = models.ForeignKey(Projectdb,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100,null=True)
    account_no =models.CharField(max_length=100,null=True)
    mobile_number = models.PositiveBigIntegerField(null=True)
    rate = models.PositiveBigIntegerField(null=True)
    created_at = models.DateTimeField(auto_now=True)








