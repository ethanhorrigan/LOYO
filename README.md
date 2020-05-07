

<p align="center">
  <img width="250" height="250" src="https://i.imgur.com/zW8EOj9.png">
</p>

# Applied Project & Minor Dissertation
A Service for users to Create, Manage & Participate in Online Custom Games. With a Matchmkaing System and an Integrated Point System, This service allows users to manage their events.

## Screencast
[![screencast](https://img.youtube.com/vi/vccfBFOMI0I/0.jpg)](https://www.youtube.com/watch?v=vccfBFOMI0I)

Simply click on the picture to open the screencast video or https://www.youtube.com/watch?v=vccfBFOMI0I
![Arch](https://github.com/ethanhorrigan/Applied-Project-Minor-Dissertation/blob/master/img/MainArchitecture.png)


## Setup
- **Clone**
    - Clone this repo to your local machine using:

    ```git clone https://github.com/ethanhorrigan/LOYO.git```

- **Install**

    - Install Python Packages:

    ```pip install -r requirements.txt```
    - If using Python3:

    ```pip3 install -r requirements.txt```
    
    - Install Angular CLI (Note: Node may have to be installed: [NodeJS](https://nodejs.org/en/)

    ```pip3 install -r requirements.txt```

    - NOTE: Packages may have to be installed.

    ```cd frontend/```

    ```npm install```

## Running & Testing 
- **Running**

    ```cd frontend/```
    ```ng serve --open```

- **Testing**

    - Unit Tests:

    ```ng test```

    - e2e Tests:

    ```ng e2e```

- **Build & Deploy**

    - Build

    ```cd frontend/```
    ```ng build --prod --aot```
    
    - Deploy

    ```firebase deploy```  

---

## Change Log
- 29/01/2020 - Changed Database from SQLIte to MongoDB
- 30/01/2020 - Connected to monogoDB through mongoose
- 31/01/2020 - Refactored all tables in the database
- 31/01/2020 - Leaderboards added (Server-Side & Client-Side)
- 31/01/2020 - In order to recieve tournament codes from Riot, the matches that are created must be prized. to combat this, i will create a points system, where players
recieve points from winning games. These points can then be spent to purchase in-game rewards.
Submission for tournament codes: http://competitive.euw.leagueoflegends.com/competitive/prized/submit-tournament
- 02/02/2020 - Registration changed from SQLite to MongoDB
- 03/02/2020 - Added Angular Material
- 03/02/2020 - .gitpod.yml
- 16/02/2020 - user authentication
- 20/02/2020 - Retrieve Summoner Data
- 26/02/2020 - Riot API Key Problem
Production App:
Register your project to apply for a Production API Key with access to the Standard APIs and/or Tournaments API. A Production API key requires a working prototype. Production API keys are not for testing purposes. You may submit an application in the planning stage of your project, but your application for a production key won’t be approved until your project is ready for public consumption. Work in progress should be tested using your demo key.
- 26/02/2020 - Observables in Typescript are asynchronous, this causes many issues with user authentication to solve this problem i used
ConcatMap (https://www.learnrxjs.io/learn-rxjs/operators/transformation/concatmap)
- 27/02/2020 - Added Role (SVG) Icons
- 28/02/2020 - Password Encryption
- 28/02/2020 - Lobby System and Design Implemented
- 28/02/2020 - Begin Session-Based User Authentication
- 01/02/2020 - Documenting Backend Code.
- 02/02/2020 - Began Changing the Database.
- 26/03/2020 - Fixed HTTP request issue due to HTTPClientTesting module overriding HTTPClient Module
- 02/04/2020 - Refactored Postgres and Parameterised Queries 
- 18/04/2020 - https://stackoverflow.com/a/42458129 Unique URL Angular
- 18/04/2020 - https://www.infragistics.com/products/ignite-ui-angular/angular/components/time_picker.html TimePicker
- 20/04/2020 - Deploy Angular to Firebase
- 22/04/2020 - total_games Post fix and total_games riot api fix

## Helpful Project Links

- DB tips and tricks: http://archive.oreilly.com/oreillyschool/courses/Python2/DatabaseHintsAndTricks.html
- Angular Cheat Sheet: https://angular.io/guide/cheatsheet
- FA Icons: https://fontawesome.com/v4.7.0/icons/
- https://www.spiderposts.com/2019/07/04/flask-sqlalchemy-tutorial-login-system-with-python/
- https://stackoverflow.com/questions/48775478/flask-user-login-check-if-user-exists
