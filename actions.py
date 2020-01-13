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

logger = logging.getLogger(__name__)

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
		if value.lower() in self.location_db():
			# validation succeeded, set the value of the "location" slot to value
			return {entities.LOCATION, value.lower()}
		else:
			# validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
			dispatcher.utter_message(template='utter_ask_location')
			return {entities.LOCATION, None}

	def validate_cuisine(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain:Dict[Text, Any]) -> Dict[Text, Any]:
		"""validate cuisine value"""

		if value.lower() in self.cuisine_db():
			 # validation succeeded, set the value of the "cuisine" slot to value
			return {entities.CUISINE, value.lower()}
		else:
			# validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
			dispatcher.utter_message(template='utter_ask_cuisine')
			return {entities.CUISINE, None}

	def validate_budget(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain:Dict[Text, Any]) -> Dict[Text, Any]:
		"""validate cuisine value"""
		# Test code
		logger.log("validate budget is :" , value)
		return {entities.BUDGET, 700}

	def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
		# Test code
		# refactoring required
		zomato = zomatopy.initialize_app(config)
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		logger.log('RestaurantSearchForm : submit' , loc, cuisine)
		location_detail=zomato.get_location(loc, 1)
		d1 = json.loads(location_detail)
		lat=d1["location_suggestions"][0]["latitude"]
		lon=d1["location_suggestions"][0]["longitude"]
		cuisines_dict={
			'american' : 5,
			'chinese' : 25,
			'italian' : 55,
			'mexican' : 73,
			'north indian' : 50,
			'south indian' : 85
			}
		results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 5)
		d = json.loads(results)
		response=""
		if d['results_found'] == 0:
			response= "no results"
		else:
			for restaurant in d['restaurants']:
				response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+"\n"
		
		dispatcher.utter_message("-----"+response)
		return [SlotSet('location',loc)]

