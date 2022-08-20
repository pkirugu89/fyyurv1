#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from collections import defaultdict
import json
import pstats
from pyclbr import Function
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from config import DbConfig
import sys
from sqlalchemy import func
from sqlalchemy.sql import operators,extract
#import datetime
#from babel.dates import format_datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = DbConfig.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    address = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120), nullable = False)
    image_link = db.Column(db.String(500), nullable = False)
    facebook_link = db.Column(db.String(120), nullable = False)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String(180), nullable = False)
    website_link = db.Column(db.String(250), nullable = False)
    seeking_talent = db.Column(db.Boolean, default=True, nullable = False)
    seeking_description = db.Column(db.String(250), nullable = False)
    venue_shows = db.relationship('Show', backref='venue',lazy=True)

    def __init__(self, name,city,state,phone,genres,facebook_link,image_link,website_link,seeking_venue,seeking_description):
      self.name =name
      self.city = city
      self.state = state
      self.phone = phone
      self.genres = genres
      self.facebook_link = facebook_link
      self.image_link = image_link
      self.website_link = website_link
      self.seeking_venue = seeking_venue
      self.seeking_description = seeking_description

    def _repr__(self):
      return f'<Venue{self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.genres} {self.image_link} {self.facebook_link} {self.website_link} {self.seeking_talent} {self.seeking_description}>'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120), nullable = False)
    genres = db.Column(db.String(120), nullable = False)
    image_link = db.Column(db.String(500), nullable = False)
    facebook_link = db.Column(db.String(120), nullable = False)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(200),nullable = False)
    seeking_venue = db.Column(db.Boolean, default=True, nullable = False)
    seeking_description = db.Column(db.String(200), nullable = False)
    artist_show = db.relationship('Show',backref='artist', lazy=True)

    def __init__(self, name,city,state,phone,genres,facebook_link,image_link,website_link,seeking_venue,seeking_description):
      self.name =name
      self.city = city
      self.state = state
      self.phone = phone
      self.genres = genres
      self.facebook_link = facebook_link
      self.image_link = image_link
      self.website_link = website_link
      self.seeking_venue = seeking_venue
      self.seeking_description = seeking_description

    def __repr__(self):
       return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.phone} {self.genres} {self.facebook_link} {self.image_link} {self.website_link} {self.seeking_venue} {self.seeking_description}>'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show (db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer,db.ForeignKey('artists.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

  def __init__(self, artist_id,venue_id,start_time):
     self.artist_id = artist_id
     self.venue_id = venue_id
     self.start_time = start_time

  def __repr__(self):
     return f'<Show {self.id} {self.artist_id} {self.venue_id} {self.start_time}>'
