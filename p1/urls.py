"""p1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from p1App.views import *
from p1App.investor_views import *
from p1App.innovator_views import *
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.routers import DefaultRouter
# router=DefaultRouter()

# router.register("project/",Project,basename="pjct")


urlpatterns = [
    
    
    path('admin/', admin.site.urls),
    path('innovator/register/',InnovatorReg.as_view(),name="innovator_reg"),
    path('invester/register/',InvesterReg.as_view(),name="invester_reg"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(),name="logout"),
    path("send/message/<int:pk>",MessageViewSet.as_view(),name="send_msg"),
    path("Chat/History/<int:pk>",ChatList.as_view(),name="chat"),
    
    
    #innovator Urls
    
    path("project/",ProjectApi.as_view(),name="pjct"),
    path("project/<int:pk>",ProjectApi.as_view(),name="pjct"),
    path("category/",CatogariView.as_view(),name="category"),
    path("update/<int:pk>",UpdateView.as_view(),name="update"), #updates of projects from innovator
    path("notification/view",NotificationViewAPI.as_view(),name="notify"),
    path("confirm/notify/<int:pk>",NotificationConfirm.as_view(),name="confirm"),
    path("reject/notification/<int:pk>",RemoveNotification.as_view(),name="reject"),
    path("notified/list/",MessageList.as_view(),name="msg"),
    path("list/investor/<int:pk>",InvestedProjects.as_view(),name="invested"),
    path("payed/user/list/<int:pk>",InvestedProjectsUser.as_view(),name="list_invested"),# list investors in innovaters project
    
    #investor Urls
    path("projectview/<int:pk>",ProjectView.as_view(),name="prjview_int"),
    path("projectview/",ProjectView.as_view(),name="prjview"),
    path('user/profile/update/', ProfileUpdate.as_view(), name='user_update'),
    path("profileview/",ProfileView.as_view(),name="profile_view"),
    path("project/notify/<int:pk>",NotificationView.as_view(),name="notyview"),
    path("send/message/rcv/",MessageListInvestor.as_view(),name="invs_msg"),
    path("project/list/",ConfirmedProjectList.as_view(),name="pjr"),
    path("Add/Investment/<int:pk>",AddInvestment.as_view(),name="investment"),
    path("Investment/done/",MyInvestments.as_view(),name="invest_list"), # list invested projects
    path("get/updation/<int:pk>",GetUpdations.as_view(),name="list_update"),# list updation of project
    path("make/payment/<int:pk>",MakePayment.as_view(),name="payment"),# make payment or investment
    path("transaction/history/",PaymentHistory.as_view(),name="payment_history"),#payment history
    path("send/investor/message/<int:pk>",FirstMessageViewSet.as_view(),name="send_msg_first"),# to send message to innovaters

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
