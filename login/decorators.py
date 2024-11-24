from functools import wraps
from django.shortcuts import render


# este decoardor es para verificar un solo grupo
# def group_required(group_name, access_denied_template='pagina/acceso_denegado.html'):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             if not request.user.groups.filter(name=group_name).exists():
#                 # Redireccionar a alguna página de acceso denegado o login
#                 return render(request, access_denied_template)
#             return view_func(request, *args, **kwargs)
#         return _wrapped_view
#     return decorator

# verifixa varios grupos
def groups_required(groups, access_denied_template='pagina/acceso_denegado.html'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_groups = request.user.groups.values_list('name', flat=True)
            if not any(group in user_groups for group in groups):
                # Renderizar la página de acceso denegado
                return render(request, access_denied_template)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
