import csv
import io
from django import forms
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from .models import PaqueteTuristico, Reserva

admin.site.site_header = "Administración Viajes EBC"
admin.site.site_title = "Panel Viajes EBC"
admin.site.index_title = "Control de Operaciones Turísticas"


class CsvImportForm(forms.Form):
    csv_file = forms.FileField(label='Selecciona un archivo CSV')


@admin.register(PaqueteTuristico)
class PaqueteTuristicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'destino', 'precio', 'categoria', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre', 'destino')

    change_list_template = "admin/paquetes_list.html"
    actions = ['cargar_csv_action']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('importar-csv/', self.admin_site.admin_view(self.importar_csv), name='paquete_importar_csv'),
        ]
        return custom_urls + urls

    def importar_csv(self, request):
        """Vista integrada que genera la pantalla de subida con el diseño predeterminado de Django Admin"""
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'El archivo debe tener extensión .csv')
                    return redirect('.')

                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string, None)  # Omitir la primera línea (encabezados)

                contador = 0
                for row in csv.reader(io_string, delimiter=','):
                    if row:
                        PaqueteTuristico.objects.create(
                            nombre=row[0].strip(),
                            destino=row[1].strip(),
                            precio=row[2].strip(),
                            categoria=row[3].strip().upper()
                        )
                        contador += 1

                messages.success(request, f'¡Se cargaron {contador} paquetes correctamente!')
                return redirect('..')
        else:
            form = CsvImportForm()

        context = {
            'form': form,
            'title': 'Cargue Masivo de Paquetes Turísticos (CSV)',
            'site_header': admin.site.site_header,
            'opts': self.model._meta,
            'add': True,
            'change': False,
        }


        return render(request, "admin/csv_form.html", context)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'paquete', 'estado', 'total', 'fecha')
    list_filter = ('estado', 'fecha')
    search_fields = ('cliente_nombre',)