import os
from forms.SearchForm import SearchForm
from models.SearchParameters import get_parameters, add_parameters
from runmain import runmain, clean_up_db, send_test_text
from application import create_app
from flask import request, render_template
from flask_ngrok import run_with_ngrok
from twilio.twiml.messaging_response import MessagingResponse
from models.MessageModel import handle_incoming_message
from dotenv import load_dotenv

# Check and set environment
is_prod = os.environ.get('IS_HEROKU', None)

if os.environ.get('IS_HEROKU', None):
    print('we are in prod') #no need to set envs
else:
    load_dotenv()

#https://www.twilio.com/blog/build-a-sms-chatbot-with-python-flask-and-twilio
app = create_app()

# Create a route that just returns "In progress"
@app.route("/", methods=['GET', 'POST'])
def serve_homepage():
    form = SearchForm()
    search_parameters = get_parameters()
    if request.method == 'GET':
        form.site.data = search_parameters.site
        form.subdomain.data = search_parameters.subdomain
        form.search_terms.data = search_parameters.search_terms
        form.limit.data = search_parameters.limit
        form.submit.label.text = 'Update'
    
    if form.validate_on_submit() and request.method == 'POST':
        print(f'SUBMIT {(form.search_terms)}')
        site = form.site.data
        subdomain = form.subdomain.data
        search_terms = form.search_terms.data
        limit = form.limit.data
        add_parameters(site, subdomain, search_terms, limit)
        
    return render_template('index.html',
        form=form,
        search_parameters=search_parameters
    )

@app.route("/manual-search", methods=['GET', 'POST']) #will loop the app.py script while on thie page
def run_main():
    form = SearchForm()
    search_parameters = get_parameters()
    if request.method == 'GET':
        form.site.data = search_parameters.site
        form.subdomain.data = search_parameters.subdomain
        form.search_terms.data = search_parameters.search_terms
        form.limit.data = search_parameters.limit
    
    if form.validate_on_submit() and request.method == 'POST':
        print(f'SUBMIT {(form.search_terms)}')
        site = form.site.data
        subdomain = form.subdomain.data
        search_terms = form.search_terms.data
        limit = form.limit.data
        search_params = add_parameters(site, subdomain, search_terms, limit)
        runmain(search_params)
        
    return render_template('manualsearch.html',
        form=form,
        search_parameters=search_parameters
    )


@app.route("/testtext")
def test_text():
    send_test_text()
    return render_template('testtext.html')

@app.route("/clean") #will loop the app.py script while on thie page
def clean():
    clean_up_db()
    return render_template('clean.html')

@app.route("/sms", methods=['POST'])
def handle_incoming_msg():
    incoming_msg = request.values.get('Body', '').lower() #store the body of the message into a variable
    # handle response from app server
    found = handle_incoming_message(incoming_msg)
    if found:
        final_body = "\n\n: \n\nConsumerBot: I will send a message on Reddit to the author of post ID, " + '"' + found['id'] + '".'
    else:
        final_body = '\n\n: \n\nConsumerBot: I did not find any posts matching post ID, ' + '"' + incoming_msg + '".' + ' It might not be saved or it was deleted.'

    resp = MessagingResponse() 
    msg = resp.message()
    msg.body(final_body)
    
    print(final_body) #somewhere in here, need to save the inbound-message?
    return str(resp)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# Start the web server when this file runs
# also run ngrok http 5000
if __name__ == "__main__":
    if os.environ.get('IS_HEROKU', None) is None:
        run_with_ngrok(app)
    app.run()