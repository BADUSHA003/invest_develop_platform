from rest_framework.views import APIView
from p1App.models import *
from p1App.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework import status,permissions,authentication
from django.core.exceptions import ValidationError


class ProjectView(APIView):

    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        id = kwargs.get("pk")
        if id:
            projects = Projectdb.objects.filter(id=id)
        else:
            projects = Projectdb.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

        
class ProfileUpdate(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = self.request.user.id
        try:
            profile = CustomUserdb.objects.get(id=user)
        except CustomUserdb.DoesNotExist:
            return Response(data={"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomUserdbSerializer(instance=profile, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user.id
        profile=CustomUserdb.objects.filter(id=user)
        serializer = CustomUserdbSerializer(profile,many=True)
        return Response(serializer.data)
    
class NotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            qs = Projectdb.objects.get(id=id)
        except Projectdb.DoesNotExist:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.validated_data['sender'] = request.user
                serializer.save(receiver=qs.inovator, project=qs)
                return Response(data=serializer.data)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class MessageListInvestor(APIView):
     permission_classes=[permissions.IsAuthenticated]

     def get(self,request,*args,**kwargs):
         user=self.request.user.id
         data=Notificationdb.objects.filter(sender_id=user,Is_there=True)
         c=[]
         for i in data:
            c.append(i.receiver.id)
         user_list = []
         for j in c:
            qs = CustomUserdb.objects.filter(id=j)
            for user in qs:
                print(user.id)
                user_list.append(user)
         serializer = RegSerializer(user_list, many=True)
         return Response(serializer.data)
     

class ConfirmedProjectList(APIView):
     permission_classes=[permissions.IsAuthenticated]

     def get(self,request,*args,**kwargs):
         user=self.request.user.id
         data=Notificationdb.objects.filter(sender_id=user,Is_there=True)
         c=[]
         for i in data:
            c.append(i.project.id)
         project_list = []
         for j in c:
            qs = Projectdb.objects.filter(id=j)
            for user in qs:
                print(user.id)
                project_list.append(user)
         serializer = ProjectSerializer(project_list, many=True)
         return Response(serializer.data)
     


class AddInvestment(APIView):
    permission_classes=[permissions.IsAuthenticated]
 
    def post(self,request,*args,**kwargs):
        user=self.request.user.id
        project = kwargs.get("pk")
        imvestment_data = {
            'project_name':project,
            'investor': user ,  
        }
        serializer = InvestmentSerializer(data = imvestment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data)
        else:
            return Response(data = serializer.errors)
        


class MyInvestments(APIView):
    permission_classes=[permissions.IsAuthenticated]

    
    def get(self,request,*args,**kwargs):
         user=self.request.user.id
         data=Investeddb.objects.filter(investor_id=user)
         c=[]
         for i in data:
            c.append(i.project_name_id)
         project_list = []
         for j in c:
            qs = Projectdb.objects.filter(id=j)
            for user in qs:
                print(user.id)
                project_list.append(user)
         serializer = ProjectSerializer(project_list, many=True)
         return Response(serializer.data)
     


class GetUpdations(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        data=projectupdatedb.objects.filter(project_name_id = id)
        serializer = UpdateSerializer(data, many=True)
        return Response(serializer.data)
     
class MakePayment(APIView):
    permission_classes=[permissions.IsAuthenticated]


    def post(self, request, *args, **kwargs):
        sender = request.user
        message_data = {
            'user': sender.id,
            'project': kwargs.get("pk"),
            'amount': request.data.get('amount',request.data),
            'full_name': request.data.get('full_name',request.data),
            'account_no': request.data.get('account_no',request.data),
            'mobile_number': request.data.get('mobile_number',request.data)
        }
        serializer = PaymentSerializer(data=message_data)
        if serializer.is_valid():
            message = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PaymentHistory(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        id = request.user
        data=Paymentmodel.objects.filter(user_id = id)
        serializer = PaymentSerializer(data, many=True)
        return Response(serializer.data)
     



class FirstMessageViewSet(APIView):
    def post(self, request, *args, **kwargs):
        id= kwargs.get("pk")
        sender = request.user
        data=Projectdb.objects.get(id = id)


        message_data = {
            'sender': sender.id,
            'receiver':data.inovator_id,
            'message': request.data.get('message',request.data)
        }
        serializer = MessageSerializer(data=message_data)
        if serializer.is_valid():
            message = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
