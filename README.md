# AddressBookAppBE

## Table of Content
- [AddressBookAppBE](#addressbookappbe)
  - [Table of Content](#table-of-content)
  - [Overview](#overview)
  - [Live Demo](#live-demo)
  - [Tech Stack](#tech-stack)
  - [Getting Started](#getting-started)
  - [FE Detail Documentation](#fe-detail-documentation)
    - [Env Config](#env-config)
    - [Backend For Frontend (BFF)](#backend-for-frontend-bff)
    - [The Structure of the code](#the-structure-of-the-code)
    - [RTK Query](#rtk-query)
    - [Endpoits Mapping](#endpoits-mapping)
  - [BE Detail Documentation](#be-detail-documentation)
    - [Database](#database)
    - [Authentication in Address Book App](#authentication-in-address-book-app)
      - [Authentication Flow](#authentication-flow)
      - [Configuration](#configuration)
    - [Custom Search](#custom-search)
    - [The Structure of the code](#the-structure-of-the-code-1)
    - [Endpoits Mapping](#endpoits-mapping-1)
  - [Solution Diagram](#solution-diagram)
    - [Application](#application)
    - [Components](#components)

## Overview

I developed an Address Book App that allows users to search for contacts and save them to their favorites list, linked to their account. The app is a full-stack solution built using NextJS, SASS, and RTK on the front-end and Python and Django on the back-end. 

Users can create an account or log in to an existing one to search for contacts and filter the results based on nationality and/or gender. The search filter works without refreshing the page. Users can view contact details and add them to their favorites list, which is saved in the database so that users can keep their list. 

The app supports internationalization, allowing users to switch between Portuguese and English. To ensure security, I built a request handler on the SSR (BFF) to work as a middleware between our app and service, which allows us to hide and protect our internal services (API Gateway / BE). 

The back-end acts as an API Gateway, responsible for handling different services and authorization. It includes an Auth endpoint that handles interaction with Auth0 for login and signup, a Search endpoint that requests data from randomuser.me, and a User endpoint that handles account favorites and adding or removing contacts from the database. I used PostgreSQL for the deployed version and SQlite for a test environment. 

The complete application is deployed in a production environment. For the front-end, I used Vercel to deploy the app every time a new PR is merged in the master branch, while for the back-end, I used my own server to deploy together with GitHub Action. For PostgreSQL, I'm using the Vercel Storage service.

## Live Demo

FE App:
https://address-app.brunopereira.dev/

http://address-service.brunopereira.dev/

Try it ;)

## Tech Stack
FE:
- Next.js with app router [docs](https://nextjs.org/docs)
- React [docs](https://react.dev/)
- Redux [docs](https://redux.js.org/)
- RTK Queries [docs](https://redux-toolkit.js.org/introduction/getting-started)
- Typescript
- SASS
- i18n

BE:
- Python
- Django
- Auth0
- PostgreSQL

## Getting Started

To get started with Address Book App Project, follow these steps:

1. **Clone the Repository**: Clone the project repository from our GitHub repository

Inside of your FE Project Folder:

1. **Install Dependencies**: Run `npm install` to install the necessary dependencies.

2. **Configuration**: Make sure you have the `.env` file in you FE root project folder.

3. **Start the Development Server**: Run `npm run dev` to start the development server.

4. **Build the Project**: Run `npm run build` to start the development server.

5. **Run test coverage**: Run `npm run test:coverage` to start the development server.

6. **Explore**: You can visit the app on [localhost:3000](http://localhost:3000)

Inside of your BE Project Folder:

1. **Install Dependencies**: Run `pip install -r requirements.txt` to install the necessary dependencies.

2. **Configuration**: Make sure you have the `.env` file in you BE root project folder.

3. **Start the Development Server**: Run `DJANGO_TESTING=False python3 manage.py runserver 8000` to start the development server.

4. **Run test coverage**: Run `DJANGO_TESTING=True pytest --cov=.` to start the development server.

5. **Explore**: You can use POSTMAN to request data at [localhost:8000](http://localhost:8000)

## FE Detail Documentation

### Env Config

To configure you need to add the following variable in your `.env` file

```
NEXT_PUBLIC_SERVICE_API_URL=http://127.0.0.1:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_APP_ENVIRONMENT=staging
NEXT_PUBLIC_ENABLE_REDUX_DEV_TOOLS=true
```

### Backend For Frontend (BFF)

I'm using the Next.js [route handler](https://nextjs.org/docs/app/building-your-application/routing/route-handlers) to create a BFF as a middleman to call our backend APIs. The reasons is to protect our internal services and increase the security of it. With the BFF layer I can force authorization params and avoiding [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).

### The Structure of the code

1. **Components**: Different types of components together form a page.
    * The `page` component is responsible for rendering the page. This type of component is basically a wrapper for multiple components.
    * The `container` is responsible for all the interactions with the store and passes the data to the `component`
    * The `component` is responsible for all the component logic and rendering of the UI elements.


   1. **Components File Structure**:
      ```
        └── Example
          ├── component.tsx
          ├── component.module.scss
          ├── component.test.tsx
          ├── container.tsx
          ├── container.module.scss
          └── index.ts
      ```
      The container handles the state and the store access. The component is then left to render, depending only on the props provided by the container. Any logic that is triggered from the component, e.g., a callback on a button click, is defined in the container.

2. **Hooks**: I use hooks to encapsulate logic and data transformation, making our components thinner and easier to work with.
3. **Store**: I use the store folder containing the RKT configuration.
   1. **Slices**: Each component should provide its own slice to interact with the Redux store
   2. **Services**: The only service we have for each component now is the RTK Query API
4. **Types**: This is the directory for each module's model information.
5. **Providers**: This is the directory that keeps the providers of our app.
6. **Layouts**: This is the directory to keep the root layout to be shared between all project pages.
7. **Styles**: This folder contains the global style configurations.
8. **Translations**: This is the directory keeping translation key files.
9. **Utils**: This directory contains all the shared functions of the project
10. **Configs**: This directory contains all the shared configurations of the project.
11. **i18n**: This directory contains the configuration for the translations of the project
12. **App**: This directory defines the project's routing. Each folder inside of it represents a page on the app.
    1. **API**: This directory is used as our BFF handler. Each folder inside of it represents an endpoint on the server side.

### RTK Query

In order to simplify API queries, a better alternative to [React Query](https://tanstack.com/query/v3/), i.e. [RTK Query](https://redux-toolkit.js.org/rtk-query/overview) is being used to send async API queries to the backend APIs using Redux Thunks. It stores the data and the cache keys in Redux stores.

### Endpoits Mapping

Unprotected Route:
`{base-url}/login`: Allow  the user to login with email and password.
`{base-url}/signup`: Allow the user to create an account into the app.

Protected Route:
`{base-url}/`: Allow the user to search contacts with or without filters. And add them to the favorites.
`{base-url}/favorites`: Allow the user to check the list of favorite contacts
`{base-url}/settings`: Allow the user to add or manage filters to be used on the search element.

## BE Detail Documentation

### Database

I'm using PostgreSQL database from Vercel to keep the favourites from user's accounts.

To configure you need to add the following variable in your `.env` file

```env
DB_NAME=verceldb
DB_USER=default
DB_PASSWORD=w7DXqgLjsG9S
DB_HOST=ep-steep-darkness-43137634-pooler.eu-central-1.postgres.vercel-storage.com
DB_PORT=5432
```


### Authentication in Address Book App

#### Authentication Flow

For authentication and authorization in Address Book App, we utilize Auth0 as the OAuth provider.

#### Configuration

To configure authentication for Address Book App, define the required environment variables for your Auth0 configuration. 
  These should include the Auth0 domain and client ID.
```env
AUTH0_CLIENT_ID=N3A5YSuGsIww3EXRiVzRoZpYtR55LCL2
AUTH0_CLIENT_SECRET=UjBThP-l0x2Dq41PU_CGQ8LjKcKSzKpREfAfo4dPOX87mAH5UOQRyOB_MTytCsFX
AUTH0_DOMAIN=dev-aadsufcp8tmz0ufm.eu.auth0.com
```

This configuration will be used for all interactions with Auth0, to handle authentication for our service. The access token will be passed to the frontend app, allowing the BFF to add it to the header of all requests for private service endpoints. The API Gateway will validate the token provided on the request with Auth0 to ensure its validity.

### Custom Search 

I have created a solution to search for users by name since the randomuser.me service does not provide a customizable search functionality. To ensure data consistency and meet the requirements of the test, I have used the seed parameter provided by the API to always receive the same list of data with a limit of 50 users per page and a maximum of 20 pages, resulting in 1000 contacts per catalog.

Whenever a search is performed, with or without filters, such as name, nationality, or gender, the service will go through the external API page by page until a batch of 50 contacts is created or the page limit is reached. Once either of these conditions is met, the response will be returned for application.

To prevent the API from blocking our service due to too many requests and to improve the application's performance, I have implemented caching in the lists. The cache is used to feed the application in future user interactions, making it faster in service response. The cache is maintained for one hour, ensuring data refreshes every hour, even if it is a fixed list.

### The Structure of the code

1. **middleware**: Responsable for handling with the authorization of the requests made to the API.
2. **view**:
   1. **auth_views**: Responsable to handle with the authtication with Auth0
   2. **user_views**: Responsable to handle with the app operations

### Endpoits Mapping

Unprotected Route:
`{base-url}/auth/login`: Handle with the user login flow.
`{base-url}/auth/signup`: Handle with the user account creation flow.
`{base-url}/auth/change-password`: Handle with the user account reset password flow.

Protected Route:
`{base-url}/search`: Handle with the search of the contacts.
`{base-url}/user`: Handle with contact information
`{base-url}/user/add`: Handle with add action of the contact to the favorites
`{base-url}/user/remove`: Handle with remove action of the contact from the favorites
`{base-url}/favorites`: Handle with the list of favorite contacts. 

## Solution Diagram

### Application


### Components

