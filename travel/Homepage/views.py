from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import requests
import json
from django.utils import timezone
from Homepage.models import Transactions
from datetime import datetime
from geopy.geocoders import Nominatim
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail


def get_hotels_by_coordinates_from_api(start_date, end_date, destination, nb_adults, nb_kids) -> 'list':
        #Upon entering the parameters into the function, the api returns us a json object which contains all the info we wish to use in later functions
    name = Nominatim(user_agent='Jihad')                                                                    
    location = name.geocode(destination)
    latitude = location.latitude        
    longitude = location.longitude      
    url = "https://booking-com.p.rapidapi.com/v1/hotels/search-by-coordinates"
    querystring = {"checkin_date": start_date, "order_by": "popularity", "units": "metric", "longitude": longitude, "adults_number": nb_adults, "latitude": latitude, "room_number": "1", "locale": "en-gb",
                   "filter_by_currency": "USD", "checkout_date": end_date, "children_number": nb_kids, "children_ages": "5,0", "page_number": "0", "categories_filter_ids": "class::2,class::4,free_cancellation::1", "include_adjacency": "true"}
    if nb_kids == '':
        querystring.pop('children_number')
    headers = {
        'x-rapidapi-host': "booking-com.p.rapidapi.com",
        'x-rapidapi-key': "f0316cac40msh76d4493eeaf0626p13601fjsna26c9566032c"
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    info = json.loads(response.text)    #info now contains everything we need from the booking.com api
    print(info)
    return info


def get_all_bought_hotels_from_database() -> 'list':    #booking the hotel adds it to a list in order to not be shown the next time we search.
    liste_of_transactions = Transactions.objects.all()
    hotels_bought = []
    for hotels in liste_of_transactions:
        hotels_bought.append(hotels.Hotel_name)
    return hotels_bought


def create_list_of_hotels(info, hotels_bought, list_of_hotels): 
    #we extract the needed items from "info" in order to store them into templates exclusive to every hotel, with some additional items used for the "book now" and "get news" functions along with the lat and long for the "view on map: button
    for i in range(0, len(info['result'])):
        dict = {}
        if '/' not in info['result'][i]['hotel_name'] and info['result'][i]['address_trans'] != '' and '/' not in info['result'][i]['address_trans']:
            if info['result'][i]['hotel_name'] not in hotels_bought:
                dict['Hotel_name'] = info['result'][i]['hotel_name']
                dict['hotel_city'] = info['result'][i]['city_trans']
                dict['hotel_address'] = info['result'][i]['address_trans']
                dict['price'] = str(info['result'][i]['price_breakdown']
                                    ['gross_price'])+' '+info['result'][i]['currencycode']
                dict['image_url'] = str(info['result'][i]['max_photo_url'])
                dict['id_Hotel'] = str(info['result'][i]['id'][14:])
                dict['rating'] = info['result'][i]['review_score']
                dict['checkin_date'] = info['result'][i]['checkin']['from']
                dict['longitude_city'] = str(info['result'][i]['longitude'])
                dict['latitude_city'] = str(info['result'][i]['latitude'])

                list_of_hotels.append(dict)


def get_landmarks_from_api(id):     # to be used in book now
    url_landmarks = "https://booking-com.p.rapidapi.com/v1/hotels/nearby-places"
    querystring1 = {"locale": "en-gb", "hotel_id": id}
    headers1 = {
        'x-rapidapi-host': "booking-com.p.rapidapi.com",
        'x-rapidapi-key': "f0316cac40msh76d4493eeaf0626p13601fjsna26c9566032c"
    }
    response1 = requests.request(
        "GET", url_landmarks, headers=headers1, params=querystring1)
    info = json.loads(response1.text)
    return info


def get_hotel_images_from_api(id):  # to be used in book now
    url_images = "https://booking-com.p.rapidapi.com/v1/hotels/photos"
    querystring2 = {"locale": "en-gb", "hotel_id": id}

    headers2 = {
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com",
        "X-RapidAPI-Key": 'f0316cac40msh76d4493eeaf0626p13601fjsna26c9566032c'
    }
    response2 = requests.request(
        "GET", url_images, headers=headers2, params=querystring2)
    response2 = json.loads(response2.text)
    return response2


def get_hotel_description_from_api(id): # to be used in book now
    url_desc = "https://booking-com.p.rapidapi.com/v1/hotels/description"

    querystring3 = {"hotel_id": id, "locale": "en-gb"}

    headers3 = {
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com",
        "X-RapidAPI-Key": 'f0316cac40msh76d4493eeaf0626p13601fjsna26c9566032c'
    }

    response3 = requests.request(
        "GET", url_desc, headers=headers3, params=querystring3)
    response3 = json.loads(response3.text)
    hotel_desc = response3['description']
    return hotel_desc


def get_touristic_monuments_from_api(id):   #to be used in book now
    url4 = "https://booking-com.p.rapidapi.com/v1/hotels/nearby-places"
    querystring4 = {"locale": "en-gb", "hotel_id": id}
    headers4 = {
        'x-rapidapi-host': "booking-com.p.rapidapi.com",
        'x-rapidapi-key': 'f0316cac40msh76d4493eeaf0626p13601fjsna26c9566032c'
    }
    response4 = requests.request(
        "GET", url4, headers=headers4, params=querystring4)
    info = json.loads(response4.text)
    return info


@login_required(login_url='/login/  ')  # using django, we can block the user from generating the hotels and redirect him to the login page if he accesses the homepage without being logged in
def hotels_generator(request):
    if request.method == 'POST':
        start_date = request.POST.get("trip-start")
        end_date = request.POST.get("trip-end")
        if start_date > end_date or start_date < str(datetime.date(datetime.now())) or end_date < str(datetime.date(datetime.now())):
            return render(request, 'Homepage/homepage.html', {'l': ['error']}) # used in the html/django code to indicate an error in the date input.
        date_diff = datetime.fromisoformat(
            end_date)-datetime.fromisoformat(start_date)
        if date_diff.days >= 30:
            return render(request, 'Homepage/homepage.html', {'li': ['error']})
        destination = request.POST.get("Destination")
        nb_adults = request.POST.get("numofadults")
        nb_kids = request.POST.get("numofkids")

        info = get_hotels_by_coordinates_from_api(
            start_date=start_date, end_date=end_date, destination=destination, nb_adults=nb_adults, nb_kids=nb_kids)
        list_of_hotels = []
        hotels_bought = get_all_bought_hotels_from_database()
        create_list_of_hotels(
            info=info, hotels_bought=hotels_bought, list_of_hotels=list_of_hotels)
        return render(request, 'Homepage/Template.html', {'l': list_of_hotels}) # sends the list of hotels to template.html and redirects the user to the homepage where all the hotels are shown.
    else:
        return render(request, 'Homepage/homepage.html')


def Get_News(destination):      # we use a websearch api using the destination as the topic and it returns us the most relevant news regarding the topic(destination)
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"

    querystring = {"q": destination, "pageNumber": "1", "pageSize": "4", "autoCorrect": "true",
                   "safeSearch": "true", "withThumbnails": "true", "fromPublishedDate": "null", "toPublishedDate": "null"}

    headers = {
        "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "5825d2c943mshecefe03fc214646p14a20bjsn2566751bd456"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    info_news = json.loads(response.text)
    print(info_news)
    return info_news


def book_now(request, id_hotel, name, add, destination):    # gets all the needed info and redirects the user to the hotel page that they selected which contains news,nearby monuments and landmarks, hotel image, description.
    Hotel_landmarks = []
    landmarks = get_landmarks_from_api(id_hotel)
    for i in landmarks['landmarks']['closests']:
        Hotel_landmarks.append(i['landmark_name']+'  '+str(i['distance'])+' m')

    hotel_images_url = []
    response2 = get_hotel_images_from_api(id=id_hotel)
    for i in response2:
        hotel_images_url.append(i['url_max'])

    hotel_desc = get_hotel_description_from_api(id=id_hotel)

    liste_of_monuments = []
    info = get_touristic_monuments_from_api(id=id_hotel)
    for i in info['landmarks']['populars']:
        liste_of_monuments.append(
            i['landmark_name']+'  '+str(i['distance'])+' m')

    list_news = []
    info = Get_News(destination)
    for i in info["value"]:
        dict_news = {}
        dict_news["title"] = i["title"]
        dict_news["article_url"] = i["url"]
        dict_news["description"] = i["description"]
        dict_news["image"] = i["image"]["url"]
        list_news.append(dict_news)

    return render(request, 'Homepage/Hotels_page.html', {'l': Hotel_landmarks, 'name': name, 'add': add, 'img': hotel_images_url, 'desc': hotel_desc, 'l2': liste_of_monuments, "lnews": list_news})


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('loginpage:check_user'))


def about_us(request):
    return render(request, 'Homepage/AboutUs.html')


def contact_us(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email_address_client = request.POST.get('mail')
        country = request.POST.get('country')
        send_mail(
            'From '+name+' '+last_name+' '+country,
            subject,
            email_address_client,
            ['traveltrailhelp@gmail.com'],
            fail_silently=False,
        )
        return render(request, 'Homepage/contact.html')
    else:
        return render(request, 'Homepage/contact.html')


def Buy_now(request, name):
    transaction = Transactions(
        Hotel_name=name, user=request.user, purchase_time=timezone.now())
    transaction.save()
    print('ok')
    return HttpResponseRedirect(reverse('Homepage:hotels_generator'))
