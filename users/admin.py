from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission
from users.models import *

# Register your models here.

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('email', 'names','last_names')

    def clean_password2(self):
    
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
       
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password1"])
        if commit:
            usuario.save()
        return usuario
    
class UserChangeForm(forms.ModelForm):
   
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('email', 'password', 'names','last_names', 'active_user', 'admin_user')

class UserAdmin(BaseUserAdmin):
    
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'names','last_names', 'admin_user')
    list_filter = ('admin_user',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('names','last_names')}),
        ('Permissions', {'fields': ('admin_user','groups', 'user_permissions')}),
        #('Permisos', {'fields': ('groups', 'user_permissions' )}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
            ('Personal info', {'fields': ('names','last_names')}),
            ('Permissions', {'fields': ('admin_user','groups', 'user_permissions')}),   
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Usuario, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Group)
admin.site.register(Permission)


