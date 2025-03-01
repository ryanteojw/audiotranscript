from flask import jsonify, Blueprint, request
from app import db
from ..models.Audio import Audio
from ..models.Transcription import Transcription
import base64

search_routes = Blueprint('search', __name__)

@search_routes.route('/search', methods=['GET'])
def get_audio_file():
    try:
        # obtain the user input text
        query_text = request.args.get('query', '')
        # ilike for case insensitive, wildcard to retrieve all relevant rows from Audio and Transcription tables
        filtered_rows = db.session.query(Audio).join(Transcription).filter((Audio.filename.ilike(f"%{query_text}%")) | (Transcription.transcribed_text.ilike(f"%{query_text}%"))).all()
        
        filtered_list = []
        # loop through each row in the query list
        for audio in filtered_rows:
            # temp dictionary to store all the relevant data
            transcription_dict = {}
            transcription_dict["id"] = audio.id
            transcription_dict["filename"] = audio.filename

            audio_file = Audio.file_data
            # convert binary data to base64 string
            transcription_dict["file_data"] = f"data:audio/{audio.filename[-3:]};base64,{base64.b64encode(audio.file_data).decode('utf-8')}"

            transcription_dict["transcribed_text"] = Transcription.query.get(audio.id).transcribed_text
            transcription_dict["uploaded_timestamp"] = audio.created_time
            transcription_dict["finished_processing_timestamp"] = Transcription.query.get(audio.id).created_time
            # append each row "dictionary" into the return list
            filtered_list.append(transcription_dict)
        
        return jsonify(
            {
                "status": "success",
                "message": "Successfully retrieved filtered data!",
                "data": filtered_list
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "status": "fail",
                "message": f'Failed to retrieve audio file!',
                "error" : str(e)
            }
        ), 500