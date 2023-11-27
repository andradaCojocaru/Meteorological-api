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
        tari = Tari.objects.all().values('id', 'nume_tara', 'latitudine', 'longitudine')
        formatted_tari = [{'id': entry['id'], 'nume': entry['nume_tara'], 'lat': entry['latitudine'], 'lon': entry['longitudine']} for entry in tari]
        return JsonResponse(formatted_tari, safe=False)

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
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


    def delete(self, request, id, *args, **kwargs):
        try:
            tara = Tari.objects.get(id=id)
            tara.delete()
            return JsonResponse({}, status=200)
        except Tari.DoesNotExist:
            return JsonResponse({'error': 'Tara not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class OraseListCreateView(View):
    def get(self, request, *args, **kwargs):
        orase = Orase.objects.all().values('id', 'id_tara', 'nume_oras','latitudine', 'longitudine')
        formatted_orase = [{'id': entry['id'],'idTara': entry['id_tara'], 'nume': entry['nume_oras'], 'lat': entry['latitudine'], 'lon': entry['longitudine']} for entry in orase]
        return JsonResponse(formatted_orase, safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        existing_country = Tari.objects.filter(id=data.get('idTara')).first()

        # Check if 'idTara' exists in the Tari model
        if not existing_country:
            return JsonResponse({'error': 'Tara not found'}, status=404)

        tara = existing_country
        id_tara = tara.id
        nume = data.get('nume')
        lat = data.get('lat')
        lon = data.get('lon')

        # Check if 'nume' is provided
        if not nume:
            return JsonResponse({'error': 'not having a name'}, status=400)

        # Check for an existing record with the same 'nume' for the given 'idTara'
        existing_city = Orase.objects.filter(id_tara=id_tara, nume_oras=nume).first()
        if existing_city:
            return JsonResponse({'error': 'City already exists for this country'}, status=409)

        # Save to the Cities model
        city = Orase.objects.create(id_tara=tara, nume_oras=nume, latitudine=lat, longitudine=lon)

        return JsonResponse({'id': city.id}, status=201)


# @method_decorator(csrf_exempt, name='dispatch')
# class CitiesListView(View):
#     def get(self, request, *args, **kwargs):
#         cities = Orase.objects.all().values()
#         return JsonResponse(list(cities), safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CitiesByCountryView(View):
    def get(self, request, id_Tara, *args, **kwargs):
        try:
            # Check if 'id_tara' exists in the Tari model
            if not Tari.objects.filter(id=id_Tara).exists():
                return JsonResponse({'error': 'Tara not found'}, status=404)

            orase = Orase.objects.filter(id_tara_id=id_Tara).values('id', 'id_tara', 'nume_oras','latitudine', 'longitudine')
            formatted_orase = [{'id': entry['id'],'idTara': entry['id_tara'], 'nume': entry['nume_oras'], 'lat': entry['latitudine'], 'lon': entry['longitudine']} for entry in orase]
            return JsonResponse(formatted_orase, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class CitiesUpdateDeleteView(View):
    def put(self, request, id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            id_tara = data.get('idTara')
            nume = data.get('nume')
            lat = data.get('lat')
            lon = data.get('lon')

            # Check if 'idTara' exists in the Tari model
            if not Tari.objects.filter(id=id_tara).exists():
                return JsonResponse({'error': 'Tara not found'}, status=404)

            city = Orase.objects.get(id=id)
            city.id_tara_id = id_tara
            city.nume = nume
            city.latitudine = lat
            city.longitudine = lon
            city.save()

            return JsonResponse({}, status=200)

        except Orase.DoesNotExist:
            return JsonResponse({'error': 'City not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, id, *args, **kwargs):
        try:
            city = Orase.objects.get(id=id)
            city.delete()
            return JsonResponse({}, status=200)

        except Orase.DoesNotExist:
            return JsonResponse({'error': 'City not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
