# views.py

from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Tari, Orase, Temperaturi
from django.utils.decorators import method_decorator
from django.views import View
import json

@method_decorator(csrf_exempt, name='dispatch')
class TariListCreateView(View):
    def get(self, request, *args, **kwargs):
        # mapping between database and response
        tari = Tari.objects.all().values('id', 'nume_tara', 'latitudine', 'longitudine')
        formatted_tari = [{'id': entry['id'], 'nume': entry['nume_tara'], 'lat': entry['latitudine'], \
                        'lon': entry['longitudine']} for entry in tari]
        return JsonResponse(formatted_tari, safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        # parse body
        nume = data.get('nume')
        lat = data.get('lat')
        lon = data.get('lon')

        # Check if 'nume' is provided
        if not nume:
            return JsonResponse({'error': 'not having a name'}, status=400)
        # Check if 'nume' is provided
        if not lat:
            return JsonResponse({'error': 'not having a latitudine'}, status=400)
        # Check if 'nume' is provided
        if not lon:
            return JsonResponse({'error': 'not having a longitudine'}, status=400)
        
        # check proper value type
        if not isinstance(nume, str):
            return JsonResponse({'error': 'Invalid data type for nume'}, status=400)
        if not isinstance(lon, float):
            return JsonResponse({'error': 'Invalid data type for lon'}, status=400)
        if not isinstance(lat, float):
            return JsonResponse({'error': 'Invalid data type for lat'}, status=400)

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

            # Update the Tari object with the provided data
            tara.nume_tara = data['nume']
            tara.latitudine = data['lat']
            tara.longitudine = data['lon']
            tara.save()

            return JsonResponse({}, status=200)
        
        # check for errors
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
        formatted_orase = [{'id': entry['id'],'idTara': entry['id_tara'], 'nume': entry['nume_oras'], \
                        'lat': entry['latitudine'], 'lon': entry['longitudine']} for entry in orase]
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
        # Check if 'nume' is provided
        if not lat:
            return JsonResponse({'error': 'not having a latitudine'}, status=400)
        # Check if 'nume' is provided
        if not lon:
            return JsonResponse({'error': 'not having a longitudine'}, status=400)
        if not id_tara:
            return JsonResponse({'error': 'not having an id_tara'}, status=400)

        # check proper value type
        if not isinstance(nume, str):
            return JsonResponse({'error': 'Invalid data type for nume'}, status=400)
        if not isinstance(lon, float):
            return JsonResponse({'error': 'Invalid data type for lon'}, status=400)
        if not isinstance(lat, float):
            return JsonResponse({'error': 'Invalid data type for lat'}, status=400)
        if not isinstance(id_tara, int):
            return JsonResponse({'error': 'Invalid data type for id_tara'}, status=400)

        # Check for an existing record with the same 'nume' for the given 'idTara'
        existing_city = Orase.objects.filter(id_tara=id_tara, nume_oras=nume).first()
        if existing_city:
            return JsonResponse({'error': 'City already exists for this country'}, status=409)

        # Save to the Cities model
        city = Orase.objects.create(id_tara=tara, nume_oras=nume, latitudine=lat, longitudine=lon)

        return JsonResponse({'id': city.id}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class OraseByCountryView(View):
    def get(self, request, id_Tara, *args, **kwargs):

        # Check if 'id_tara' exists in the Tari model
        if not Tari.objects.filter(id=id_Tara).exists():
            return JsonResponse({'error': 'Tara not found'}, status=404)

        orase = Orase.objects.filter(id_tara_id=id_Tara).values('id', 'id_tara', 'nume_oras','latitudine', \
                                                                'longitudine')
        formatted_orase = [{'id': entry['id'],'idTara': entry['id_tara'], 'nume': entry['nume_oras'], \
                            'lat': entry['latitudine'], 'lon': entry['longitudine']} for entry in orase]
        return JsonResponse(formatted_orase, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class OraseUpdateDeleteView(View):
    def put(self, request, id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            id_tara = data.get('idTara')

            # Check if 'idTara' exists in the Tari model
            if not Tari.objects.filter(id=id_tara).exists():
                return JsonResponse({'error': 'Tara not found'}, status=404)

            city = Orase.objects.get(id=id)
            city.id_tara_id = data.get('idTara')
            city.nume_oras = data.get('nume')
            city.latitudine = data.get('lat')
            city.longitudine = data.get('lon')
            city.save()

            return JsonResponse({}, status=200)

        except Orase.DoesNotExist:
            return JsonResponse({'error': 'City not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, id, *args, **kwargs):
        try:
            city = Orase.objects.get(id=id)
            city.delete()
            return JsonResponse({}, status=200)

        except Orase.DoesNotExist:
            return JsonResponse({'error': 'City not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class TemperaturiListCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        id_oras = data.get('idOras')
        valoare = data.get('valoare')

        # Check if 'id_oras' is provided
        if not id_oras:
            return JsonResponse({'error': 'not having an id_oras'}, status=400)
        
        existing_city = Orase.objects.filter(id=id_oras).first()

        # Check if 'existing_city' exists
        if not existing_city:
            return JsonResponse({'error': 'Oras not found'}, status=404)
        
        # Check if 'valoare' is provided
        if not valoare:
            return JsonResponse({'error': 'not having a value'}, status=400)

        # try Save to the Temperaturi model
        try:
            temperature = Temperaturi.objects.create(id_oras=existing_city, valoare=valoare)

            return JsonResponse({'id': temperature.id}, status=201)
        # error in saving to db
        except Exception as e:
            return JsonResponse({'error': f'Error: {str(e)}'}, status=409)
    
    def get(self, request, *args, **kwargs):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        start_date = request.GET.get('from')
        end_date = request.GET.get('until')

        queryset = Temperaturi.objects.all()

        city_ids = []

        if lat and lon:
            # Filter by both latitude and longitude
            cities = Orase.objects.filter(Q(latitudine=lat) & Q(longitudine=lon))
            city_ids = list(cities.values_list('id', flat=True))

            queryset = queryset.filter(id_oras__in=city_ids)
        else:
            if lat:
                # Filter by latitude
                cities = Orase.objects.filter(latitudine=lat)
                city_ids.extend(cities.values_list('id', flat=True))

            if lon:
                # Filter by longitude
                cities = Orase.objects.filter(longitudine=lon)
                city_ids.extend(cities.values_list('id', flat=True))

            if city_ids:
                queryset = queryset.filter(id_oras__in=city_ids)

        if start_date:
            try:
                # Check if start_date is in the correct format (assuming 'YYYY-MM-DD')
                datetime.strptime(start_date, '%Y-%m-%d')
                # Filter by start date
                queryset = queryset.filter(timestamp__gte=start_date)
            except ValueError:
                return JsonResponse({'error': 'Invalid start date format'}, status=400)

        if end_date:
            try:
                # Check if end_date is in the correct format (assuming 'YYYY-MM-DD')
                datetime.strptime(end_date, '%Y-%m-%d')
                # Filter by end date
                queryset = queryset.filter(timestamp__lte=end_date)
            except ValueError:
                return JsonResponse({'error': 'Invalid end date format'}, status=400)

        temperatures = list(queryset.values())
        formatted_temperaturi = [{'id': entry['id'], 'valoare': entry['valoare'], \
                                'timestamp': entry['timestamp'].strftime('%Y-%m-%d')} \
                                for entry in temperatures]
        return JsonResponse(formatted_temperaturi, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class TemperaturiByCityView(View):
    def get(self, request, id_oras, *args, **kwargs):
        start_date = request.GET.get('from')
        end_date = request.GET.get('until')

        queryset = Temperaturi.objects.filter(id_oras=id_oras)

        if start_date:
            try:
                # Check if start_date is in the correct format (assuming 'YYYY-MM-DD')
                datetime.strptime(start_date, '%Y-%m-%d')
                # Filter by start date
                queryset = queryset.filter(timestamp__gte=start_date)
            except ValueError:
                return JsonResponse({'error': 'Invalid start date format'}, status=400)

        if end_date:
            try:
                # Check if end_date is in the correct format (assuming 'YYYY-MM-DD')
                datetime.strptime(end_date, '%Y-%m-%d')
                # Filter by end date
                queryset = queryset.filter(timestamp__lte=end_date)
            except ValueError:
                return JsonResponse({'error': 'Invalid end date format'}, status=400)

        temperatures = list(queryset.values())
        formatted_temperaturi = [{'id': entry['id'], 'valoare': entry['valoare'], \
                                'timestamp': entry['timestamp'].strftime('%Y-%m-%d')} \
                                for entry in temperatures]
        return JsonResponse(formatted_temperaturi, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class TemperaturiByCountryView(View):
    def get(self, request, id_tara, *args, **kwargs):
        start_date = request.GET.get('from')
        end_date = request.GET.get('until')

        queryset = Temperaturi.objects.filter(id_oras__id_tara=id_tara)

        if start_date:
            try:
                # Check if start_date is in the correct format (assuming 'YYYY-MM-DD')
                datetime.strptime(start_date, '%Y-%m-%d')
                # Filter by start date
                queryset = queryset.filter(timestamp__gte=start_date)
            except ValueError:
                return JsonResponse({'error': 'Invalid start date format'}, status=400)

        if end_date:
            try:
                # Check if end_date is in the correct format (assuming 'YYYY-MM-DD')
                datetime.strptime(end_date, '%Y-%m-%d')
                # Filter by end date
                queryset = queryset.filter(timestamp__lte=end_date)
            except ValueError:
                return JsonResponse({'error': 'Invalid end date format'}, status=400)

        temperatures = list(queryset.values())
        formatted_temperaturi = [{'id': entry['id'], 'valoare': entry['valoare'], \
                                'timestamp': entry['timestamp'].strftime('%Y-%m-%d')} \
                                for entry in temperatures]
        return JsonResponse(formatted_temperaturi, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class TemperaturiRetrieveUpdateDestroyView(View):
    def put(self, request, id, *args, **kwargs):
        try:
            temperature = Temperaturi.objects.get(id=id)
            data = json.loads(request.body)
            temperature.id_oras_id = data['id_oras']
            temperature.valoare = data['valoare']
            temperature.timestamp = timezone.now()
            temperature.save()
            return JsonResponse({}, status=200)
        except Temperaturi.DoesNotExist:
            return JsonResponse({'error': 'Temperature not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, id, *args, **kwargs):
        try:
            temperature = Temperaturi.objects.get(id=id)
            temperature.delete()
            return JsonResponse({}, status=200)
        except Temperaturi.DoesNotExist:
            return JsonResponse({'error': 'Temperature not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        

