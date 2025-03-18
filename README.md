
# About the Student Profile Management System
- The system stores student profile and students' activity attendances.

## Functionalities
- Visualizing score based on attendances. 
- Activity arrangement requests.
- Curriculum-based OKR visualization (CS, IT have their own preferences). 
- The API and UI are designed to serve both Staff and Student. The permission works at the field level (e.g. Student cannot edit some fields).
- Basic file permission based on Role (Staff and Student).
- Bulk adding attendances.

## To-do
- Tweak UI.
- Detailed documentation. 
- Deploy to the server. (Lots of things to do, e.g., set DEBUG = FALSE, Regenerate api key, securities, ...)
    
# Note🔥 
- This project is *not* meant to be used in production. It's the exploration of the capabilities of Django. 


# Tools

## Backend 

- [Django](https://github.com/django/django)
  - All basic functionalities are included. You can move ridiculously fast!
- [Django Rest Framework](https://github.com/encode/django-rest-framework)
  - Api design simplified. Serializers do tons of jobs for you. What a lovely tool. 
- [nginx](https://github.com/nginx/nginx)
  - Used to route requests to Frontend and Backend servers.
- [PostgreSQL](https://github.com/postgres/postgres)
  - When the tool is great, everything just works. 
- [Docker](https://github.com/docker)
  - Used to run PostgreSQL.


## Frontend
- [Vue.js](https://github.com/vuejs) 
   - This tool is amazing!! (This was my first JavaScript framework). Love it.
- [Vite](https://vitejs.dev/)
   - This is the frontend server.
    

# Testing
    
- No external tools needed, Django and Vite provide internal testing frameworks.

1. Api Testing
   - You don't need Postman for Api Testing. Django provides a great testing framework.
2. Frontend Testing
   - [Vitest](https://github.com/vitest-dev/vitest) is provided with vite!
