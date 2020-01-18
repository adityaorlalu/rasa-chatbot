import logging
import json

from typing import Text, List, Dict, Union, Any

from rasa_sdk import Tracker,Action
from rasa_sdk.events import (SlotSet, EventType)
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

import zomatopy
import entities
import intents
from zomatowrapper import ZomatoWapper

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

config={
	"user_key":"c70b18b69ff112b04d76cebf3fa1a545"
	}

class RestaurantSearchForm(FormAction):
	""" Form for Restaurant Search """
	
	def name(self) -> Text:
		"""unique name for restaurant search form """

		return "restaurant_search_form"
	
	@staticmethod
	def required_slots(tracker: Tracker) -> List[Text]:
		"""a list of required slot for restaurant search"""

		return [
			entities.LOCATION,
			entities.CUISINE,
			entities.BUDGET
		]

	
	def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
		"""a dictionary to map required solt for restaurant search"""

		return {
			entities.LOCATION : self.from_entity(entity=entities.LOCATION, intent=[intents.RESTAURANT_SEARCH]),
			entities.CUISINE : self.from_entity(entity=entities.CUISINE, intent=[intents.RESTAURANT_SEARCH]),
			entities.BUDGET : [
				self.from_entity(entity=entities.BUDGET, intent=[intents.BUDGET_CHOICE]),
				self.from_entity(entity=entities.USER_CHOICE)
			]
		}

	@staticmethod
	def cuisine_db() -> List[Text]:
		"""Database of supported cuisines"""

		return [
			'chinese',
			'mexican',
			'italian',
			'american',
			'south indian',
			'north indian'
        ]
	
	@staticmethod
	def location_db() -> List[Text]:
		"""Database of supported cuisines"""

		return [
			'bangalore', 'chennai', 'delhi', 'hyderabad', 'kolkata', 'mumbai', 'ahmedabad', 'pune',
			'agra', 'ajmer', 'aligarh', 'amravati', 'amritsar', 'asansol', 'aurangabad', 'bareilly', 'belgaum', 'bhavnagar', 
			'bhiwandi', 'bhopal', 'bhubaneswar', 'bikaner', 'bilaspur', 'bokaro steel city', 'chandigarh', 'coimbatore',
			'nagpur', 'cuttack', 'dehradun', 'dhanbad', 'bhilai', 'durgapur', 'erode', 'faridabad', 'firozabad', 'ghaziabad',
			'gorakhpur', 'gulbarga', 'guntur', 'gwalior', 'gurgaon', 'guwahati', 'hamirpur',
			'hubli–dharwad', 'indore', 'jabalpur', 'jaipur', 'jalandhar', 'jammu', 'jamnagar', 'jamshedpur', 'jhansi', 'jodhpur',
			'kakinada', 'kannur', 'kanpur', 'kochi', 'kolhapur', 'kollam', 'kozhikode', 'kurnool', 'ludhiana', 'lucknow', 'madurai',
			'malappuram', 'mathura', 'goa', 'mangalore', 'meerut', 'moradabad', 'mysore', 'nanded', 'nashik', 'nellore', 'noida',
			'patna', 'pondicherry', 'purulia', 'prayagraj', 'raipur', 'rajkot', 'rajahmundry', 'ranchi', 'rourkela', 'salem', 'sangli',
			'shimla', 'siliguri', 'solapur', 'srinagar', 'thiruvananthapuram', 'thrissur', 'tiruchirappalli', 'tiruppur', 'ujjain',
			'bijapur', 'vadodara', 'varanasi', 'vasai-virar city', 'vijayawada', 'vellore', 'warangal', 'surat', 'visakhapatnam'
        ]


	def validate_location(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain:Dict[Text, Any]) -> Dict[Text, Any]:
		"""validate location value"""
		logger.info("validate location is : %s", str(value))
		if value.lower() in self.location_db():
			# validation succeeded, set the value of the "location" slot to value
			return {entities.LOCATION : value.lower()}			
		else:
			# validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
			dispatcher.utter_message("Presently we dont have offering for location %s.\n Please choose some other location." %(value))
			dispatcher.utter_template("utter_ask_location")
			return {entities.LOCATION : None}


	def validate_cuisine(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain:Dict[Text, Any]) -> Dict[Text, Any]:
		"""validate cuisine value"""
		logger.info("validate cuisine is : %s", str(value))
		location = tracker.get_slot(entities.LOCATION)
		if value.lower() in self.cuisine_db():
			 # validation succeeded, set the value of the "cuisine" slot to value
			return {entities.CUISINE : value.lower()}
		else:
			# validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
			dispatcher.utter_message("Presently we dont have offering for %s cuisine restaurant in location %s.\n" %(value, location))
			dispatcher.utter_message(template='utter_ask_cuisine')
			return {entities.CUISINE : None}


	def validate_budget(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain:Dict[Text, Any]) -> Dict[Text, Any]:
		"""validate budget value"""
		# Test code
		logger.info("validate budget is : %s", str(value))
		return {entities.BUDGET : 700, entities.BUDGET_MAX: 700, entities.BUDGET_MIN:300 }


	def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
		location = tracker.get_slot(entities.LOCATION)
		cuisine = tracker.get_slot(entities.CUISINE)
		budget_max = tracker.get_slot(entities.BUDGET_MAX)
		budget_min = tracker.get_slot(entities.BUDGET_MIN)

		zomatoWapper = ZomatoWapper(location)

		status, city_id, latitude, longitude = zomatoWapper.get_location()
		if (status != 'success'):
			dispatcher.utter_message("Presently we dont have offering for location %s.\n" %(location))
			dispatcher.utter_template('utter_ask_cuisine')
			return [SlotSet(entities.LOCATION, None)]

		status, cuisine_id = zomatoWapper.get_cuisine_id(city_id, cuisine)
		if (status != 'success'):
			dispatcher.utter_message("Presently we dont have offering for %s cuisine restaurant in location %s.\n" %(cuisine, location))
			dispatcher.utter_template('utter_ask_cuisine')
			return [SlotSet(entities.CUISINE, None)]
		
		df = zomatoWapper.restaurant_search(latitude, longitude, cuisine_id)

		if (df.shape[0] == 0):
			dispatcher.utter_message("Presently we dont have offering for %s cuisine restaurant in location %s.\n" %(cuisine, location))
			dispatcher.utter_template('utter_ask_cuisine')
			return [SlotSet(entities.CUISINE, None)]
		
		df = df[(df['Budget'] < budget_max) & (df['Budget'] > budget_min) ]
		df = df.sort_values(by=['Rating'], ascending=False)[:10]
		df = df.reset_index()

		response = 'Showing you top rated restaurants: \n'
		for row_index in range(0, 5):
			statement = "%s - '%s' in '%s' has been rated %s \n" %(str(row_index + 1), df['Name'][row_index], df['Address'][row_index], df['Rating'][row_index])
			response = response + statement
		dispatcher.utter_message(response)

		details_for_email = []
		for row_index in range(0, df.shape[0]):
			details_for_email.append([df['Name'][row_index], df['Address'][row_index], df['Budget'][row_index], df['Rating'][row_index]])
		
		return [SlotSet('email_content', details_for_email)]

		# # Test code
		# # refactoring required
		# zomato = zomatopy.initialize_app(config)
		# loc = tracker.get_slot('location')
		# cuisine = tracker.get_slot('cuisine')
		# logger.info('RestaurantSearchForm : submit -> {loc} {cuisine}')
		# logger.info("validate cuisine is : %s %s", str(loc) , str(cuisine))
		# location_detail=zomato.get_location(loc, 1)
		# d1 = json.loads(location_detail)
		# lat=d1["location_suggestions"][0]["latitude"]
		# lon=d1["location_suggestions"][0]["longitude"]
		# cuisines_dict={
		# 	'american' : 5,
		# 	'chinese' : 25,
		# 	'italian' : 55,
		# 	'mexican' : 73,
		# 	'north indian' : 50,
		# 	'south indian' : 85
		# 	}
		# results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 5)
		# d = json.loads(results)
		# response=""
		# if d['results_found'] == 0:
		# 	response= "no results"
		# else:
		# 	for restaurant in d['restaurants']:
		# 		response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+"\n"
		
		# dispatcher.utter_message("-----"+response)
		# return [SlotSet('location',loc)]

