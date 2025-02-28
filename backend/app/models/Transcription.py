from app import db
from datetime import datetime, timezone, timedelta

# Singapore time zone UTC+8
sg_time = datetime.now(timezone(timedelta(hours=8)))

class Transcription(db.Model):
    __tablename__ = "Transcription"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_id = db.Column(db.Integer, db.ForeignKey('Audio.id'), nullable=False)
    transcribed_text = db.Column(db.Text, nullable=False)
    created_time = db.Column(db.DateTime, default=sg_time)

    audio = db.relationship("Audio", backref=db.backref("audio_transcription", uselist=False), uselist=False)