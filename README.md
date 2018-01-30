# About

Source for my web app: [Is Bristol Choking](isbristolchoking.uk). Scrapes air pollution data from
the Bristol Air Quality website and displays it on a single page with binary
yes or no based on the legal limits.

I rolled this together in a couple of mornings and free hours to learn Flask
and Python web app technologies. For this reason it is fairly rough around the
edges.

# Run

Create .env file with Google Maps API key or set environment variable.

```
pipenv install
pipenv run gunicorn app:app
```

Visit localhost:8000 to see the site.
