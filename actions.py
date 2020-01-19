import logging
import json

from typing import Text, List, Dict, Union, Any, Tuple

from rasa_sdk import Tracker, Action
from rasa_sdk.events import (SlotSet, EventType)
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

import zomatopy
import entities
import intents
from zomatowrapper import ZomatoWapper
from mail import SendEmailWapper

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

config={
	"user_key":"c70b18b69ff112b04d76cebf3fa1a545"
	}

SENDER_EMAIL_ADDRESS = 'adityalalu@gmail.com'
SENDER_EMAIL_PASSWORD = 'Lalu_003'

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
			entities.BUDGET : self.from_entity(entity=entities.BUDGET, intent=[intents.RESTAURANT_SEARCH])
		}

	@staticmethod
	def cuisine_db() -> List[Text]:
		"""list of supported cuisines"""

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
		"""list of supported cuisines"""

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


	@staticmethod
	def determine_budget_range(budget:Text) -> Tuple[Text, Text]:
		"""
			Method to evaluate budget range
			Default - Moderate(300 - 700)
		"""
		budget_min = 300
		budget_max = 700
		if (budget == 'low') :
			budget_min = 0
			budget_max = 300
		elif(budget_max == 'high'):
			budget_min = 700
			budget_max = 1000

		return budget_min, budget_max


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
			dispatcher.utter_message(template="utter_ask_location")
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

		logger.info("validate budget is : %s", str(value))
		buget_min, budget_max = self.determine_budget_range(value)

		dispatcher.utter_message("Searching...")
		return {entities.BUDGET : value, entities.BUDGET_MAX: budget_max, entities.BUDGET_MIN:buget_min }


	def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
		"""
			Once all the required slots are filled, FormAction will call this method
			This method has a responsibility of calling zomato api and display results to users
		"""
		# initialise the variables will all the required slots
		location = tracker.get_slot(entities.LOCATION)
		cuisine = tracker.get_slot(entities.CUISINE)
		budget_max = tracker.get_slot(entities.BUDGET_MAX)
		budget_min = tracker.get_slot(entities.BUDGET_MIN)

		# initialise the zomato wrapper
		zomatoWapper = ZomatoWapper(config, location)

		# get city_id, latitude and longitude from zomato get_location api
		status, city_id, latitude, longitude = zomatoWapper.get_location()
		
		# below is the safer check to make sure api has successed and all required fields like (latitude, longitude and city_id) are populated
		# otherwise, display appropriate message to user
		if (status != 'success' or (latitude == 0 and longitude == 0 and city_id == 0)):
			dispatcher.utter_message("Presently we dont have offering for location %s.\n" %(location))
			dispatcher.utter_message(template='utter_ask_cuisine')
			return [SlotSet(entities.LOCATION, None)]

		# get cuisine_id from zomato cuisines api
		status, cuisine_id = zomatoWapper.get_cuisine_id(city_id, cuisine)

		# below is the safer check to make sure api has successed and cuisine_id is populated
		# otherwise, display appropriate message to user
		if (status != 'success' or cuisine_id == 0):
			dispatcher.utter_message("Presently we dont have offering for %s cuisine restaurant in location %s.\n" %(cuisine, location))
			dispatcher.utter_message(template='utter_ask_cuisine')
			return [SlotSet(entities.CUISINE, None)]
		
		# get restaurant search result from zomato search api. zomatowrapper will update the results in dataframe.
		df = zomatoWapper.restaurant_search(latitude, longitude, cuisine_id)

		# condition for no result
		# if no result, then display appropriate message to user
		if (df.shape[0] == 0):
			dispatcher.utter_message("Presently we dont have offering for %s cuisine restaurant in location %s.\n" %(cuisine, location))
			dispatcher.utter_message(template='utter_ask_cuisine')
			return [SlotSet(entities.CUISINE, None)]
		
		# filter the results based on budget range and sort based on customer rating
		df = df[(df['Budget'] < budget_max) & (df['Budget'] > budget_min)]
		df = df[df['Rating'] != 0]
		df = df.sort_values(by=['Rating'], ascending=False)[:10]
		df = df.reset_index()

		# below has the logic of displaying results to users
		response = 'Showing you top rated restaurants: \n'
		for row_index in range(0, 5):
			statement = "%s - '%s' in '%s' has been rated %s \n" %(str(row_index + 1), df['Name'][row_index], df['Address'][row_index], df['Rating'][row_index])
			response = response + statement
		dispatcher.utter_message(response)

		# lets create a list of results which we might require to send email if user opt for this.
		# this will be add as new slot 'email_content'
		details_for_email = []
		for row_index in range(0, df.shape[0]):
			details_for_email.append([df['Name'][row_index], df['Address'][row_index], df['Budget'][row_index], df['Rating'][row_index]])
		
		# create another slot which will be used in email formaction
		return [SlotSet('email_content', details_for_email)]


class SendEmailForm(FormAction):
	""" Form for sending email Search """
	
	def name(self) -> Text:
		"""unique name for seanding email form """
		return "send_email_form"

	
	@staticmethod
	def required_slots(tracker: Tracker) -> List[Text]:
		"""a list of required slot for send email"""

		return [
			entities.EMAIL_ID
		]
	
	def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
		"""a dictionary to map required solt for restaurant search"""
		return {
			entities.EMAIL_ID : [
				self.from_entity(entity=entities.EMAIL_ID),
				self.from_intent(intent=intents.AFFIRM, value=True),
                self.from_intent(intent=intents.DENY, value=False),
			]		
		}

	def validate_emailid(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain:Dict[Text, Any]) -> Dict[Text, Any]:
		"""validate email id value"""
		logger.info("validate email id is : %s", str(value))
		if (type(value) is not bool and '@' in value):
			# users has input valid email
			return {entities.EMAIL_ID : value.lower()}
		elif (value is True):
			# user has affirm, ask him to provided email address
			dispatcher.utter_message(template='utter_ask_emailid_details')
			return {entities.EMAIL_ID : None}
		else:
			# user has deny
			return {entities.EMAIL_ID : False}
	
	def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
		"""
			Once all the required slots are filled, FormAction will call this method
			This method has a responsibility of sending email to user based on emailid slot populated value
		"""
		# # initialise the variables will all the required slots
		email_content_list = tracker.get_slot('email_content')
		email_id = tracker.get_slot(entities.EMAIL_ID)
		location = tracker.get_slot(entities.LOCATION)
		cuisine = tracker.get_slot(entities.CUISINE)

		# user has denied for sending email. display appropriate message and return
		if (email_id is False):
			dispatcher.utter_message(template='utter_response_no_email')
			return []
		
		# below has the logic of displaying results to users via email
		subject = "Top rated %s restaurants from %s" %(cuisine, location)
		email_response = 'Hi, \n\n Below are the list of top rated restaurants:\n\n'
		for row in email_content_list:
			statement = 'Restaurant Name: %s\n' %(row[0])
			statement = statement + 'Restaurant locality address: %s\n' %(row[1])
			statement = statement + 'Average budget for two people: %s\n' %(row[2])
			statement = statement + 'Zomato user rating: %s\n\n' %(row[3])
			email_response = email_response + statement
		email_response = email_response + "\n Regards, \nZomato Team"

		# send the email to user
		status = SendEmailWapper.send(SENDER_EMAIL_ADDRESS, SENDER_EMAIL_PASSWORD, email_id, subject, email_response)
		# check if email send is success or failure and display appropriate message to user
		if (status is True):
			dispatcher.utter_message(template='utter_repsonse_email_sent_success')
		else:
			dispatcher.utter_message(template='utter_repsonse_email_sent_failed')
		return []