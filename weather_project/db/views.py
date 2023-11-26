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
        try:
            data = json.loads(request.body)
            # Extract values from the JSON data
            nume = data.get('nume')
            lat = data.get('lat')
            lon = data.get('lon')

            # Save to the Tari model
            tara = Tari.objects.create(nume_tara=nume, latitudine=lat, longitudine=lon)
            
            return JsonResponse({'id': tara.id}, status=201)
        except Exception as e:
            # Consider logging the exception for further investigation
            return JsonResponse({'error': 'Internal Server Error'}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class TariRetrieveUpdateDestroyView(View):
    def put(self, request, id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            tara = Tari.objects.get(id=id)
            tara.nume_tara = data['nume']
            tara.latitudine = data['lat']
            tara.longitudine = data['lon']
            tara.save()
            return JsonResponse({}, status=200)
        except Tari.DoesNotExist:
            return JsonResponse({'error': 'Tara not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, id, *args, **kwargs):
        try:
            tara = Tari.objects.get(id=id)
            tara.delete()
            return JsonResponse({}, status=200)
        except Tari.DoesNotExist:
            return JsonResponse({'error': 'Tara not found'}, status=404)
