from flask import jsonify, Blueprint, request
from app import db
from ..models.Audio import Audio
from ..models.Transcription import Transcription
from ..utils import file_processing
import base64

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
                "status": "success",
                "message": "Successfully retrieved data!",
                "data": transcription_list
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "status": "fail",
                "message": 'Failed to retrieve transcriptions!',
                "error" : str(e)
            }
        ), 500

@transcribe_routes.route('/transcribe', methods=['POST'])
def process_audio_file():
    try:
        # get the list of files from form data in the request payload
        file_list = request.files.getlist('audioFiles')

        uploaded_files = []
        failed_files = []

        # loop through each audio file to be passed into the ml model
        for file in file_list:
            # call the helper function single_file_processing defined in utils folder
            uploaded_filename, error = file_processing.single_file_processing(file)

            # update the file lists
            if uploaded_filename:
                uploaded_files.append(uploaded_filename)
            else:
                failed_files.append(file.filename)

        if len(failed_files) > 0:
            return jsonify(
                {
                    "status": "fail",
                    "message": "Failed to upload these audio files!",
                    "data": failed_files
                }
            ), 400
        return jsonify(
            {
                "status": "success",
                "message": "Successfully uploaded audio files!",
                "data": uploaded_files
            }
        ), 200
    except Exception as e:
        # undo db changes
        db.session.rollback()
        return jsonify(
            {
                "status": "fail",
                "message": 'Failed to upload all audio files!',
                "error" : str(e)
            }
        ), 500