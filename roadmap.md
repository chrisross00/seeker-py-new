# Roadmap

## Priority
  * Don't send SMS until morning
  * Blueprints might be used wrong... need to investigate. Could clone the whole thing and then start trying to set up the db without any blueprint stuff
    * Either way, blueprints is the key to setting up separate route handlers
  * Need messages to user
    * Login
    * Whether a search parameter already exists or is new

* Config table - app config
  * Config for job runners and jobs
  * Config for Search
  * Config for Twilio
* Dev vs prod differentiation
  * Required to get to Heroku
* VS code install to work from iPad via Google VM
* Fix python3 install
* Rename that twilio status column too
* Don't store to OutQuery if no child tables
* Route Handler pattern

## Notes
https://www.youtube.com/watch?v=SiCAIRc0pEI
* Really helpful walkthrough deploying a flask app to Heroku
* Important commands to update a database after changing models/columns etc
  * `flask db init`
  * `flask db migrate`
  * `flask db upgrade`

* Adding new models:
  * add the model file to the model folder
  * import the model to the `blueprints.py` file
    * build a blueprint for 
  * import the model to `application.py`
    * add it to the BLUEPRINTS list
  * Update the db as described above (flask db migrate)

* Pushing to Heroku
  * git push heroku master
  * 

## Backlog
* Added FE to update queries! 
  * Need to show query parameters in the front end, and give user a way to update them
    * Store and save the query parameters, then show on the page
    * When the user changes them, update them
      * **Test: can change configuration and save (job and/or parameter) and the job running picks it up**

* Google OAuth: Need auth - otherwise anyone can just pop in and possibly get my reddit creds/twilio creds
* Added INSERT DATE to 
  * Message table
* Added Last_Used_Date to
  * SearchParameters

* **Deployed to Heroku!!! It's Live!!!**
  * 4/28 - deployed to heroku, everything builds. But need, in order to actually have a usable app: :white_check_mark:
    * Figure out the environment variable thing because there is no .env file in prod. 
      * Working on test in runmain :white_check_mark:
      * All ngrok and get_auth_config stuff needs to be redone :white_check_mark:
      * SQL_ALCHEMY stuff on application.py :white_check_mark:
      * Make production env vars :white_check_mark:
    * SSL - Upgraded to hobby version for $7 per month 

* **Come up with better SMS handling**
  * Could design a whole text/command interpretation system
  * Should mimic something like Slack 
  * Help command?
  * 

* **List comprehension refactor**
  * Get rid of for loops where possible, see if it improves performance

* **Create Twilio Class** :white_check_mark:
  * That way you make sure to use one Twilio instance and pass it to objects that need it :white_check_mark:

* **Message Reddit**
  * Accept an SMS response, then message the author based on the result_id
  * Default to a dummy post (find my old Yugo post, maybe) to test
  * 

* **SMS response handling**
  * Just get Twilio to accept a response and pass it back to the app :white_check_mark:
    * Note: This might force having a web server up :white_check_mark:
      * https://www.twilio.com/docs/video/tutorials/get-started-with-twilio-video-python-flask-server
      * Post-implementation note: Using ngrok (via cmd) as the web server
      * Requires manual update to Twilio webhook since ngrok url is randomly generated
  * Compare response against list of id's sent via text
    * Build and store a list
      * Status
 * Test handling other SMS user responses :white_check_mark:
    * Post-test note: basically you can get the body off of whatever a user sends when it redirects to the ngrok endpoint. 
    * If you want to do different things or repeatable commands (reminders, notes, emails), you might want to implement a (product-required) syntax structure that allows parsers to be consistent 

* **Autonomic Bot System**
  * Job-runner to run app.py
  * Web server to handle request/response

* **Monitor Management**
  * SMS tree management flow
  * FE for direct management
  * Users will need a way to update their search_parameters, and maybe set up new, separate monitors
    * The whole app is a monitor/bot, of sorts

* **Authentication stuff**
  * Get_X_Instance generator
    * Should be able to provide an instance for whatever
    * Could either make it a method of the respective class (SearchResult/reddit; Message/twilio) so when the class is instantiated, it auths itself; or abstract as a general utility that accepts a parameter
  * Refresh auth
    * Need a way to check and refresh auth for various classes

* **Test data**
  * Something to not have to compare and rebuild the library
    * Need to store data a different states so I can load in at different points in the flow


* **Error Handling**
  * Tech debt: ooooweeee you've got some error handling to implement


## Done!

* Search flow:
    * on main page, see a table with the most recently used search
    * pull from config database and get the most recently used search :white-check-mark:
    * populate the variables below with the query from the db :white-check-mark:
    * search :white-check-mark:
    * evaluate if search is different, if so store it :white-check-mark:
    * pick from a list of previously used searches :white-check-mark:

* Make the twilio thing look at the queue and send anything that has a 0 status

* Update Search to clean up if nothing in the child table

* Add jobrunner (flask-apscheduler) to re-run reddit -> twilio pipeline

* Update response handling to use database

* Added multiple models 
  * Retooled server to use application.py to support multiple models
  * Added blueprints.py 
  * These helped a lot:
    * https://www.youtube.com/watch?v=WhwU1-DLeVw
    * https://github.com/PrettyPrinted/youtube_video_code/tree/master/2022/02/02/How%20to%20Use%20Flask-SQLAlchemy%20With%20Flask%20Blueprints/sqlalchemy_blueprint/myproject/
    * https://github.com/svieira/Budget-Manager/

* Search2 is the new Search
  * Refactor for db usage:
    * pure_search
    * eval_refactor
    * generate_results

* Got rid of Twilio and integrated it to the MessageModel
  * Might want to further abstract Twilio to a messaging provider or something but meh

* ALL THE DB WRITE LOGIC
  * Only write the dbo.Message if unique
  * Only write to dbo.SearchResultDb if unique
  * 

* **File/data mgmt stuff**
  * Replace files with Mongo DB? 
  * Update in-memory copy to
    * be smaller - only what's needed
    * Dump after storing to classes etc
    * Update only after a change is found
  * Twilio.json? For managing/updating basic Twilio information I want on hand (like phone_sid)