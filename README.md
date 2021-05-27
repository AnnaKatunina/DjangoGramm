# DjangoGramm project

This application is a web service with web interface for posting, sharing and viewing pictures of other users.

This app has the following features:

- after registration users are redirected to the profile page and can add their full name, bio, avatar
- users can register and login via third-party services (GitHub, Google)
- users can subscribe or unsubscribe to other users (ajax functionality)
- users can post their images (for storing images added cloudinary functionality)
- the main page is a feed of images posted by the users he/she follows and the user's images in reverse chronological order
- users can like or unlike other users images (ajax functionality)


The application has been covered by unittests.

The application has been deployed to Heroku
https://djangogramm-project.herokuapp.com/

____
## Requirements

- Python 3.7+
- Django 3.1

## Installing

1\. Clone the repository
```
git clone https://github.com/AnnaKatunina/DjangoGramm.git
```
2\. Create and activate virtualenv
- for Linux/macOS
```
python -m venv venv
source venv/bin/activate
```
- for Windows
```
python -m venv venv
venv\Scripts\activate
```
3\. Install packages from requirements.txt
```
pip install -r requirements.txt
```
## Usage

Run the application
```
python manage.py runserver
```