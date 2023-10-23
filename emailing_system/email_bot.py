from emailing_system.models import Users, Events, EmailTemplates, EmailTracker, Logs
from datetime import datetime, timedelta
from emailing_system.extensions import db, scheduler 
import random
import logging

def send_mail(recipient_email, sender_mail, subject, body):
    # logic to send emails using SMTP server will come here
    # for now we are assuming that email is sent successfully with a 70% probability 

    number = random.random()
    if number <= 0.7:
        status = "Delivered"
        message = "Success"
    elif number > 0.7 and number <= 0.9:
        status = "Pending"
        message = "Email delayed due to xyz reason"
    else:
        status = "Error"
        message = "Email could not be sent due to xyz reason"
    
    return status, message

@scheduler.task(
    "cron",
    id="email_service",
    hour=3,
    minute=38
)
def send_event_emails_2_employees(max_retries = 3):
    logging.info('Initiating email bot')
    if(max_retries == 0):
        return True
    current_date = datetime.now().date()
    # current_date = datetime(2023, 10, 1).date() #+ timedelta(days=random.randint(1,30))
    with scheduler.app.app_context():
        try:
            events_pending_2day = Events.query.filter(Events.date >= current_date, Events.date < current_date + timedelta(days=1)).all()
            if len(events_pending_2day) == 0:
                logging.warning('No events scheduled for today')
                log_row = Logs(datetime.now(), "INFO", "No events are scheduled for the current period")
                db.session.add(log_row)
                db.session.commit()
            else:
                logging.info('Sending emails to employees')
                for event in events_pending_2day:
                    user_details = Users.query.filter(Users.employee_id == event.employee_id).all()[0]
                    recipient_email = user_details.email 
                    recipient_name = user_details.employee_name 

                    email_template = EmailTemplates.query.filter(EmailTemplates.event_type == event.event_type)[0].email_template
                    email_subject = event.event_type 
                    email_body = email_template.replace('[Employee Name]', recipient_name).replace('[Event Date]', str(event.date))
                    
                    status, message = send_mail(recipient_email, 'email_sender.gmail.com', email_subject, email_body)
                    trial_number = max_retries - 1
                    while(status == 'Error' and trial_number > 0):
                        logging.warning('Retrying sending email to employee with employee id {}'.format(event.employee_id))
                        status, message = send_mail(recipient_email, 'email_sender.gmail.com', email_subject, email_body)
                        trial_number -= 1
                    if status == 'Error':
                        logging.warning('Email could not be sent to employee with employee id {}'.format(event.employee_id))
                    elif status == 'Pending':
                        logging.warning('Email pending for employee with employee id {}'.format(event.employee_id))

                    email_tracker_row = EmailTracker(datetime.now(), event.employee_id, event.event_type, email_content = email_body, status = status, description = message)
                    db.session.add(email_tracker_row)
                log_row = Logs(datetime.now(), "INFO", "Emails sent to employees for the current period")
                db.session.add(log_row)
                db.session.commit()
        except Exception as e:
            logging.error('Error sending emails - ' + str(e))
    return True
