# About

**20/01/2019: [Features in GCN 'How Toxic Is City Cycling? | GCN Investigates'](https://www.youtube.com/watch?v=ySzmo_sScQk)**

Source for my web app: [Is Bristol Choking](http://www.isbristolchoking.uk). Scrapes air pollution data from
the Bristol Air Quality website and displays it on a single page with binary
yes or no based on the legal limits.

I rolled this together in a couple of mornings and free hours to learn Flask
and Python web app technologies. For this reason it is fairly rough around the
edges.

## Systems Used

* [Flask](http://flask.pocoo.org/)
* [Bootstrap 4](https://v4-alpha.getbootstrap.com/) - example 'album' used as a template.
* [Flask SocketIO](https://flask-socketio.readthedocs.io/en/latest/) - for
  async scraping on user loading page.
* [CSS Coding Animation](https://github.com/Chippd/css_loading_animation) -
  used for loading placeholder.

## Run

Create .env file with Google Maps API key or set environment variable.

```
pipenv install
pipenv run gunicorn app:app
```

Visit [localhost:8000](http://localhost:8000) to see the site.
