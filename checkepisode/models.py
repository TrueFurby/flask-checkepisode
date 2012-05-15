from checkepisode import app
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

from passlib.apps import custom_app_context as pwd_context

favorite_series = db.Table('favorite_series',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('series_id', db.Integer, db.ForeignKey('series.id'))
)

watched_episodes = db.Table('watched_episodes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('episode_id', db.Integer, db.ForeignKey('episode.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), unique=True)
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(128))
    favorite_series = db.relationship('Series', secondary=favorite_series,
        backref=db.backref('users', lazy='dynamic'))
    watched_episodes = db.relationship('Episode', secondary=watched_episodes,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, name, password):
        app.logger.info('Creating user "%s".', name)
        self.name = name
        self.password = pwd_context.encrypt(password)

    def verify(self, password):
        return pwd_context.verify(password, self.password)
        
class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(2), unique=True, nullable=False)

    def __init__(self, caption):
        self.caption = caption

    def __repr__(self):
        return '<Language %r>' % self.caption
        
class Network(db.Model):
    __tablename__ = 'network'
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(40), unique=True, nullable=False)

    def __init__(self, caption):
        self.caption = caption

    def __repr__(self):
        return '<Network %r>' % self.caption
        
series_genres = db.Table('series_genres',
    db.Column('series_id', db.Integer, db.ForeignKey('series.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)
        
class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(40), unique=True, nullable=False)

    def __init__(self, caption):
        self.caption = caption

    def __repr__(self):
        return '<Genre %r>' % self.caption
    
class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, caption):
        self.caption = caption

    def __repr__(self):
        return '<Status %r>' % self.caption
        
class Series(db.Model):
    __tablename__ = 'series'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    tvdb_id = db.Column(db.Integer, unique=True)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    language = db.relationship('Language',
        backref=db.backref('series', lazy='dynamic'))
    first_aired = db.Column(db.String(8))
    airs_dow = db.Column(db.String(2))
    airs_time = db.Column(db.String(7))
    genre = db.relationship('Genre', secondary=series_genres,
        backref=db.backref('series', lazy='dynamic'))
    imdb_id = db.Column(db.String(10))
    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    network = db.relationship('Network',
        backref=db.backref('series', lazy='dynamic'))
    overview = db.Column(db.Text)
    tvdb_rating = db.Column(db.Float)
    tvdb_ratecount = db.Column(db.Integer)
    runtime = db.Column(db.Integer)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    status = db.relationship('Status',
        backref=db.backref('series', lazy='dynamic'))
    last_update = db.Column(db.Integer)
    banner = db.Column(db.String(40))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Series %s>' % self.name
        
class Episode(db.Model):
    __tablename__ = 'episode'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    tvdb_id = db.Column(db.Integer, unique=True, nullable=False)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    air_time = db.Column(db.String(8))
    seas_num = db.Column(db.Integer)
    epis_num = db.Column(db.Integer)
    overview = db.Column(db.Text)
    tvdb_rating = db.Column(db.Float)
    tvdb_ratecount = db.Column(db.Integer)
    last_update = db.Column(db.Integer)
    graphic = db.Column(db.String(40))
    
    series = db.relationship('Series',
        backref=db.backref('episodes', lazy='dynamic'))

    def __init__(self, epID):
        self.tvdb_id = epID

    def __repr__(self):
        return u'<Episode %d>' % self.tvdb_id
        
    @property
    def runtime(self):
        if not isinstance(self.air_time, unicode):
            return self.air_time
        t = self.series.airs_time
        if t is None:
            t = '00:00AM'
        return datetime.strptime('%s %s'%(self.air_time, t), '%Y%m%d %I:%M%p')
