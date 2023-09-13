#Savannah Informatics Technical Assessment Test

#To run and test locally.
1.  Use virtualenv to create a local environment.

2. create a virtual environment: python -m venv env.

3. Activate the environment: source env/scripts/activate

4. Install the requirements: pip install requirements.txt -r

5. Run the unit tests with coverage: ./manage.py test --cover-package=customer,order.

6. Run the project locally: python manage.py runserver and Browse to [http://localhost:8080](http://localhost:8080/)

#For Deployment