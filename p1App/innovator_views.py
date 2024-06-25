from rest_framework.views import APIView
from p1App.models import *
from p1App.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework import status,permissions,authentication

class CatogariView(APIView):
    
    def get(self,request,*args,**kwargs):
        category=Categorydb.objects.all()
        serializer=CategorySerializer(category,many=True)
        return Response(data = serializer.data)
    
    def post(self,request,*args,**kwargs):
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data)
        else:
            return Response(data = serializer.errors)
        
class ProjectApi(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):
        serializer = ProjectSerializer(data = request.data)
        if serializer.is_valid():
            serializer.validated_data['inovator'] = request.user
            serializer.save()
            return Response(data = serializer.data)
        else:
            return Response(data = serializer.errors)
        
    def get(self, request, *args, **kwargs):
        # Retrieve projects uploaded by the currently authenticated user
        projects = Projectdb.objects.filter(inovator_id=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            project = Projectdb.objects.get(id=id)
        except Projectdb.DoesNotExist:
            return Response(data={"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectSerializer(instance=project, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        project = Projectdb.objects.get(id=pk)
        if project:
            project.delete()
            return Response("project removed")
        else:
            return Response("project does not exist")
    

class UpdateView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        
        try:
            qs = Projectdb.objects.get(id=id)
        except Projectdb.DoesNotExist:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(project_name=qs)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class NotificationViewAPI(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user.id
        profile=Notificationdb.objects.filter(receiver_id=user)
        serializer = NotificationSerializer(profile,many=True)
        return Response(serializer.data)
    
class NotificationConfirm(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        serializer = NotificationSerializer()
        id=kwargs.get("pk")
        qs=Notificationdb.objects.get(id=id)
        if qs.Is_there == False:
            qs.Is_there = True
            qs.save()
        return Response(serializer.data)
    

class RemoveNotification(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Notificationdb.objects.get(id=id).delete()
        return Response(data={"message": "Notification rejected"})

    



class MessageList(APIView):
     permission_classes=[permissions.IsAuthenticated]

     def get(self,request,*args,**kwargs):
         user=self.request.user.id
         data=Notificationdb.objects.filter(receiver_id=user,Is_there=True)
         c=[]
         for i in data:
            c.append(i.sender.id)
         user_list = []
         for j in c:
            qs = CustomUserdb.objects.filter(id=j)
            for user in qs:
                print(user.id)
                user_list.append(user)
         serializer = RegSerializer(user_list, many=True)
         return Response(serializer.data)
     


class InvestedProjects(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
         id=kwargs.get("pk")
         list=Investeddb.objects.filter(project_name_id=id)
         c=[]
         for i in list:
            c.append(i.id)
         list = []
         for j in c:
            qs = CustomUserdb.objects.filter(id=j)
            for li in qs:
                print(li.id)
                list.append(li)
         serializer = RegSerializer(list, many=True)
         return Response(serializer.data)



# class InvestedProjects(APIView):
#      def get(self,request,*args,**kwargs):
#          id=kwargs.get("pk")
#          list=Investeddb.objects.filter(project_name_id=id)
#          serializer = NotificationSerializer(list,many=True)
#          return Response(serializer.data)