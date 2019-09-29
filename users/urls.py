from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.index, name="signin"),
    url(r'^$', views.index, name="login"),
    url(r'^estimated_balance', views.estimated_balance, name='estimated_balance'),
    url(r'^dashboard_admin', views.dashboard_admin, name='dashboard_admin'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^transactions', views.transactions, name='transactions'),
    url(r'^link_aadhar_card', views.link_aadhar_card, name='link_aadhar_card'),
    url(r'^transfer', views.transfer, name='transfer'),
    url(r'^deposit', views.deposit, name='deposit'),
    url(r'^report$', views.listing, name="listing"),  # $
    url(r'^report/(?P<userId>\w{0,50})/$', views.listing, name="listing"),
    url(r'^update/(?P<userId>\w{0,50})/$', views.update, name="update"),
    url(r'^add$', views.add, name="add"),
    url(r'^forgot$', views.forgot, name="forgot"),
    url(r'^logout$', views.logout, name="logout"),  # $
    url(r'^changepassword$', views.changepassword, name="changepassword"),
    url(r'^delete/(?P<userId>\w{0,50})/$', views.delete, name="delete"),

    # url(r'^test$', views.test, name="test"),

    # ------------------------------ admin -------------------------------
    # -----------------------------------------
    url(r'^admin/all_user', views.all_user, name='Tous_Utilisateur'),
    url(r'^admin/all_admin', views.all_admin, name='Tous_administrateur'),
    url(r'^admin/details', views.details, name='details'),
    url(r'^admin/admin_user', views.admin_user, name='admin_open '),
    url(r'^add_admin', views.add_admin, name='add_admin'),

]
