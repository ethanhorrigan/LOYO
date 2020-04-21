
# Applied Project & Minor Dissertation

![Arch1](https://github.com/ethanhorrigan/Applied-Project-Minor-Dissertation/blob/master/img/Archetciture2.png)

![Arch2](https://github.com/ethanhorrigan/Applied-Project-Minor-Dissertation/blob/master/img/Archetciture.png)

### Setup
## Features
- Allow users to create and manage custom matches
- Automatic Matchmacking
- User Registration and Authentication
- 
## Usage (Optional)
## Documentation (Optional)

## Build

 > The build artifacts will be stored in the `dist/` directory.

 ```shell
$ ng build
```

## Running unit tests

> To execute unit tests via [Karma](https://karma-runner.github.io)

 ```shell
$ ng test
```

## Running end-to-end tests

To execute the end-to-end tests via [Protractor](http://www.protractortest.org/)

 ```shell
$ ng e2e
```

## Tests 

> Unit Test Server

```shell
$ python loyo_python_test.py
```

---

## Contributing

> To get started...

### Step 1

- **Option 1**
    - 🍴 Fork this repo!

- **Option 2**
    - 👯 Clone this repo to your local machine using `https://github.com/ethanhorrigan/Applied-Project-Minor-Dissertation`
    - pip install cassiopeia
    - pip install riotwatcher

## Average MMR

![MMR](https://github.com/ethanhorrigan/Applied-Project-Minor-Dissertation/blob/master/research/MMR.PNG)

## TO-DO
- Implement Elo System
- Allow player to create match
- Remove match when winner has been determined
- Create Request for updating players game outcome
- begin matchmaking when enough participants 
- add option for admin ONLY to determine game outcome
- update players values accordingly
- only show games on page where outcome is pending

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
- 20/04/2020 Deploy Angular to Firebase


## Helpful Project Links

- Angular Cheat Sheet: https://angular.io/guide/cheatsheet
- FA Icons: https://fontawesome.com/v4.7.0/icons/
- https://www.spiderposts.com/2019/07/04/flask-sqlalchemy-tutorial-login-system-with-python/
- https://stackoverflow.com/questions/48775478/flask-user-login-check-if-user-exists


## Dissertation links

https://medium.com/@SoftwareDevelopmentCommunity/what-is-service-oriented-architecture-fa894d11a7ec
