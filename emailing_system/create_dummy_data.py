from emailing_system.models import Users, Events, EmailTemplates
from emailing_system.extensions import db
import logging 

events_table = [
    (1, "Meeting with the Manager", "2023-10-05"),
    (2, "Team Building Workshop", "2023-10-15"),
    (3, "Training Session on New Software", "2023-10-20"),
    (4, "Company Picnic", "2023-10-30"),
    (1, "Presentation to Clients", "2023-10-18"),
    (2, "Monthly Review Meeting", "2023-10-30"),
    (3, "Employee of the Month Celebration", "2023-10-10"),
    (4, "Project Kick-off Meeting", "2023-10-10"),
    (5, "Birthday Party for Employee 5", "2023-10-12"),
    (6, "Quarterly Sales Review", "2023-10-25"),
    (7, "Lunch with New Hires", "2023-10-10"),
    (8, "Work Anniversary Celebration", "2023-10-05"),
    (5, "Presentation to Stakeholders", "2023-10-01"),
    (6, "Product Launch Event", "2023-10-17"),
    (7, "Team Bonding Activity", "2023-10-15"),
    (8, "Holiday Office Party", "2023-10-20"),
    (9, "Birthday Party for Employee 9", "2023-10-05"),
    (10, "Quarterly Budget Meeting", "2023-10-30"),
    (11, "Training Workshop on Communication Skills", "2023-10-22"),
    (12, "Employee Recognition Awards Ceremony", "2023-10-12"),
    (9, "Client Presentation and Dinner", "2023-10-14"),
    (10, "Team Building Retreat", "2023-10-03"),
    (11, "Employee's Birthday Celebration", "2023-10-02"),
    (12, "Quarterly Sales Kick-off", "2023-10-02"),
    (13, "Holiday Office Potluck", "2023-10-24"),
    (14, "Team Building Exercise", "2023-10-18"),
    (15, "Product Development Workshop", "2023-10-10"),
    (16, "Birthday Party for Employee 16", "2023-10-08"),
    (13, "Monthly Performance Review", "2023-10-28"),
    (14, "Company Town Hall Meeting", "2023-10-17"),
    (15, "Employee's Birthday Celebration", "2023-10-10"),
    (16, "Quarterly Planning Meeting", "2023-10-05"),
    (17, "Holiday Office Party", "2023-10-19"),
    (18, "Training Workshop on Leadership", "2023-10-15"),
    (19, "Birthday Party for Employee 19", "2023-10-20"),
    (20, "Team Building Retreat", "2023-10-08"),
    (17, "Product Launch Event", "2023-10-12"),
    (18, "Employee's Birthday Celebration", "2023-10-28"),
    (19, "Quarterly Sales Review", "2023-10-21"),
    (20, "Holiday Office Potluck", "2023-10-31"),
    (21, "Meeting with the Manager", "2023-10-05"),
    (22, "Team Building Workshop", "2023-10-15"),
    (23, "Training Session on New Software", "2023-10-20"),
    (24, "Company Picnic", "2023-10-30"),
    (21, "Quarterly Budget Meeting", "2023-10-30"),
    (22, "Team Bonding Activity", "2023-10-18"),
    (23, "Work Anniversary Celebration", "2023-10-05"),
    (24, "Birthday Party for Employee 24", "2023-10-09"),
]

