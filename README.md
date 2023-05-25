# Description

This project consists of four modules:

Data Parsing: This module is responsible for parsing data from a specific source.
Data Conversion: The parsed data is passed through the ChatGPT API to convert it into a desired format.
Data Posting: The converted data is then posted to a VK group using the VK API.
Error Notification: In case of any errors, a notification is sent to a Telegram channel.

## Installation 

To install and run the application, please follow the steps below:

1. Clone the repository to your local machine.
2. Create a .env file in the project's root directory and add the necessary tokens (refer to the src/start.py file for the required tokens).
3. Build the Docker image using the following command:
docker build -t IMAGE_NAME.
4. Run the Docker container using the following command:
docker run IMAGE_NAME

## Configuration 

Before running the application, make sure to configure the necessary parameters.

## Configuration 
Monitoring and Logging
You can monitor and view the logs of your Docker container using the following command:
docker logs CONTAINER_NAME


## Errors and Notifications
If any errors occur during the execution of the script or if you want to receive notifications, the application can send messages to a Telegram channel. Make sure you have a configured Telegram bot and access token. Edit the corresponding settings in the config.py file.

## Contribution and Feedback
If you have any questions, suggestions, or found any issues, please feel free to reach out to us or create an issue in the project repository.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
