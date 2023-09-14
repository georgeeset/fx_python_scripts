# fx_python_scripts
scripts that can be executed periodically and deliver alerts to users.

### Introduction:
This project is a backend routine script for the project [Fx-price-watch](https://github.com/georgeeset/fx-price-watch)
the scripts will run routingly to fetch recent trading data and send messages to users based on their requests.

### Aim of project**
- Fetch price data form website using webscraping and API service
- Query dataabase alert table request database created by users to check if any of the selected alert conditon have been met.
- Query database alert table for user contact detail and choice of social media or messaging platform
- Send message to users (email and Telegram methods have been implemented for now)

### Technologies:
The following are libraties employed in the project
- The entire project is based on python.
- A little bit of SQL scripts for crating managing and querying Mysql database
- Web scraping libraries
- Currency price tick API

### Limitations
- Only forex and deriv instruments are covered as of october 2023, more currencies will be added as data sources increase.
- The scripts are ment to run and terminate. the shripts will be run using Scheduling a software