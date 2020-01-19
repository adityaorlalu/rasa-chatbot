## interactive_story_1
* greet
    - utter_greet
* restaurant_search
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "bangalore"}
    - form: restaurant_search_form
    - slot{"location": "bangalore"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "chinese"}
    - form: restaurant_search_form
    - slot{"cuisine": "chinese"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "high"}
    - form: restaurant_search_form
    - slot{"budget": "high"}
    - slot{"budget_max": 700}
    - slot{"budget_min": 300}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: affirm
    - form: send_email_form
    - slot{"emailid": true}
    - slot{"emailid": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* restaurant_search{"emailid": "adityaorlalu@gmail.com"}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"emailid": "adityaorlalu@gmail.com"}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_2
* greet
    - utter_greet
* restaurant_search
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "delhi"}
    - form: restaurant_search_form
    - slot{"location": "delhi"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "north indian"}
    - form: restaurant_search_form
    - slot{"cuisine": "north indian"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "moderate"}
    - form: restaurant_search_form
    - slot{"budget": "moderate"}
    - slot{"budget_max": 700}
    - slot{"budget_min": 300}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: affirm
    - form: send_email_form
    - slot{"emailid": true}
    - slot{"emailid": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* restaurant_search{"emailid": "adityaorlalu@gmail.com"}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"emailid": "adityaorlalu@gmail.com"}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_1
* greet
    - utter_greet
* restaurant_search{"location": "nagpur"}
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"location": "nagpur"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "italian"}
    - form: restaurant_search_form
    - slot{"cuisine": "italian"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "low"}
    - form: restaurant_search_form
    - slot{"budget": "low"}
    - slot{"budget_max": 300}
    - slot{"budget_min": 0}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: affirm
    - form: send_email_form
    - slot{"emailid": true}
    - slot{"emailid": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* restaurant_search{"emailid": "nishikumari@gmail.com"}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"emailid": "nishikumari@gmail.com"}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_1
* greet
    - utter_greet
* restaurant_search{"location": "patna"}
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"location": "patna"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "american"}
    - form: restaurant_search_form
    - slot{"cuisine": "american"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "moderate"}
    - form: restaurant_search_form
    - slot{"budget": "moderate"}
    - slot{"budget_max": 700}
    - slot{"budget_min": 300}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: affirm
    - form: send_email_form
    - slot{"emailid": true}
    - slot{"emailid": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* restaurant_search{"emailid": "abc@edu.xyz"}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"emailid": "abc@edu.xyz"}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_1
* restaurant_search{"cuisine": "south indian", "location": "ranchi"}
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"location": "ranchi"}
    - slot{"cuisine": "south indian"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "moderate"}
    - form: restaurant_search_form
    - slot{"budget": "moderate"}
    - slot{"budget_max": 700}
    - slot{"budget_min": 300}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: affirm
    - form: send_email_form
    - slot{"emailid": true}
    - slot{"emailid": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* restaurant_search{"emailid": "abhishek_sdf@eedu.go.in"}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"emailid": "abhishek_sdf@eedu.go.in"}
    - form{"name": null}
    - slot{"requested_slot": null}
* goodbye{"location": "thanks"}
    - utter_goodbye

## interactive_story_1
* greet
    - utter_greet
* restaurant_search{"location": "chennai"}
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"location": "chennai"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "american"}
    - form: restaurant_search_form
    - slot{"cuisine": "american"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "high"}
    - form: restaurant_search_form
    - slot{"budget": "high"}
    - slot{"budget_max": 700}
    - slot{"budget_min": 300}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: affirm
    - form: send_email_form
    - slot{"emailid": true}
    - slot{"emailid": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* restaurant_search{"emailid": "asdfasf@asdfasdf.com.sd"}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"emailid": "asdfasf@asdfasdf.com.sd"}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_1
* restaurant_search{"cuisine": "chinese", "location": "patna"}
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"location": "patna"}
    - slot{"cuisine": "chinese"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "low"}
    - form: restaurant_search_form
    - slot{"budget": "low"}
    - slot{"budget_max": 300}
    - slot{"budget_min": 0}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: deny
    - form: send_email_form
    - slot{"emailid": false}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_1
