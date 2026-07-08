from django.urls import path, reverse_lazy
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_view
from .forms import (
    LoginForm,
    MyPasswordResetForm,
    MyPasswordChangeForm,
    MySetPasswordForm
)

urlpatterns = [
    path('', views.home, name="home"),
    path('category/<slug:val>/', views.CategoryView.as_view(), name="category"),
    path('category-title/<slug:val>/', views.CategoryTitle.as_view(), name="category-title"),
    path('product_detail/<int:pk>/', views.ProductDetail.as_view(), name="product_detail"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateaddress/<int:pk>', views.UpdateAddress.as_view(), name='UpdateAddress'),
    path('add-to-cart/',views.add_to_cart,name="add-to-cart"),
    path('cart/',views.show_cart,name="showcart"),
    path('checkout/',views.checkout.as_view(),name="checkout"),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('payment/', views.payment, name='payment'),
    path('orders/', views.orders, name='orders'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    path('wishlist/', views.show_wishlist, name='wishlist'),
    path('removewishlist/', views.remove_wishlist, name='removewishlist'),
    path('orderdetail/<int:pk>/', views.order_detail, name='orderdetail'),
    path('deleteorder/<int:pk>/', views.delete_order, name='deleteorder'),
    path('buyagain/<int:pk>/', views.buy_again, name='buyagain'),
    path('search/', views.search, name='search'),
    path('product-detail/<int:pk>/',views.product_detail,name='product-detail'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),

    # login
    path('registration/', views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path('accounts/login/', auth_view.LoginView.as_view(
        template_name='app/login.html',
        authentication_form=LoginForm
    ), name="login"),

    # password reset
    path('password-reset/', auth_view.PasswordResetView.as_view(
    template_name='app/password_reset.html',
    email_template_name='app/password_reset_email.html',
    subject_template_name='app/password_reset_subject.txt',
    form_class=MyPasswordResetForm,
     ), name='password_reset'),

    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html',
        form_class=MySetPasswordForm
    ), name='password_reset_confirm'),

    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'
    ), name='password_reset_complete'),

    # password change
    path('passwordchange/', auth_view.PasswordChangeView.as_view(
        template_name="app/changepassword.html",
        form_class=MyPasswordChangeForm,
        success_url=reverse_lazy('passwordchangedone')
    ), name='passwordchange'),

    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(
        template_name='app/passwordchangedone.html'
    ), name='passwordchangedone'),

    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
]