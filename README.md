# Rob the Bot - Django App communicating with Slack to remind people to fill the Skills Form

This project is a tool for the [_Data against Covid-19_](https://twitter.com/data_covid?s=09) initiative.

## Install

- Necessary config vars for launching the two commands : DATABASE_URL, SLACK_BASE_URL, SLACK_TOKEN - ask a project member to give it to you
- The commands can be launched from the Heroku console, as well as locally.


## Two main commands and one endpoint : sync_slack_users, send_reminder and save_user_answer

### 1. sync_slack_users command
- This command gets the list of all workspace users from Slack API and create the missing users in DB. 
- It is meant to be launched every time before triggering the `send_reminder` command, on a daily basis.

### 2. send_reminder command
- This command scans the DB to find all the users who have not answered "yes" to question "Have you already filled the Skills Form?", and sends them a message with this question.
- This should be triggered every day, as a reminder for people to fill the form.

### 3. DB update on user answer
- The endpoint `save_user_answer` is called by the Slack API when people answer the question by clicking "YES" or "NO", to save this answer in DB
