from rest_framework import serializers
from p1App.models import *
from django.contrib.auth import authenticate

class RegSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUserdb
        fields=['username','full_name','email','mobile','password']

class RegSerializer1(serializers.ModelSerializer):
    class Meta:
        model=CustomUserdb
        fields=['id','username','full_name','email','mobile']


class Loginserializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Incorrect username or password")

        attrs['user'] = user
        return attrs
    
#innovator Serializers    

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projectdb
        fields = ['id','project_name','description','category','amount','end_date','image']
    
class ProjectSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Projectdb
        fields = ['id','project_name','description','category','amount','date','end_date','image','inovator']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorydb
        fields = "__all__"

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = projectupdatedb
        fields = ['update_message']
        
#investor Serializers        

class CustomUserdbSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserdb
        fields = [
            'full_name', 'email', 'mobile', 'country', 'designation',
            'proff_bio', 'twitter', 'linkedin', 'web', 'Location', 'profile_pic','dob','address','gender','instagram'
        ]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notificationdb
        exclude=['sender','receiver','project','Is_there','date_time']



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messagedb
        fields = '__all__'


class InvestmentSerializer(serializers.ModelSerializer):
    total_invested = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    balance_due = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Investeddb
        fields = ['project_name', 'investor', 'amount_invested', 'total_invested', 'balance_due', 'date_invested']



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paymentmodel
        fields = ['user','project','rate','full_name','account_no','mobile_number']