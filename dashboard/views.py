from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from item.models import ItemComprado

@login_required
def index(request):
    # Obtener los ítems comprados por el usuario desde la tabla ItemComprado
    items_comprados = ItemComprado.objects.filter(usuario=request.user)

    return render(request, 'dashboard/index.html', {
        'items_comprados': items_comprados,
    })

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'dashboard/profile.html', {'user': user})


