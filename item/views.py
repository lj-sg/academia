from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewItemForm, EditItemForm
from .models import Category, Item, CarritoItem, TransaccionPago, ItemComprado
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')

@login_required
def agregar_al_carrito(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    # Verificar si el usuario ya ha comprado este item
    try:
        ItemComprado.objects.get(usuario=request.user, item=item)
        messages.warning(request, f'Ya has comprado el producto "{item.name}". No puedes agregarlo al carrito nuevamente.')
    except ObjectDoesNotExist:
        # El usuario no ha comprado este item, se puede agregar al carrito
        carrito_item, created = CarritoItem.objects.get_or_create(
            product=item,
            user=request.user
        )

        if not created:
            carrito_item.quantity += 1
            carrito_item.save()
            messages.success(request, f'Se ha agregado 1 unidad del producto "{item.name}" al carrito.')
        else:
            messages.success(request, f'Se ha agregado el producto "{item.name}" al carrito.')

    return redirect('item:ver_carrito')

@login_required
def quitar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, pk=item_id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        messages.success(request, f'Se ha restado 1 unidad del producto "{item.product.name}" en el carrito.')
    else:
        item.delete()
        messages.success(request, f'Se ha eliminado el producto "{item.product.name}" del carrito.')

    return redirect('item:ver_carrito')


@login_required
def ver_carrito(request):
    items_en_carrito = CarritoItem.objects.filter(user=request.user)
    total_carrito = sum(item.subtotal() for item in items_en_carrito)

    context = {
        'items_en_carrito': items_en_carrito,
        'total_carrito': total_carrito,
    }

    return render(request, 'item/carrito.html', context)


@login_required
def procesar_pago(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        numero_tarjeta = request.POST.get('tarjeta')
        fecha_caducidad = request.POST.get('caducidad')

        # Obtener los items en el carrito antes de vaciarlo
        items_en_carrito = CarritoItem.objects.filter(user=request.user)

        for carrito_item in items_en_carrito:
            item = carrito_item.product

            # Verificar si hay suficiente cantidad disponible para el ítem
            if not item.vender(carrito_item.quantity):
                # Manejar el caso en que no hay suficiente cantidad disponible
                messages.error(request, f'No hay suficiente cantidad disponible para "{item.name}".')

                # Vaciar el carrito del usuario
                items_en_carrito.delete()
                return redirect('dashboard:index')



            # Crear una instancia de ItemComprado y guardarla en la base de datos
            item_comprado = ItemComprado(
                usuario=request.user,
                item=item,
                cantidad=carrito_item.quantity,
            )
            item_comprado.save()

        # Crear una instancia de TransaccionPago y guardarla en la base de datos
        transaccion = TransaccionPago(
            usuario=request.user,
            nombre_cliente=nombre,
            direccion_cliente=direccion,
            # Agrega otros campos según sea necesario
        )
        transaccion.save()

        # Vaciar el carrito del usuario
        items_en_carrito.delete()

        messages.success(request, 'Pago exitoso. ¡Gracias por tu compra!')
        return redirect('dashboard:index')  # Cambia 'dashboard:index' por la URL de tu página de inicio
        
    return render(request, 'item/procesar_pago.html')


@login_required
def pago_exitoso(request):
    # Obtener el carrito del usuario
    carrito_items = CarritoItem.objects.filter(user=request.user)

    # Verificar que haya items en el carrito
    if carrito_items.exists():
        # Obtener el último item del carrito (puedes ajustar esto según tu lógica)
        item_comprado = carrito_items.last().product

        # Crear una nueva transacción de pago y vincularla al item comprado
        transaccion = TransaccionPago(
            usuario=request.user,
            item_comprado=item_comprado,
            # Agrega otros campos según sea necesario
        )
        transaccion.save()

        # Limpiar el carrito del usuario
        carrito_items.delete()

        # Redirigir al usuario al dashboard
        return redirect('dashboard:index')
    else:
        # Manejar el caso en que no hay items en el carrito
        return render(request, 'item/error.html', {'mensaje': 'No hay items en el carrito.'})