![Logo](salt-and-paper-logo.png)

# Salt and Paper: Software Architecture Capstone Project Report

## Demonstration

[Demo](http://saltandpaper-lb-1821943437.us-east-1.elb.amazonaws.com/api/v1/home)

## Abstract

Introducing Salt & Paper, an innovative application designed to create a global community for cooking enthusiasts. This platform not only provides a space for users to post, save, search, and share recipes, but also encourages engagement, discovery, and culinary creativity. With a robust architecture that ensures scalability and availability, Salt & Paper is geared to handle a large userbase, providing a seamless experience for users regardless of peak usage times.

The platform features an inclusive browser version that allows users to utilize the application with ease. The inclusion of both authenticated and guest user modes ensures the application caters to the needs of users at different engagement levels. Users can effortlessly search for recipes using either keywords or tags, allowing for a wide array of results tailored to their specific requirements.

Additionally, Salt & Paper offers a feature to create and edit recipes, complete with title, description, images, and tags, thereby nurturing the users' creativity. With visibility settings that can be toggled between 'public' and 'only me,' users can have full control over their shared content.

Moreover, the application includes a personalized cookbook feature for users to save their favorite recipes, fostering a custom and organized recipe collection. With the integration of a personal recipe recommendation system, the application can suggest recipes based on user's preferences, creating an intuitive and personalized culinary journey.

In the spirit of continual improvement, Salt & Paper is able to receive regular updates introducing new features, thus extending its functionality to better serve its users. By connecting cooking lovers worldwide and fostering a dynamic space for recipe sharing and discovery, Salt & Paper aims to stir up a culinary revolution.

## Changes

Several features have been excluded as they are not considered essential to the main features of the application. These features include the option to add images in recipe posts, the visibility settings for the recipe posts, and the personalised recommendation system.

From an architecture perspective, we initially decided to design the application using microservices for each of the collection of endpoints, such as recipe endpoints, cookbook endpoints, among others. This was to improve its scalability and extensibility. However, due to the high amount of communication needed between services, this approach did not seem suitable as it would make the application complex, while not necessarily making the database operations faster, and since the application is still in its early stages and do not have a large user base yet, this approach is not needed yet.

## Architecture

### Context

<div align="center">
  <img src="../model/adrs/Context label.PNG" alt="Salt and Paper Context Diagram" width="800"/>
</div>

<div align="center">
  <img src="../model/adrs/Context1.PNG" alt="Salt and Paper Context Diagram" width="800"/>
</div>

### Container

<div align="center">
  <img src="../model/adrs/Container legend.PNG" alt="Salt and Paper Container Diagram" width="800"/>
</div>

<div align="center">
  <img src="../model/adrs/container1.PNG" alt="Salt and Paper Container Diagram" width="800"/>
</div>

<div align="center">
  <img src="../model/adrs/Container2.PNG" alt="Salt and Paper Container Diagram" width="800"/>
</div>

### Dynamic

<div align="center">
  <img src="../model/adrs/dynamic diagram.PNG" alt="Salt and Paper Container Diagram" width="800"/>
</div>

The Minimum Viable Product (MVP) showcases a tantalizing software architecture, composed of components:

1. Frontend:

   - User Interface (UI): Crafted with cutting-edge React frameworks, the UI tantalizes users' visual senses, providing a seamless and visually pleasing experience.
   - Views and Components: We incorporated pictures icons, and other elements to make it easier to navigate through the app. The UI is designed to be responsive, ensuring a consistent experience across devices.

2. Backend:

   - Server: We used Python Flask to serve the API endpoints. The server is responsible for handling the requests and responses between the frontend and the database. Orchestrates the flow of requests, serving multiple API endpoints of data to the frontend. Some of the endpoints are enforced with protected routes middleware to ensure the authentication and authorization of the users.
   - Database: We used PostgreSQL for its robustness. The database stores users' profiles, recipes, Cookbook and Ratings. Its design ensures data integrity and efficient recipe retrieval. We used the Sequelize ORM to facilitate the interaction with the database.

3. API:
   - Endpoints: The endpoints are designed to be RESTful and follow the best practices of RESTful API design. The endpoints are enforced with authentication and authorization to ensure the security of the data.
   - RESTful API: The API endpoints are designed to be intuitive and easy to use.

## Trade-Offs

- Performance vs. Extensibility: By optimizing certain components, we've achieved a adequate performance. However, to ensure a better user experience, we traded a slight reduction in extensibility. For the core architecture still welcomes future enhancements.

- Simplicity vs. Customization: Our UI design focuses on simplicity and elegance. While customization options are limited, this approach ensures that users a consistent and intuitive interface.
- accuracy of search task are traded for efficiency and availability the search task.
  Use global variables to stored documents which would expire in 5 minutes to respond to the search request.
  Only return 5 most related documents,just like the first page of google search result.

## Critique

### Security

- User registration credentials are protected using strong Password Hash.

The user registration credentials that the user adds as input in our application when signing up or logging in are protected using a strong password hash mechanism. This ensures that the hash values cannot be decrypted, which means that there is an additional layer of protection against unauthorised access. This aligns with the Defense in Depth Principle.

- Request Forgery prevention using CSRF tokens [3]

CSRF attacks involve a malicious user performing actions using another user's credentials without that user's knowledge or consent. Adding this layer of protection in our application aligns with the Principle of Least Privilege because we're ensuring that only authorised and authenticated users can submit forms or perform any action on the application, preventing theses CSRF attacks.

These are some of the mechanisms we have not implemented that should be implemented to improve the security of the application.

- Add SSL HTTPS certificate (Principle of Least Privilege)
- Use reverse proxy (Defense in Depth)

### Scalability

- Horizontal Scaling using Async Task Queue using Celery.

We have implemented an asynchronous task queue for the searching endpoints using Celery. This helps with scalability because the system will be able to handle an increase in search requests without causing performance bottlenecks.

One way to improve this is to implement the asynchronous task queue for other heavy endpoints as well, for instance the creating recipe endpoint.

## Evaluation

### Test Images

<div align="center">
  <img src="../model/tests/number_of_users_1685937873.png" alt="Salt and Paper test Diagram" width="800"/>
</div>

<div align="center">
  <img src="../model/tests/total_requests_per_second_1685937873.png" alt="Salt and Paper test Diagram" width="800"/>
</div>

### Scalability and Availability

For these attributes, we have performed a load test for 2000 users using Locust whilst simultaneously checking that the tests returned successful status codes (to check availability as well).

Based on the test, the application was able to handle the increase number of users, but unfortunately in terms of availability, the requests weren’t able to run 100% of the time, with multiple failures.

It is important to note though that we ran tests on an earlier version of the system which did not include the authentication system, as that was delivered quite late.

### Extensibility

The architecture separates endpoints based on their usage. For instance, endpoints relating to authentication, recipes, cookbooks, and search are put in separate view files. This ensures that if we were to add a new feature, we would not have to modify a lot of the existing code and can simply add to the codebase. However, one way this could be improved is to make the application microserviced, as this would ease the process of adding features even more.

## Reflection

- Improved Requirements Gathering: We've learned that requirements gathering is a continuous process. We've improved our requirements gathering process by incorporating feedback from each iteration.

- Embrace Iterative Development: By adopting an iterative development approach, such as Agile or Scrum, we can utilize frequent feedback loops. This will ensure that the software is developed to meet the needs of the users.

- Continuous Integration and Deployment: Automating with robust CI/CD pipelines will ensure a seamless development process. This will allow us to focus on the development of the software, while the CI/CD pipelines take care of the rest.

## Reflection

- Improved Requirements Gathering: We've learned that requirements gathering is a continuous process. We've improved our requirements gathering process by incorporating feedback from each iteration.

- Embrace Iterative Development: By adopting an iterative development approach, such as Agile or Scrum, we can utilize frequent feedback loops. This will ensure that the software is developed to meet the needs of the users.

- Continuous Integration and Deployment: Automating with robust CI/CD pipelines will ensure a seamless development process. This will allow us to focus on the development of the software, while the CI/CD pipelines take care of the rest.

---
