from django.shortcuts import render
from django.db.models import Exists, OuterRef, Case, When, Value, IntegerField, Q

from taller.models import Vehiculo, Tarea, EntregaVehiculo


def lista_clientes(request):

    busqueda = request.GET.get('q', '')

    vehiculos = Vehiculo.objects.all()

    if busqueda:
        vehiculos = vehiculos.filter(
            Q(placa__icontains=busqueda) |
            Q(propietario__icontains=busqueda)
        )

    vehiculos = vehiculos.annotate(
        tiene_tareas=Exists(
            Tarea.objects.filter(
                vehiculo=OuterRef('pk')
            )
        ),
        tiene_pendientes=Exists(
            Tarea.objects.filter(
                vehiculo=OuterRef('pk'),
                estado__in=['Pendiente', 'En Proceso']
            )
        ),
        tiene_entrega=Exists(
            EntregaVehiculo.objects.filter(
                vehiculo=OuterRef('pk')
            )
        )
    ).annotate(
        orden_estado=Case(
            When(tiene_entrega=True, then=Value(3)),
            When(tiene_pendientes=True, then=Value(1)),
            When(tiene_tareas=False, then=Value(0)),
            default=Value(2),
            output_field=IntegerField()
        )
    ).order_by('orden_estado', '-fecha_ingreso')

    return render(
        request,
        'clientes/vista_clientes.html',
        {
            'vehiculos': vehiculos,
            'busqueda': busqueda
        }
    )
    


from django.shortcuts import render, get_object_or_404
from taller.models import EntregaVehiculo

def ver_entrega_cliente(request, placa):

    entrega = get_object_or_404(
        EntregaVehiculo,
        vehiculo__placa=placa
    )

    error = None

    if request.method == 'POST':

        identificacion = request.POST.get('identificacion')

        if str(entrega.vehiculo.ID) == str(identificacion):
            return render(
                request,
                'clientes/entrega_cliente.html',
                {
                    'entrega': entrega
                }
            )

        error = "La identificación no coincide con la registrada para este vehículo."

    return render(
        request,
        'clientes/validar_entrega.html',
        {
            'placa': placa,
            'error': error
        }
    )
 
