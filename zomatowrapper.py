import logging
from multiprocessing import Process, Manager
import json
import pandas as pd

from typing import Text, Tuple

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

import zomatopy

config={
	"user_key":"c70b18b69ff112b04d76cebf3fa1a545"
	}

class ZomatoWapper():
    def __init__(self, location: Text):
        self.__zomato = zomatopy.initialize_app(config)
        self.__location = location

    def get_location(self) -> Tuple[Text, int, int, int] :
        city_id = 0; latitude = 0; longitude = 0
        try:
            location_detail = self.__zomato.get_location(self.__location, 1)
        except:
            logger.info("An exception occurred")
            return 'failed', city_id, latitude, longitude

        logger.info("API response : %s", location_detail)
        jsonData = json.loads(location_detail)
        logger.info("API response : %s", jsonData)
        status = jsonData['status']
        if (jsonData['status'] == 'success' and len(jsonData['location_suggestions']) > 0) :
            city_id = jsonData['location_suggestions'][0]['city_id']
            latitude = jsonData['location_suggestions'][0]['latitude']
            longitude = jsonData['location_suggestions'][0]['longitude']
            return status, city_id, latitude, longitude
        else:
            return status, 0, 0, 0
    
    def get_cuisine_id(self, city_id: int, cuisine: Text) -> Tuple[Text, int]:
        initial_key = 0
        try:
            dict_data = self.__zomato.get_cuisines(city_id)
        except:
            logger.info("An exception occurred")
            return 'failed', initial_key

        logger.info("API response : %s", dict_data)
        for key, value in dict_data.items():
            if (value.lower() == cuisine):
                initial_key = key
                break
        return 'success', initial_key
    
    def _restaurant_search_offset(self, offset: int, latitude: int, longitude:int, cuisine_id: int, count: int, list_obj:list):
        try:
            restaurant_details = self.__zomato.restaurant_search('&count=' + str(offset), latitude, longitude, str(cuisine_id), count)
        except:
            logger.info("An exception occurred")
            return
        jsonData = json.loads(restaurant_details)
        for restaurant in jsonData['restaurants']:
            list_obj.append([restaurant['restaurant']['name'],
                restaurant['restaurant']['location']['address'],
                restaurant['restaurant']['average_cost_for_two'],
                restaurant['restaurant']['user_rating']['aggregate_rating']])
        
    def restaurant_search(self, latitude: int, longitude:int, cuisine_id: int, limit: int):
        jobs = []
        manager = Manager()
        list_obj = manager.list()
        df = pd.DataFrame(columns=['Name', 'Address', 'Budget', 'Rating'])        


        for offset in range(0, 200, 20):
            p = Process(target=self._restaurant_search_offset, args=(offset, latitude, longitude, cuisine_id, 20, list_obj))
            jobs.append(p)
            p.start()

        for job in jobs:
            job.join()

        for innerlist in list_obj:
            df = df.append(pd.Series([innerlist[0], innerlist[1], innerlist[2], innerlist[3]], index=df.columns), ignore_index=True)
        
        print(df)

    def restaurant_search_old(self, latitude: int, longitude:int, cuisine_id: int, limit: int):
        for index in range(0, 201, 20):
            try:
                restaurant_details = self.__zomato.restaurant_search('&count=' + str(index), latitude, longitude, str(cuisine_id), limit)
            except:
                logger.info("An exception occurred")
                return []
            jsonData = json.loads(restaurant_details)

            for restaurant in jsonData['restaurants']:
                df = df.append(pd.Series([restaurant['restaurant']['name'],
                restaurant['restaurant']['location']['address'],
                restaurant['restaurant']['average_cost_for_two'],
                restaurant['restaurant']['user_rating']['aggregate_rating']], index=df.columns), ignore_index=True)
        
        print(df)


    
    def restaurant_search_by_location(self):
        _, city_id, latitude, longitude = self.get_location()
        _, cuisine_id = self.get_cuisine_id(city_id, 'south indian')
        self.restaurant_search(latitude, longitude, cuisine_id, 20)