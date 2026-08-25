# Day NN — Build the URL Shortener

**Date:** 2026-08-25
**Spend so far:** $0.00
**Resources currently running:** None — everything ran locally on my computer

---

## What I built

i built a URL shortener API using FastAPI and SQLite. It can create short codes and redirect users to the original URL, count clicks and check the health of the storage system.i also added automated tests and finished with all 8/8 tests passing.

## The thing that took longest

Understanding how the FastAPI application works took the longest. I spent the most time understanding how the short-code redirect works, and especially how the Store abstraction connects main.py to SQLite without making main.py depend directly on the database. I also had to debug the /healthz implementation and the missing health() method in SqliteStore.


## What broke, and what I learned



### /healthz returned 404

- **What I expected to happen:**I expected /healthz to return 200 because the health endpoint was supposed to be implemented.
- **What actually happened:** assert (await client.get("/healthz")).status_code == 200 E assert 404 == 200 E + where 404 = <Response [404 Not Found]>
- **What I thought was causing it:** I think there was something wrong with the test or the request.
- **What was actually causing it:**The /healthz route was not correctly available in the application at that point.
- **How I found out:**I ran the failing test individually and saw that the request to /healthz returned 404.
- **What I'd check first if I saw this again:**Check that the route exists in main.py and that the correct FastAPI app is being started.
###  SqliteStore was missing health()

- **What I expected to happen:**I expected Uvicorn to start the FastAPI application.
- **What actually happened:** TypeError: Can't instantiate abstract class SqliteStore without an implementation for abstract method 'health'
- **What I thought was causing it:** I am not sure why the application couldn't create the SQLite store.
- **What was actually causing it:** Store required a health() method, but SqliteStore did not implement it as a method of the class.
- **How I found out:**Uvicorn showed the error while loading app.main.
- **What I'd check first if I saw this again:**Check the abstract methods
###  SQLite could not open the database

- **What I expected to happen:**I expected the application to start
- **What actually happened:** sqlite3.OperationalError: unable to open database file
- **What I thought was causing it:** SQLite cant find the right path.
- **What was actually causing it:**SQLite could not open the database at the configured path.
- **How I found out:**The traceback pointed to sqlite3.connect(self.db_url).
- **What I'd check first if I saw this again:**Check the database URL/path and make sure the directory exists and is accessible.

## Concepts I can now explain to someone else
What a 302 redirect does.
Why secrets.choice() is used instead of random.choice().
What a route is in a FastAPI application.
Why checking for a code before inserting it can cause a problem.
The difference between liveness and readiness.


## ❓ What I still don't understand

I want to understand more deeply how the Store abstraction will allow the application to switch from SQLite to PostgreSQL and later Azure storage.


## Commands / snippets worth keeping

Check application health
curl -i http://localhost:8000/healthz
Measure redirect latency
curl -o NUL -s -w "redirect: %{time_total}s\n" -I http://localhost:8000/<CODE>  
## Journal prompts
1-Short-code decision and collision math

I decided to use 7 character short codes with an alphabet of 62 characters (a-z, A-Z, and 0-9). This gives 62⁷ = 3,521,614,606,208, or about 3.5 trillion possible codes.i could use more than 7 characters, but that would make the short URLs longer without providing a useful benefit for this project. For the collision experiment, I temporarily changed the code length to one characterand it reduced the number of possible codes to only 62.
2-the 301 experiment
The browser had cached the permanent 301 redirect, so the browser could use its cached redirect without contacting my server again.
3-Baseline redirect latency
I measured the time taken for my application to process a redirect using:
curl -o NUL -s -w "redirect: %{time_total}s\n" -I http://localhost:8000/KbHqHiB
The result was:
redirect: 0.228832s
So my baseline redirect latency on Day 2 was approximately 0.229 seconds.
## Tomorrow
Start **Day 3 — First VM and Linux hosting**. Take the URL shortener that is finished locally today and deploy it to an Azure VM.
