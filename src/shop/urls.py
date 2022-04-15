from atexit import register
from django.urls import path
from .views import *
app_name = 'shop'
urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('leaves/', Leaves.as_view(), name='leave'),
    # path('leaves/', leaveview, name='leave'),
    path('pay/', Pay.as_view(), name='pay'),
    path('<pk>/approve-or-decline/', Leave_Update.as_view(), name='leave-update'),
    path('register/', signupview, name='register' ),
    path('<pk>/update/', Employee_Update.as_view(), name='update' ),
    path('list/', Leave_List.as_view(), name='leave-list' )
]