from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'date_joined'
    )
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email', 'first_name',)
    empty_value_display = '-'
    readonly_fields = ('date_joined', 'last_login')


admin.site.register(Follow)
