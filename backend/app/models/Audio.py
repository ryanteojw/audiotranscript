from __init__ import db
from datetime import datetime, timezone, timedelta

# Singapore time zone UTC+8
sg_time = datetime.now(timezone(timedelta(hours=8)))

class Audio(db.Model):
    __tablename__ = "Audio"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)
    created_time = db.Column(db.DateTime, default=sg_time)

    transcription = db.relationship("Transcription", backref=db.backref("audio_files", uselist=False), uselist=False)