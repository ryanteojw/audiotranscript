from app import db
from ..models.Audio import Audio
from ..models.Transcription import Transcription
from ..utils import whispertiny

# helper function to process each file to be committed to the db
def single_file_processing(file):
    try:
        uploaded_filename = file.filename
        file_content = file.read()

        # create Audio object and store in Audio table
        new_audio = Audio (
            filename = uploaded_filename,
            file_data = file_content
        )
        
        db.session.add(new_audio)
        db.session.flush()

        # send the audio file to the ml model
        text = whispertiny.transcribe_text(file_content)

        # create Transcription object and store in Transcription table
        new_transcription = Transcription (
            file_id = new_audio.id,
            transcribed_text = text['text']
        )
        db.session.add(new_transcription)

        db.session.commit()
        # index 0 is filename, index 1 is error msg
        return uploaded_filename, None

    except Exception as e:
        # rollback the current file transaction if there is any issue
        db.session.rollback()  
        return None, str(e) 