* restaurant_search
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "patna"}
    - form: restaurant_search_form
    - slot{"location": "patna"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "mexican"}
    - form: restaurant_search_form
    - slot{"cuisine": "mexican"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "low"}
    - form: restaurant_search_form
    - slot{"budget": "low"}
    - slot{"budget_max": 300}
    - slot{"budget_min": 0}
    - slot{"cuisine": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* restaurant_search{"cuisine": "chinese"}
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"location": "patna"}
    - slot{"budget": "low"}
    - slot{"budget_max": 300}
    - slot{"budget_min": 0}
    - slot{"cuisine": "chinese"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: restaurant_search{"emailid": "adityaorlalu@gmail.com"}
    - form: send_email_form
    - slot{"emailid": "adityaorlalu@gmail.com"}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_1
* restaurant_search{"cuisine": "american", "location": "ranchi"}
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"location": "ranchi"}
    - slot{"cuisine": "american"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "low"}
    - form: restaurant_search_form
    - slot{"budget": "low"}
    - slot{"budget_max": 300}
    - slot{"budget_min": 0}
    - slot{"cuisine": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* restaurant_search{"cuisine": "south indian"}
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"location": "ranchi"}
    - slot{"budget": "low"}
    - slot{"budget_max": 300}
    - slot{"budget_min": 0}
    - slot{"cuisine": "south indian"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: deny
    - form: send_email_form
    - slot{"emailid": false}
    - form{"name": null}
    - slot{"requested_slot": null}
* goodbye
    - utter_goodbye

## interactive_story_1
* greet
    - utter_greet
* restaurant_search
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "bangalore"}
    - form: restaurant_search_form
    - slot{"location": "bangalore"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "italian"}
    - form: restaurant_search_form
    - slot{"cuisine": "italian"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "moderate"}
    - form: restaurant_search_form
    - slot{"budget": "moderate"}
    - slot{"budget_max": 700}
    - slot{"budget_min": 300}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: restaurant_search{"emailid": "ahdcdj@dkj.com"}
    - form: send_email_form
    - slot{"emailid": "ahdcdj@dkj.com"}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_1
* greet
    - utter_greet
* restaurant_search{"location": "rishikesh"}
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"location": null}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "prayagraj"}
    - form: restaurant_search_form
    - slot{"location": "prayagraj"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "chinese"}
    - form: restaurant_search_form
    - slot{"cuisine": "chinese"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "high"}
    - form: restaurant_search_form
    - slot{"budget": "high"}
    - slot{"budget_max": 700}
    - slot{"budget_min": 300}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: restaurant_search{"emailid": "xyz@sth.edu"}
    - form: send_email_form
    - slot{"emailid": "xyz@sth.edu"}
    - form{"name": null}
    - slot{"requested_slot": null}
* goodbye
    - utter_goodbye

## interactive_story_1
* greet
    - utter_greet
* restaurant_search{"location": "guwathi"}
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"location": null}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "gwathati"}
    - form: restaurant_search_form
    - slot{"location": null}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "kolkota"}
    - form: restaurant_search_form
    - slot{"location": null}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "kochi"}
    - form: restaurant_search_form
    - slot{"location": "kochi"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "american"}
    - form: restaurant_search_form
    - slot{"cuisine": "american"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "moderate"}
    - form: restaurant_search_form
    - slot{"budget": "moderate"}
    - slot{"budget_max": 700}
    - slot{"budget_min": 300}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: deny
    - form: send_email_form
    - slot{"emailid": false}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_1
* greet
    - utter_greet
* restaurant_search
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "mubaim"}
    - form: restaurant_search_form
    - slot{"location": null}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "mumbai"}
    - form: restaurant_search_form
    - slot{"location": "mumbai"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "american"}
    - form: restaurant_search_form
    - slot{"cuisine": "american"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "low"}
    - form: restaurant_search_form
    - slot{"budget": "low"}
    - slot{"budget_max": 300}
    - slot{"budget_min": 0}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: affirm
    - form: send_email_form
    - slot{"emailid": true}
    - slot{"emailid": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* restaurant_search{"emailid": "samgoryal@ddddd.com"}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"emailid": "samgoryal@ddddd.com"}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_1
* greet
    - utter_greet
* restaurant_search{"cuisine": "chinese", "location": "chandigarh"}
    - restaurant_search_form
    - form{"name": "restaurant_search_form"}
    - slot{"location": "chandigarh"}
    - slot{"cuisine": "chinese"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "low"}
    - form: restaurant_search_form
    - slot{"budget": "low"}
    - slot{"budget_max": 300}
    - slot{"budget_min": 0}
    - form{"name": null}
    - slot{"requested_slot": null}
    - send_email_form
    - form{"name": "send_email_form"}
    - slot{"requested_slot": "emailid"}
* form: deny
    - form: send_email_form
    - slot{"emailid": false}
    - form{"name": null}
    - slot{"requested_slot": null}
