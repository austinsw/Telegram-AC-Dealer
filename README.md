# Telegram AC Dealer
A Telegram bot for granting a certain number of permission to GM and buying Telegram account. made in 2021

## Run
The code is run on Python 3. If Python 3 is not your default interpreter (say Python 2.7), you will probably need `pip3 install`, and `python3` command to install the packages and run the .py file.

If the packages are not already installed, run the code to install the package: E.g. `pip install python-telegram-bot --upgrade`

`python ACDealer3.1.py` to run the file: It was originally created on PyCharm, but can be put on a virtual machine, say Google Cloud for 24/7 usesage.

## ACDealer3.1py
Newest version 
- threading allows multiple users to buy account at the same time

Although the `users`, `users_num` and `super_users` lists are pre-defined in the code, they are actually later loaded from ***users.txt***, ***users_num.txt*** and ***super_users.txt***, i.e. keep the most updated record in the *.txt* files, no need to constanlty make changes on the code itself. Each entry in those 3 files should be followed by a comma `,`.

Each entry in ***users.txt*** corresponds to each entry in ***users_num.txt***, i.e. they should have same number of records. `users` refer to normal usesr who would request buying account. `users_num` refers to their corresponding number of quota. `super_users` are the admins and can add new user and quotas through Telegram. Both `users` and `super_users` support both id and username.

### Set up the basics
Change the following lines of code accordinly:
- `BOT_TOKEN ` Insert the Telegram bot token
- `sim_token` Insert the 5sim api token
- `country` If one country fails too often, can change to another e.g. 'america', 'philippines', etc.

### Commands in Telegram
Only users can use:
- `/request` Requesting a phone no. and sms

Only super users can use:
- `/add {user_id} {num}` Adding new user and quota. To deduct quota (or remove completely), simly use a negative number to replace {num}, e.g. `/add User1 -100`
- `/list` Listing out all users and their quota
- `/user {user_id}` Checking that specific user's quota

Anyone can use:
- `/help` Displaying the above 4 commands
- `/start` Testing to see if the bot is working. The bot will reply with the sender's id

Telegram user / group chat id can be checked by Nicegram or by other means.

## dispatcher2.py
Old version

Need to add threading to handle multiple users' event? Javascript?

### Commands in Telegram:
- For requesting a phone no. and sms: `/request`
- For adding new user: `/add {user_id} {num}`
- For listing all the user status: `/list`
- For checking a specific user status: `/user {user_id}`
- `/help`
- `/start`

Only super users can use 2,3,4. Normal users can only use 1.
