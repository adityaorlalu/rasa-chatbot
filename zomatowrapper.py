import logging
from multiprocessing import Process, Manager
import json
import pandas as pd
import zomatopy
from typing import Text, Tuple

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Zomato user key
config={
	"user_key" : "c70b18b69ff112b04d76cebf3fa1a545"
	}

"""
This a wrapper class on top of zomato.py
"""
class ZomatoWapper():
    def __init__(self, location: Text):
        """ constructor """
        # Initialize zomato class
        self.__zomato = zomatopy.initialize_app(config)
        # inputed location
        self.__location = location


    def get_location(self) -> Tuple[Text, int, int, int] :
        """
            Method to call zomato location api and return api status, city_id, latitude and longitude
        """
        # initial values
        city_id = 0; latitude = 0; longitude = 0
        try:
            location_detail = self.__zomato.get_location(self.__location, 1)
        except Exception as err:
            # incase api raises exception
            logger.error("An exception occurred: %s", err)
            # return status as failed and initial values ('failed', 0, 0, 0)
            return 'failed', city_id, latitude, longitude

        jsonData = json.loads(location_detail)
        logger.info("API response : %s", jsonData)
        status = jsonData['status']

        # check status and suggestions list has elements
        if (jsonData['status'] == 'success' and len(jsonData['location_suggestions']) > 0) :
            # get city_id, latitude and longitude
            city_id = jsonData['location_suggestions'][0]['city_id']
            latitude = jsonData['location_suggestions'][0]['latitude']
            longitude = jsonData['location_suggestions'][0]['longitude']
            
        return status, city_id, latitude, longitude
    

    def get_cuisine_id(self, city_id: int, cuisine: Text) -> Tuple[Text, int]:
        """
            Method to call zomato cuisine id api and return api status and cuisine_id
        """
        # initial values
        cuisine_id = 0
        try:
            dict_data = self.__zomato.get_cuisines(city_id)
        except Exception as err:
            logger.error("An exception occurred: %s", err)
            # return status as failed and initial values ('failed', 0)
            return 'failed', cuisine_id

        logger.info("API response : %s", dict_data)
        # iterate through dictonary and check if value is as passed cuisine
        # assign the cuisine_id as key for the matched cuisine
        for key, value in dict_data.items():
            if (value.lower() == cuisine):
                cuisine_id = key
                break

        return 'success', cuisine_id
    

    def _restaurant_search_offset(self, offset: int, latitude: int, longitude:int, cuisine_id: int, count: int, list_obj:list):
        """
            This method is used for multiprocessing thread.
            This method search the restaurant based on latitude, longitude and cuisine_id

            Note: This multiprocessing is required as zomato has a limitation where it can give max restaurant count upto 20.
                  To get more results from zomato, we need to call search api with offset and count
            
            list_obj passed input is instance of Manager.list() object where we would be adding the result from search api
        """
        try:
            restaurant_details = self.__zomato.restaurant_search('&start=' + str(offset), latitude, longitude, str(cuisine_id), count)
        except Exception as err:
            logger.error("An exception occurred: %s", err)
            # return in case of exception
            return

        jsonData = json.loads(restaurant_details)
        # for each for the restaurant, add a entry in list_obj
        for restaurant in jsonData['restaurants']:
            # add a list entry with restaurant name, address, average cost for two and rating
            list_obj.append([restaurant['restaurant']['name'],
                restaurant['restaurant']['location']['address'],
                restaurant['restaurant']['average_cost_for_two'],
                restaurant['restaurant']['user_rating']['aggregate_rating']])


    def restaurant_search(self, latitude: int, longitude:int, cuisine_id: int) -> pd.DataFrame:
        """
            Method uses multiprocessing to get restaurant search from zomato api
            More infomation, check _restaurant_search_offset method
        """
        jobs = []
        manager = Manager()
        list_obj = manager.list()
        # create empty dataframe with columns 'Name', 'Address', 'Budget', 'Rating'
        df = pd.DataFrame(columns=['Name', 'Address', 'Budget', 'Rating'])        

        # run below loop for 10 times
        # offset is required as zomato has a limitation where it can give max restaurant count upto 20. providing offset will help in getting more results
        for offset in range(0, 40, 20):
            # create multiprocessing thread, list_obj will the object which will be updated from each thread if result found
            p = Process(target=self._restaurant_search_offset, args=(offset, latitude, longitude, cuisine_id, 20, list_obj))
            jobs.append(p)
            p.start()
        # join the jobs
        for job in jobs:
            job.join()

        # iterate through list_obj and add the resultant dataframe
        for innerlist in list_obj:
            df = df.append(pd.Series([innerlist[0], innerlist[1], innerlist[2], innerlist[3]], index=df.columns), ignore_index=True)

        return df
    

    def restaurant_search_by_location(self):
        _, city_id, latitude, longitude = self.get_location()
        _, cuisine_id = self.get_cuisine_id(city_id, 'south indian')
        return self.restaurant_search(latitude, longitude, cuisine_id)