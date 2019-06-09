
# Sched.py

This is just a very simple CLI to add events to google calendar using "quick add" strings.

## Usage

```
> python3 sched.py "Call Bob tomorrow at 8pm"
Event occurs in 22 hours, 22 minutes, 8 seconds
> python3 sched.py "Get haircut on june 22"
Event occurs in 13 days, 2 hours, 17 minutes, 20 seconds
```

See documentation elsewhere for all the different options with google's "quick add" command

## Installation

Use pip with virtualenv with the packages in requirements.txt

Add your own credentials.json file to the same directory of the sched.py from the google API developer pages.

Then upon running it the first time, it will ask you for your credentials which it will cache to file for next time.

Note that it will always use your primary calendar.

