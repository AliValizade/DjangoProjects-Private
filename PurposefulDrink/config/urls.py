"""
URL configuration for A project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.urls import re_path , path
from django.conf import settings
from django.conf import settings
from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

...

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

# urlpatterns = [
#    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cms', include('cms.urls.admin_urls', namespace='cms_admin')),
    path('accounts/admin/', include('accounts.urls.admin_urls', namespace='accounts_admin')),
    path('accounts/user/', include('accounts.urls.user_urls', namespace='accounts_user')),
    path('shop/', include('shop.urls', namespace='shop')),
    # path('blog/front', include('blog.urls.front', namespace='blog-front')),
    path('blog/admin/', include('blog.urls.admin', namespace='blog-admin')),
    
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

#all path and urls 



# swagger<format>/ [name='schema-json']
# swagger/ [name='schema-swagger-ui']
# redoc/ [name='schema-redoc']
# admin/
# [name='cmsview']
# accounts/admin/
# accounts/user/ o/
# accounts/user/ register/ [name='register/']
# accounts/user/ api/token/login/email [name='email_token']
# accounts/user/ api/token/login/phone [name='phone_token']
# accounts/user/ logout/ [name='logout']
# accounts/user/ api/token/verify/ [name='verify']
# shop/
# blog/