# create all the above tables
db.create_all()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  venues = Venue.query.distinct(Venue.city,Venue.state).all()
  data=[]
  for vn in venues:
    data1={}
    data1['city'] = vn.city
    data1['state']=vn.state
    ven = Venue.query.filter(Venue.city == vn.city, Venue.state == vn.state).all()
    v =[]
    for n in ven:
      nv ={}
      nv['id'] = n.id
      nv['name'] = n.name
    # getting the aggregate number of upcoming shows 
      nv['num_upcoming_shows'] = len(list(filter(lambda show: show.start_time > datetime.now(),n.venue_shows))) 
      v.append(nv)
    data1['venues'] = v
    data.append(data1)  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_termz = request.form.get('search_term', '')
  venue_look = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_termz}%')).all()
  for v in venue_look:
    venue_future_shw = list(filter(lambda show: show.start_time > datetime.now(), v.venue_shows))
    vu_shows =[]
    vshows = {
      'id':v.id,
      'name': v.name,
      'num_upcoming_shows':len(venue_future_shw)
      }
    vu_shows.append(vshows)
  response={
      "count": len(venue_look),
      "data": vu_shows
    }   
        
  return render_template('pages/search_venues.html', results=response, search_term=search_termz)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = db.session.query(Venue).filter_by(id=venue_id).one()
  #data = []
  data1={}
  # past shows
  VenuePastShows = list(filter(lambda show: show.start_time < datetime.now(),venue.venue_shows))
  past_shows =[]
  for ve in VenuePastShows:
    artistInfo = Artist.query.filter_by(id = ve.artist_id).one()
    vn ={
      'artist_id': ve.artist_id,
      'artist_name': artistInfo.name,
      'artist_image_link': artistInfo.image_link,
      'start_time': ve.start_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    past_shows.append(vn)
  # Upcoming shows
  FutureShows = list(filter(lambda show: show.start_time > datetime.now(),venue.venue_shows))
  venue_upcoming_shows =[]
  for vs in FutureShows:
    vshow_artist = Artist.query.filter_by(id = vs.artist_id).one()
    artists_shows ={
      'artist_name': vshow_artist.name,
      'artist_image_link': vshow_artist.image_link,
      'start_time': vs.start_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    venue_upcoming_shows.append(artists_shows)
    # Converting venue genre array into string and splitting them
    global venue_genre
    venue_genre =''
    venue_genre = ''.join(map(str,venue.genres)).split(',')

  data1={
    "id": venue.id,
    "name": venue.name,
    "genres": venue_genre,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows_count": len(past_shows),
    "past_shows":past_shows,
    "upcoming_shows_count": len(venue_upcoming_shows),
    "upcoming_shows" : venue_upcoming_shows
  }
 # data.append(data1)
  #data = list(filter(lambda d: d['id'] == venue_id, [data1]))[0]
  return render_template('pages/show_venue.html', venue=data1)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  form = VenueForm(request.form)
  try:
      vname = form.name.data
      vcity = form.city.data
      vstate = form.state.data
      vaddress = form.address.data
      vphone = form.phone.data
      vgenres = form.genres.data
      vfb_link = form.facebook_link.data
      vimg_link = form.image_link.data
      vsite_link = form.website_link.data
      vseek_talent = form.seeking_talent.data
      vseek_desc = form.seeking_description.data
      addVenue = Venue(name=vname,city=vcity,state=vstate,address=vaddress,phone=vphone,
      genres=vgenres,facebook_link=vfb_link,image_link=vimg_link,website_link=vsite_link,
      seeking_talent=vseek_talent,seeking_description=vseek_desc)
      db.session.add(addVenue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + vname + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
    flash('An error occurred. Venue ' + vname + ' could not be listed.')
  finally:
    db.session.close()  
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error =False
  try:
    venue_del = Venue.query.filter_by(id = venue_id).one()
    db.session.delete(venue_del)
    db.session.commit()
    flash('Record has been successfully deleted')
    return redirect(url_for('index'))
  except:
    error = True
    db.session.rollback()
    flash('Record has failed to be deleted')
    return redirect(url_for('index'))
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/venue.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  allArtists = Artist.query.all()
  # for a in allArtists:
  #   data=[{"id":a.id,"Name":a.name}]
  print(allArtists)
  return render_template('pages/artists.html', artists=allArtists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response ={}
  search_term =request.form.get('search_term', '')
  lookitem=db.session.query(Artist).filter(Artist.name.ilike(f'%{search_term}%')).all()
  for l in lookitem:
    upcoming_shows = list(filter(lambda show: show.start_time > datetime.now(),l.artist_show))
    u_shows =[]
    ushows = {
      'id': l.id,
      'name': l.name,
      'num_upcoming_shows': len(upcoming_shows)
      }
    u_shows.append(ushows)
  response={
      "count": len(lookitem),
      "data": u_shows
    }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = db.session.query(Artist).filter_by(id=artist_id).one()
  #print(artist)
  #data=[]
  data1 ={}
  pastArtistShow = list(filter(lambda show: show.start_time < datetime.now(),artist.artist_show))
  artist_past_shows =[]
  for v in pastArtistShow:
    venueInfo = Venue.query.filter_by(id = v.venue_id).one()
    pst = {
      'venue_id':v.venue_id,
      'venue_name': venueInfo.name,
      'venue_image_link': venueInfo.image_link,
      'start_time': v.start_time.strftime("%Y/%m/%d %H:%M:%S")
    }
    artist_past_shows.append(pst)
  # Upcoming shows 
  ShowsUpcoming = list(filter(lambda show: show.start_time > datetime.now(), artist.artist_show))
  artist_upcoming_shows =[]
  for upshows in ShowsUpcoming:
    show_venue = Venue.query.filter_by(id = upshows.venue_id).one()
    up_show ={
      'venue_name' : show_venue.name,
      'venue_image_link':show_venue.image_link,
      'start_time' : upshows.start_time.strftime("%Y%m%d %H:%M:%S")
    }
    artist_upcoming_shows.append(up_show)
    # Converting the genre array to string values and splitting them
    global genre_artist
    genre_artist = ''
    genre_artist = ''.join(map(str,artist.genres)).split(',')
  data1={
        "id": artist.id,
        "name": artist.name,
        "genres":genre_artist,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows_count": len(artist_past_shows),
        "past_shows": artist_past_shows,
        "upcoming_shows_count": len(artist_upcoming_shows),
        "upcoming_shows":artist_upcoming_shows
      }
  #data.append(data1)
 # data = list(filter(lambda d: d['id'] == artist_id, [data1]))[0]
  return render_template('pages/show_artist.html', artist=data1)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist=db.session.query(Artist).get(artist_id)
  form = ArtistForm(id = artist.id) 
  # TODO: populate form with fields from artist with ID <artist_id>
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  form.image_link.data = artist.image_link
  form.website_link.data = artist.website_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  form.populate_obj(artist)
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  error = False
  ed =db.session.query(Artist).get(artist_id)
  try:
    ed.name=form.name.data
    ed.city=form.city.data
    ed.state=form.state.data
    ed.phone=form.phone.data
    ed.genres=form.genres.data
    ed.facebook_link=form.facebook_link.data
    ed.image_link = form.image_link.data
    ed.website_link = form.website_link.data
    ed.seeking_venue = form.seeking_venue.data
    ed.seeking_desc = form.seeking_description.data
    # update the record
    db.session.add(ed)
    db.session.commit()
    flash('Record has been successfully updated')
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
    flash('An error occurred. Recordcould not be updated')
  finally:
    db.session.close()    
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue= db.session.query(Venue).get(venue_id)
  form = VenueForm(id = venue.id)
  # TODO: populate form with values from venue with ID <venue_id>
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.phone.data = venue.phone
  form.address.data = venue.address
  form.genres.data = venue.genres
  form.image_link.data = venue.image_link
  form.facebook_link.data = venue.facebook_link
  form.website_link.data = venue.website_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  form.populate_obj(venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  ev = db.session.query(Venue).get(venue_id)
  error=False
  try:
    ev.name=form.name.data
    ev.city=form.city.data
    ev.state=form.state.data
    ev.phone=form.phone.data
    ev.genres=form.genres.data
    ev.address=form.address.data
    ev.image_link=form.image_link.data
    ev.facebook_link=form.facebook_link.data
    ev.website_link=form.website_link.data
    ev.seeking_talent=form.seeking_talent.data
    ev.seeking_desc=form.seeking_description.data
# updating venue data
    db.session.add(ev)
    db.session.commit()
    flash('Record has been updated successfully !!!')
  except: 
    db.session.rollback()
    error = True
    print(sys.exc_info())
    flash('An error occurred. Record could not be updated') 
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  error = False
  try:
    artist_name = form.name.data
    artist_city = form.city.data
    artist_state = form.state.data
    artist_phone = form.phone.data
    artist_genres = form.genres.data
    artist_img_link= form.image_link.data
    artist_fb_link = form.facebook_link.data
    artist_site_link = form.website_link.data
    artist_seek_venue = form.seeking_venue.data
    artist_seek_desc = form.seeking_description.data
    # adding the record to the db
    add_artist = Artist(name=artist_name,city=artist_city,state=artist_state,phone=artist_phone,genres=artist_genres,
    facebook_link=artist_fb_link,image_link=artist_img_link,website_link=artist_site_link,seeking_venue=artist_seek_venue,
    seeking_description=artist_seek_desc)
    db.session.add(add_artist)
    db.session.commit()
  # on successful db insert, flash success
    flash('Artist ' + artist_name + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
    flash('An Error has occured. Artist'+artist_name+'could not be listed')
  finally:
    db.session.close()  

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  show_list = Show.query.all()
  data =[]
  for sh in show_list:
    data1={}
    data1['venue_id'] = sh.venue_id
    data1['artist_id'] = sh.artist_id
    data1['start_time'] = sh.start_time.strftime("%Y-%m-%d %H:%M:%S")
    data1['artist_name'] = sh.artist.name
    data1['artist_image_link'] = sh.artist.image_link
    data1['venue_name'] = sh.venue.name
    data.append(data1)
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  form = ShowForm(request.form)
  try:
    sh_artist_id = form.artist_id.data
    sh_venue_id = form.venue_id.data
    sh_start_time = form.start_time.data
    # adding a show record
    addShow = Show(artist_id=sh_artist_id,venue_id=sh_venue_id,start_time=sh_start_time)
    db.session.add(addShow)
    db.session.commit()
  # on successful db insert, flash success
    flash('Show for artist'+sh_artist_id+'was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
    flash('An error occurred. Show for'+sh_artist_id+'could not be listed.')
    #print(sh_artist_id+sh_venue_id+sh_start_time)
  finally:
    db.session.close()  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
