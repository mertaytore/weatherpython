import urllib2, urllib, json

class Weather:
    def get_forecast(self, input, day_input):

        ##### In case something goes wrong.
        def error_message(errno):
            message = ""
            if errno == 1:
                message = "Could not recognize."
            if errno == 2:
                message = "How did you end up here??"
            return message

        ##### I used Yahoo's Fahrenheit results. Below function is not needed if Celcius results are used.
        def fah_to_celc(fah):
            celc = ((float(fah) - 32) * 5 ) / 9
            return int(celc)

        ##### Interpretation of string to integers.
        ##### Of course making the conversion from string to integer can be done by entity extraction but
        ##### the API just could not get it there. There might be a better solution, but until then:
        def day_calc(day_count):
            next_days = 0
            if "TOMORROW" in day_count:
                next_days = 1
            elif "TODAY" in day_count:
                next_days = 0
            elif "TWO" in day_count:
                next_days = 2
            elif "THREE" in day_count:
                next_days = 3
            elif "FOUR" in day_count:
                next_days = 4
            elif "FIVE" in day_count:
                next_days = 5
            elif "SIX" in day_count:
                next_days = 6
            elif "SEVEN" in day_count:
                next_days = 7
            elif "WEEK" in day_count: #### JSON doesn't recognize week :P
                next_days = 7
            return next_days

        try:
            baseurl = "https://query.yahooapis.com/v1/public/yql?"
            
            #### Insert your Yahoo Weather API key below
            yahoo_api_key = " "

            #city name comes from the user
            city_name = input

            #to cause no troubles in the URL
            city_name_url = city_name.replace(" ", "")

            ##### WOE (Where on Earth) ID of the city #####
            try:
                #### This solution IS NOT okay.
                #### Fetching data and so on.
                if city_name_url == "SINGAPORE":
                    result = urllib2.urlopen("http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.places%20where%20text%3D\""+ city_name_url +"\"&format=json").read()
                    data = json.loads(result)
                    city_woeid = data['query']['results']['place'][1]['woeid']

                result = urllib2.urlopen("http://where.yahooapis.com/v1/places.q('"+ city_name_url +
                    "')?appid=" + yahoo_api_key + "&format=json").read()
                data = json.loads(result)
                city_woeid = data['places']['place'][0]['admin1 attrs']['woeid']
            except:
                result = urllib2.urlopen("http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.places%20where%20text%3D\""+ city_name_url +"\"&format=json").read()
                data = json.loads(result)
                city_woeid = data['query']['results']['place'][1]['woeid']


            ##### Finding the properties of the city with woeid #####
            yql_query = "select * from weather.forecast where woeid=" + str(city_woeid)
            yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
            result = urllib2.urlopen(yql_url).read()
            data = json.loads(result)

            ##### Finding city's properties with yql queries. #####

            # below query can retrieve the city name in Yahoo's database but the input city
            # name is used to print.

            # data['query']['results']['channel']['location']['city']

            output_result = ""

            day_condition = day_calc(day_input)
            city_condition = data['query']['results']['channel']['item']['condition']['text']
            fahrenheit_high = data['query']['results']['channel']['item']['forecast'][0]['high']
            fahrenheit_low = data['query']['results']['channel']['item']['forecast'][0]['low']
            temperature_now = data['query']['results']['channel']['item']['condition']['temp']

            output_result = "It is " + (city_condition + " and " + str(fah_to_celc(temperature_now))
                                     + " Celcius degrees in " + city_name + " today.\n")

            for x in range(0,day_condition):

                # Fetch data for consecutive days
                forecast_date = data['query']['results']['channel']['item']['forecast'][x+1]['date']
                forecast_day = data['query']['results']['channel']['item']['forecast'][x+1]['day']
                city_condition = data['query']['results']['channel']['item']['forecast'][x+1]['text']
                fahrenheit_high = data['query']['results']['channel']['item']['forecast'][x+1]['high']
                fahrenheit_low = data['query']['results']['channel']['item']['forecast'][x+1]['low']

                if( day_condition != 0):
                    output_result = output_result + ("It will be " + city_condition + ", highest " + str(fah_to_celc(fahrenheit_high))
                                                  + " and lowest " + str(fah_to_celc(fahrenheit_low)) + " on " + forecast_date + " in "
                                                  + city_name + ".\n")
            return output_result

        except:
            print (error_message(1))

    def __init__(self):
        return None
