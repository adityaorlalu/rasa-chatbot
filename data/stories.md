## complete path
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "delhi"}
    - slot{"location": "delhi"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - restaurant_search_form
    - slot{"location": "delhi"}
    - utter_goodbye
## interactive_story_1
* greet
    - utter_greet
* restaurant_search
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "danapur"}
    - form: restaurant_search_form
    - slot{"location": null}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "delhi"}
    - form: restaurant_search_form
    - slot{"location": "delhi"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "chinese"}
    - form: restaurant_search_form
    - slot{"cuisine": "chinese"}
    - slot{"requested_slot": "budget"}
* form: budget_choice{"location": "<700", "budget": "<700"}
    - form: restaurant_search_form
    - slot{"budget": 700}
    - slot{"location": "delhi"}
    - form{"name": null}
    - slot{"requested_slot": null}
