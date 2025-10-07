# CS4300
The Coursework for CS4300 Fall 2025

How to run locally
1. Create and activate a virtual environment (Unix example):

   python -m venv .venv; ./.venv/Scripts/activate

2. Install dependencies:

   pip install django djangorestframework

3. Run migrations and start the server:

   python manage.py migrate; python manage.py runserver

4. If necessary add your enviroment to the Allowed_Hosts setting in movie_theater_booking/setting.py 

5. Run tests:

   python manage.py test

AI Usage
In my original code I attempted to integrate a user login system that required
user authentication to access booking capabilities. After failing multiple times
and then learning that we didn't actually need user logins I began to remove these.
This ended up becoming a herculean task of epic proportions of me trying to fix
my code already entangled with all this junk that I eventually threw it into copilot to 
try and get me out. I thouroughly used AI to assist me in restructuring my views.py,
formatting my urls for both, and creating a broad arrangement of test cases.
I also used it to create the little local walkthrough above.
I mainly used copilot so I could see how messed up parts of the code were and
emulate fixing the problems. ChatGPT was used to ask questions on how
certain things were used.

There is no way to remove a booking once someone has selected it
this company has a enforced no refund policy. We won't do it
even if it kills us.