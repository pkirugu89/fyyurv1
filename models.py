from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# Defining the models
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