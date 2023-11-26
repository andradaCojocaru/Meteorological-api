# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Tari, Orase, Temperaturi
from django.utils.decorators import method_decorator
from django.views import View
import json

@method_decorator(csrf_exempt, name='dispatch')
class TariListCreateView(View):
    def get(self, request, *args, **kwargs):
        tari = Tari.objects.all().values()
        return JsonResponse(list(tari), safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        nume = data.get('nume')
        lat = data.get('lat')
        lon = data.get('lon')

        # Check if 'nume' is provided
        if not nume:
            return JsonResponse({'error': 'not having a name'}, status=400)

        # Check for an existing record with the same 'nume'
        existing_tara = Tari.objects.filter(nume_tara=nume).first()
        if existing_tara:
            return JsonResponse({'error': 'same country'}, status=409)

        # Save to the Tari model
        tara = Tari.objects.create(nume_tara=nume, latitudine=lat, longitudine=lon)

        return JsonResponse({'id': tara.id}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class TariUpdateDestroyView(View):
    def put(self, request, id, *args, **kwargs):
        try:
            if not id.isdigit():
                return JsonResponse({'error': 'Invalid ID format'}, status=400)
            data = json.loads(request.body)
            tara = Tari.objects.get(id=id)

            # Check if the Tari object exists
            if not tara:
                return JsonResponse({'error': 'Tara not found'}, status=404)

            # Update the Tari object with the provided data
            tara.nume_tara = data['nume']
            tara.latitudine = data['lat']
            tara.longitudine = data['lon']
            tara.save()

            return JsonResponse({}, status=200)
        
        except Tari.DoesNotExist:
            return JsonResponse({'error': 'Tara not found'}, status=404)


    def delete(self, request, id, *args, **kwargs):
        try:
            if not id.isdigit():
                return JsonResponse({'error': 'Invalid ID format'}, status=400)
            tara = Tari.objects.get(id=id)
            tara.delete()
            return JsonResponse({}, status=200)
        except Tari.DoesNotExist:
            return JsonResponse({'error': 'Tara not found'}, status=404)
