from flask import jsonify, Blueprint, request
from models.Audio import Audio
from models.Transcription import Transcription

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
            transcription_dict["filename"] = Audio.query.get(transcription.file_id).filename
            transcription_dict["file_data"] = Audio.query.get(transcription.file_id).file_data
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
