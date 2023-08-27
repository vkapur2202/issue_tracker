# issue_tracker

Basic API setup for a github issue tracker app. 

Webhook setup in repository settings: 
This repo uses hookdeck to replicate webhooks in a production setting by sending requests to a hookdeck endpoint and redirecting them to localhost:8000

Main idea is to have a read only API that a frontend can access, but have all write requests send directly to the github API.
Relies on github webhooks to handle create, update, and deletes in the databse.

Requirements:
Python 3.10+
django
djangorestframework
hookdeck
