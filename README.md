# Cinemazing Movie Website

Cinemazing is a dynamic movie website that allows users to explore, search, and interact with a wide range of movies. The website is built using Flask and MySQL, and it offers a user-friendly interface for movie enthusiasts to discover and engage with their favorite films.

## Features

### Movie Listing and Pagination

- The website showcases a comprehensive list of movies across various genres.
- Movies are presented in a visually appealing format, with details such as title, year, IMDB score, and poster image.
- Pagination is implemented to ensure smooth navigation through multiple pages of movie listings.

### Search Functionality

- Users can easily search for movies by entering keywords.
- The search results dynamically update as users type, providing real-time feedback.

### Movie Details

- Clicking on a movie's title or poster leads to a detailed movie page.
- Movie pages display essential information, including the title, year, category, IMDB score, and a trailer video.
- Users can read and contribute to movie-related comments and discussions.

### User Registration and Authentication

- New users can register on the website by providing their name, username, email, gender, age, and password.
- Passwords are securely encrypted before being stored in the database.
- Registered users can log in using their credentials, gaining access to personalized features.

### Flash Messages

- Bootstrap is used to display flash messages for user feedback and notifications.
- Messages are shown for actions such as successful login, registration, and more.

### Form Validation

- User input is validated using WTForms to ensure accurate and secure data entry.
- Error messages are displayed if users provide incorrect or incomplete information.

### User Authentication and Authorization

- Certain website sections, such as adding comments, are restricted to logged-in users.
- The `login_required` decorator is used to enforce access control.


## Technology Stack

- **Backend**: Flask, MySQL, Python
- **Frontend**: HTML, CSS, Bootstrap (All user interface designs have been customized using CSS. Bootstrap is only used to display flash messages.)
- **Database Management**: phpMyAdmin
- **Form Handling**: WTForms
- **Authentication**: Flask-Login
- **Pagination**: Flask-Paginate


