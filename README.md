#Savannah Informatics Technical Assessment Test

The project uses Django framework with Django REST framework.

#To run and test locally.
1.  Use virtualenv to create a local environment.

2. create a virtual environment: python -m venv env.

3. Activate the environment: source env/scripts/activate

4. Install the requirements: pip install requirements.txt -r

5. Run the unit tests with coverage: ./manage.py test --cover-package=customer,order.

6. Go to https://developers.africastalking.com/simulator, initiate the simulator with your desired phone  number for testing and generate a SandBox ApiKey for testing purposes. Replace These on the settings.py file.

7. Run the project locally: cd to the project folder and run `python manage.py runserver` or run with `docker-compose up` command. and Browse to [http://localhost:8080](http://localhost:8080/).

#For Deployment
The Project uses Githubs work flows for CI/CD and deploys to Azure service web app. One reqires to set up an Azure Web App and add the necessary authorization credentials to push the docker image after creation. More details are contained in the azure-container-webapp.yml comments.

A postgress DB instance will be created on Azure as well.