event_templates = [
    ("Meeting with the Manager", "Hello [Employee Name],\n\nYou have a meeting scheduled with the manager on [Event Date]. Please come prepared and on time. Thank you."),
    ("Team Building Workshop", "Dear [Employee Name],\n\nWe have a team-building workshop coming up on [Event Date]. Get ready for some exciting activities and team bonding!"),
    ("Training Session on New Software", "Hi [Employee Name],\n\nA training session on the new software is scheduled for [Event Date]. Be sure to bring your laptop and questions."),
    ("Company Picnic", "Hello [Employee Name],\n\nIt's time for our annual company picnic on [Event Date]. Get ready for some outdoor fun and great food."),
    ("Presentation to Clients", "Dear [Employee Name],\n\nYou are part of the presentation to our clients on [Event Date]. Your input is highly valuable."),
    ("Monthly Review Meeting", "Hi [Employee Name],\n\nOur monthly review meeting is scheduled for [Event Date]. Please prepare your reports and updates."),
    ("Employee of the Month Celebration", "Hello [Employee Name],\n\nJoin us in celebrating the Employee of the Month on [Event Date]."),
    ("Project Kick-off Meeting", "Hi [Employee Name],\n\nWe have an important project kick-off meeting on [Event Date]. Be prepared to discuss the project details."),
    ("Birthday Party for Employee 5", "Dear [Employee Name],\n\nWe are celebrating Employee 5's birthday on [Event Date]. Join us for cake and fun!"),
    ("Quarterly Sales Review", "Hello [Employee Name],\n\nThe quarterly sales review is on [Event Date]. Be prepared to discuss your achievements and targets."),
    ("Lunch with New Hires", "Hi [Employee Name],\n\nLet's welcome the new hires with a special lunch on [Event Date]. Your presence will be appreciated."),
    ("Work Anniversary Celebration", "Dear [Employee Name],\n\nWe're celebrating your work anniversary on [Event Date]. Join us for a special celebration."),
    ("Presentation to Stakeholders", "Hello [Employee Name],\n\nYou will be presenting to stakeholders on [Event Date]. Please review your presentation and be ready."),
    ("Product Launch Event", "Hi [Employee Name],\n\nWe have an exciting product launch event on [Event Date]. Get ready for a memorable event."),
    ("Team Bonding Activity", "Dear [Employee Name],\n\nJoin us for a team bonding activity on [Event Date]. It's going to be a fun day!"),
    ("Holiday Office Party", "Hello [Employee Name],\n\nGet ready to celebrate the holiday season at our office party on [Event Date]."),
    ("Birthday Party for Employee 9", "Hi [Employee Name],\n\nWe're celebrating Employee 9's birthday on [Event Date]. Join us for the festivities!"),
    ("Client Presentation and Dinner", "Dear [Employee Name],\n\nYou have a client presentation followed by dinner on [Event Date]. Make a great impression!"),
    ("Team Building Retreat", "Hello [Employee Name],\n\nOur team building retreat is scheduled for [Event Date]. It's a great opportunity to build strong relationships."),
    ("Employee's Birthday Celebration", "Hi [Employee Name],\n\nWe're celebrating your birthday on [Event Date]. Join us for a special celebration."),
    ("Quarterly Planning Meeting", "Dear [Employee Name],\n\nThe quarterly planning meeting is on [Event Date]. Be prepared to discuss our goals and strategies."),
    ("Holiday Office Potluck", "Hello [Employee Name],\n\nJoin us for a holiday office potluck on [Event Date]. Please bring a dish to share."),
    ("Training Workshop on Communication Skills", "Hi [Employee Name],\n\nA training workshop on communication skills is scheduled for [Event Date]. Be prepared to improve your skills."),
    ("Employee Recognition Awards Ceremony", "Dear [Employee Name],\n\nThe Employee Recognition Awards Ceremony is on [Event Date]. Your achievements will be celebrated."),
    ("Monthly Performance Review", "Hello [Employee Name],\n\nIt's time for the monthly performance review on [Event Date]. Please have your performance data ready."),
    ("Company Town Hall Meeting", "Hi [Employee Name],\n\nJoin us for the company town hall meeting on [Event Date]. Stay informed and share your ideas."),
    ("Product Development Workshop", "Dear [Employee Name],\n\nA product development workshop is scheduled for [Event Date]. Your input is crucial for our product development."),
    ("Birthday Party for Employee 16", "Hello [Employee Name],\n\nWe're celebrating Employee 16's birthday on [Event Date]. Join us for cake and festivities!"),
]

user_information = [
    (1, "Clark Kent", "clark.kent@example.com"),
    (2, "Diana Prince", "diana.prince@example.com"),
    (3, "Barry Allen", "barry.allen@example.com"),
    (4, "Bruce Wayne", "bruce.wayne@example.com"),
    (5, "Hal Jordan", "hal.jordan@example.com"),
    (6, "Arthur Curry", "arthur.curry@example.com"),
    (7, "Victor Stone", "victor.stone@example.com"),
    (8, "Lois Lane", "lois.lane@example.com"),
    (9, "Selina Kyle", "selina.kyle@example.com"),
    (10, "J'onn J'onzz", "jonn.jonzz@example.com"),
    (11, "Barbara Gordon", "barbara.gordon@example.com"),
    (12, "Harvey Dent", "harvey.dent@example.com"),
    (13, "Oliver Queen", "oliver.queen@example.com"),
    (14, "Lana Lang", "lana.lang@example.com"),
    (15, "Jimmy Olsen", "jimmy.olsen@example.com"),
    (16, "Zatanna Zatara", "zatanna.zatara@example.com"),
    (17, "Shayera Hol", "shayera.hol@example.com"),
    (18, "Wally West", "wally.west@example.com"),
    (19, "John Constantine", "john.constantine@example.com"),
    (20, "Hawkgirl", "hawkgirl@example.com"),
]

def create_tables(app):
    logging.info("Creating dummy database for development purposes")
    with app.app_context():
        for event in events_table:
            event_row = Events(event[0], event[1], event[2])
            db.session.add(event_row)

        for user in user_information:
            user_row = Users(user[0], user[1], user[2])
            db.session.add(user_row)
        
        for template in event_templates:
            template_row = EmailTemplates(template[0], template[1])
            db.session.add(template_row)

        db.session.commit()