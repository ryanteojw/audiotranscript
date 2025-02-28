from flask import jsonify, Blueprint, request
from app import db
from ..models.Audio import Audio
from ..models.Transcription import Transcription
from ..utils import whispertiny
import json, base64

transcribe_routes = Blueprint('transcibe', __name__)

@transcribe_routes.route('/transcriptions', methods=['GET'])
def get_all_transcriptions():
    try:
        # query all the data in Transcription table
        transcription_query_list = Transcription.query.all()
        transcription_list = []

        # loop through each row in the query list
        for transcription in transcription_query_list:
            # temp dictionary to store all the relevant data
            transcription_dict = {}
            transcription_dict["id"] = transcription.id

            audio_filename = Audio.query.get(transcription.file_id).filename
            transcription_dict["filename"] = audio_filename

            audio_file = Audio.query.get(transcription.file_id).file_data
            # convert binary data to base64 string
            transcription_dict["file_data"] = f"data:audio/{audio_filename[-3:]};base64,{base64.b64encode(audio_file).decode('utf-8')}"

            transcription_dict["transcribed_text"] = transcription.transcribed_text
            transcription_dict["uploaded_timestamp"] = Audio.query.get(transcription.file_id).created_time
            transcription_dict["finished_processing_timestamp"] = transcription.created_time
            # append each row "dictionary" into the return list
            transcription_list.append(transcription_dict)
        
        return jsonify(
            {
                "message": "Successfully retrieved data!",
                "data": transcription_list
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "message": f'Failed to retrieve transcriptions!',
                "error" : str(e)
            }
        ), 500

@transcribe_routes.route('/transcribe', methods=['POST'])
def process_audio_file():
    try:
        # get the list of files from form data in the request payload
        file_list = request.files.getlist('audioFiles')

        uploaded_files = []
        failed_files = [file.filename for file in file_list]

        # loop through each audio file to be passed into the ml model
        for file in file_list:
            uploaded_filename = file.filename
            file_content = file.read()
            # create Audio object and store in Audio table
            new_audio = Audio(
                filename = uploaded_filename,
                file_data = file_content
            )
            db.session.add(new_audio)
            db.session.flush()
            # send the audio file to the ml model
            text = whispertiny.transcribe_text(file_content)

            # create Transcription object and store in Transcription table
            new_transcription = Transcription(
                file_id = new_audio.id,
                transcribed_text = text['text']
            )
            db.session.add(new_transcription)

            # commit into the db
            db.session.commit()

            # update the file lists
            uploaded_files.append(uploaded_filename)
            failed_files.remove(uploaded_filename)

        return jsonify(
            {
                "message": "Successfully uploaded audio files!",
                "data": uploaded_files
            }
        ), 200
    except Exception as e:
        # undo db changes
        db.session.rollback()
        return jsonify(
            {
                "message": f'Failed to upload all audio files!',
                "failed_files" : failed_files,
                "error" : str(e)
            }
        ), 500