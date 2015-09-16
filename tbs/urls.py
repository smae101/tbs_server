from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^register$', views.RegisterView.as_view(), name='register'),
	url(r'^login$', views.LoginView.as_view(), name='login'),
	url(r'^admin_login$', views.AdminLoginView.as_view(), name='admin_login'),
	url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
	url(r'^change_password$', views.ChangePasswordView.as_view(), name='change_password'),
	url(r'^notification/$', views.NotificationView.as_view(), name='notification'),
	url(r'^transaction$', views.TransactionView.as_view(), name='transaction'),
	url(r'^sell_approval_all$', views.AllSellApprovalView.as_view(), name='sell_approval_all'),
	url(r'^sell_approval/$', views.SellApprovalView.as_view(), name='sell_approval'),
]