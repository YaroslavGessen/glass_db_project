from django.contrib import admin
from django.urls import path, re_path
from garage import views
from django.conf import settings
from django.conf.urls.static import static
from garage.views import ChangePasswordView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('addnew', views.add_new_vehicle),
    path('edit/<int:id>', views.edit_vehicle),
    path('update/<int:id>', views.update_vehicle),
    path('destroy/<int:id>', views.destroy_vehicle),
    path('glasses/<int:id>', views.glasses),
    path('addnewglass/<int:id>', views.add_new_glass),
    path('editglass/<int:id>', views.edit_glass),
    path('updateglass/<int:id>', views.update_glass),
    path('destroyglass/<int:id>', views.destroy_glass),
    path('destroyvector/<int:id>', views.destroy_vector),
    path('vectordetails/<str:source>', views.vehicle_details),
    re_path(r'^login/$', views.login_func, name='login'),
    re_path(r'^logout/', views.logout_func, name='logout'),
    re_path(r'^register/$', views.register, name='register'),
    path('importvehicles/', views.import_to_vehicles),
    path('importvector/', views.import_vector),
    path('', views.index, name='home'),
    path('show_vectors/', views.vectors, name='show_vectors'),
    re_path(r'^download/(?P<file_path>.*)/$', views.download_file, name='download_file'),
    re_path(r'^downloaddata/(?P<car_id>.*)/$', views.download_data, name='download_data'),
    re_path(r'^downloadvectordata/', views.download_vector_data, name='download_vector_data'),
    re_path(r'^profile/', views.profile, name='profile'),
    path('password/', ChangePasswordView.as_view(), name='password_change'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
