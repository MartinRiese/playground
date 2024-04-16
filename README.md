# Collection of django apps

Use `./manage.py runserver 7000` to run the server

## Shortly

A url shortener

`curl --location 'localhost:7000/shortly/' --header 'Content-Type: text/plain' --data 'https://google.com'` to get hash.

`curl --location 'localhost:7000/shortly/ksvwj4zu-tw'` to resolve shortened url.
