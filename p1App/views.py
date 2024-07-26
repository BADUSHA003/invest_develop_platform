from datetime import datetime, timedelta
from rest_framework.views import APIView
from p1App.models import *
from p1App.serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login,logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import status,permissions,authentication




class InnovatorReg(APIView):
    serializer_class=RegSerializer
    def post(self,request):
        serializer=RegSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['is_innovator'] = True
            user = CustomUserdb.objects.create_user(**serializer.validated_data)
            return Response({'message': 'registered successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InvesterReg(APIView):
    serializer_class=RegSerializer   
    def post(self,request):
        serializer=RegSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['is_investor'] = True
            user = CustomUserdb.objects.create_user(**serializer.validated_data)
            return Response({'message': 'registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class LoginView(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class= Loginserializer
    def post(self, request):
        serializer = Loginserializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
            data = {
                'id': user.id,
                'username': user.username,
                'is_innovator': user.is_innovator,
                'is_investor': user.is_investor,
            }
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'logged in successfully', 'token': token.key, 'data': data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        
        logout(request)

        
        try:
            token = request.auth
            token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass

        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
       

   
class MessageViewSet(APIView):
    def post(self, request, *args, **kwargs):
        sender = request.user

        message_data = {
            'sender': sender.id,
            'receiver': kwargs.get("pk"),
            'message': request.data.get('message',request.data)
        }
        serializer = MessageSerializer(data=message_data)
        if serializer.is_valid():
            message = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from django.db.models import Q

class ChatList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        other_user_id = kwargs.get("pk")

        now = datetime.now()

        time_threshold = now - timedelta(hours=24)

        messages = Messagedb.objects.filter(
            Q(sender_id=user_id, receiver_id=other_user_id) |
            Q(sender_id=other_user_id, receiver_id=user_id),
            created_at__gte=time_threshold
        )
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
   
    




        