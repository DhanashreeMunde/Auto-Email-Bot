from flask import Flask, request, jsonify, json, Response, abort, Blueprint
from flask_cors import CORS, cross_origin
from emailing_system.models import Users, Events, EmailTemplates, EmailTracker, Logs
from emailing_system.email_bot import send_event_emails_2_employees
import logging 

email_system_blueprints = Blueprint('email_system_blueprints', __name__)

@email_system_blueprints.route('/liveness', methods=['GET', 'POST'])
@cross_origin()
def healthx():
    responseMessage = {"status": "success", "data": None, "message": "I am alive", "code":"200"}
    responseMessage = json.dumps(responseMessage)
    return Response(response=responseMessage, status=200, mimetype='application/json')

@email_system_blueprints.route('/data/<table_name>', methods=['GET'])
@cross_origin()
def get_data_from_tables(table_name):
    logging.info('Retrieving data from table {}'.format(table_name))
    try:
        if table_name == "users":
            results = Users.query.all()
            results = [[user.employee_id, user.employee_name, user.email] for user in results]

        elif table_name == "events":
            results = Events.query.all()
            results = [[event.employee_id, event.event_type, event.date] for event in results]

        elif table_name == "email_templates":
            results = EmailTemplates.query.all()
            results = [[template.event_type, template.email_template] for template in results]

        elif table_name == "email_tracker":
            results = EmailTracker.query.all()
            results = [[email.created_at, email.employee_id, email.event_type, email.email_content, email.status, email.description] for email in results]

        elif table_name == "logs":
            results = Logs.query.all()
            results = [[log.created_at, log.log_type, log.log_text] for log in results]
        else:
            results = []
    except Exception as e:
        logging.error("Error retreiving information from table {} - ".format(table_name) + str(e))
    # for row in results:
    #     print(row.__dict__)
    responseMessage = {"status": "success", "data": results, "message": "Data from {} table".format(table_name), "code":"200"}
    responseMessage = json.dumps(responseMessage)
    return Response(response=responseMessage, status=200, mimetype='application/json')

@email_system_blueprints.route('/poke', methods=['GET', 'POST'])
@cross_origin()
def trigger_email_bot():
    flag = send_event_emails_2_employees()
    responseMessage = {"status": "success", "data": None, "message": "Email service triggered", "code":"200"}
    responseMessage = json.dumps(responseMessage)
    return Response(response=responseMessage, status=200, mimetype='application/json')
