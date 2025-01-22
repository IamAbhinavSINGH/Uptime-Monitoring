# Uptime Monitor with Discord Notifications

## Project Overview
This project is an completion of an assignment for a backend developer intern role given by "Dhruv Gera".
It is a service that monitors the availability of websites and sends notifications through Discord webhooks when a site becomes unreachable or recovers. Built with **FastAPI** and **MongoDB**, it provides an API to manage monitored sites and includes a background task to handle periodic status checks.

I am sorry for submitting the assignment this late as my university exams were going on so I did not had much time to work on this project and thus I could only spent around 5-6 hrs on this project.

## Setup Gide
You can either use the docker file to setup this repo or do it manually. I am adding the manual steps below
- Clone the repo
  ```
    git clone https://github.com/IamAbhinavSINGH/uptime-monitoring.git
  ```

- Make a virtual environment (for Windows)
  ```
    pip install virtualenv
    python -m venv myenv
    myenv\Scripts\activate
  ```

- Install dependencies
  ```
    pip install -r requirements.txt
  ```

- Add Mongodb String & Discord Webhook URL
  ```
    This project uses mongodb as a database so you need to get a mongodb string and then you need to add the string to "app/config.py" file like below

     MONGODB_URL: str = "Your mongodb string"

     You also need to get the discord webhook URL and add it in the "app/config.py" file although you can also add it by calling "/webhook" endpoint with the following body
     {
        "webhook_url" : "Your webhook url",
        "website_id" : "Id of the website to which you want it to add to"
     }
  ```

- Run the server
  ```
    uvicorn main:app --reload
  ```

## Assumptions
 There are certain assumptions that I made while working on this assignment and I am listing them below

 - You will be following the setup gide stated above and using the python environment and will be using a windows machine as I have not tested it on a linux machine yet
 - I am assuming that you have done all the setup correctly and you have also set up the mongodb string and webhook url
 - I am assuming that you will be using a Postman like application or curl requests to hit the endpoint

## Design Decisions

This is obviously a very simplified version of a website monitoring system and it could be made much scalable but due to time constraints cause of my university exams I have made it much simpler. In a real world scneario a uptime monitoring system will have multiple nodes which will monitor the website from several diff locations around the world but here I am just checking from a single node.

Since, I did not had much time I could not make it much scalable and managable but if I could have gotten some more time then I'd have done these changes

- So, the current system can easily be made scalable by using a queue like redis to streamling the incoming requests and spawning multiple instances of backend which will pick up jobs from the queue and then they will be monitoring them.

## Features
### Core Features:
- **Website Monitoring**:
  - Add or remove websites to monitor through API endpoints.
  - Monitor websites at a configurable interval (default: 5 minutes).
  - Perform HTTP status checks and track uptime/downtime history.
- **Discord Integration**:
  - Configure one or more Discord webhook URLs.
  - Send notifications when:
    - A website becomes unreachable.
    - A website recovers.
    - The first failed check after a successful status.
    - The first successful check after a failure.
- **Basic Functionality**:
  - Manage expected status codes for websites.
  - Track the response time and other metrics.

### Bonus Features that I have Implemented:

- Support for **multiple Discord webhooks** for different sites.

  You can add different webhook_url to different sites by either adding webhook_url while creating the website by calling "/sites" (POST) endpoint For example:

  ```json
  {
    "url" : "https://example.com",
    "name" : "Website name here",
    "check_interval_seconds" : 300,
    "expected_status_code" : 200,
    "webhook_url" : "Your webhook url here"
  }
  ```

or you can also add different webhook_url to different websites by using "/webhook" (POST) endpoint like this:
```json
  {
    "url" : "https://discord.com/api/webhooks/",
    "website_id" : "6790cef550a71e996d98db2b"
  }
```


