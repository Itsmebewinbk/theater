from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Admin.models import CustomUser
class CustomUserAdmin(UserAdmin):
    list_display = ('name','email','mobile','usertype')
#     # list_filter = []
#     #
    fieldsets = (
        (None, {'fields': ('username','email','password')}),
        ('Personal Informations', {'fields': ('age', 'image','address')}),
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2', 'usertype',)}
    #     ),
    # )
    # search_fields = ('email',)
    # ordering = ('email',)
admin.site.register(CustomUser, CustomUserAdmin)