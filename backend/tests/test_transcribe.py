import os
from unittest.mock import patch, MagicMock
from test_base import SetUpTestCase
from app.utils.whispertiny import transcribe_text
from app.utils.file_processing import single_file_processing

class TranscribeTestCase(SetUpTestCase):
    # test for transcribe_text function in whispertiny.py in utils folder
    @patch('app.utils.whispertiny.transcribe_text')
    def test_transcribe(self, mock_transcribe_text):
        # mock response of known audio file sample 2.mp3
        known_text = " Help me. I can't find my parents. They told me to wait for them, but I saw this pretty butterfly and followed it. Now I am lost."
        mock_transcribe_text.return_value = known_text
        
        # os path to the audio file stored in audio_file folder
        file_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio_file', 'Sample 2.mp3')
        with open(file_directory, 'rb') as audio_file:
            file_content = audio_file.read()

        text_result = transcribe_text(file_content)["text"]
        # check the result obtained from the test
        self.assertEqual(text_result, known_text)
        print("============================= transcribe_text test done! =============================")
    
    # test for single_file_processing function in file_processing.py in utils folder
    @patch('app.utils.file_processing.single_file_processing')
    @patch('app.db.session')
    def test_single_file_processing(self, mock_db_session, mock_transcribe_text):
        mock_file = MagicMock()

        # create a corrupted file by causing an IOError
        mock_file.read.side_effect = IOError("Cant read file")

        # mock db session methods
        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()
        mock_db_session.rollback = MagicMock()
        mock_db_session.flush = MagicMock()

        # call the single_file_processing with the created mock file
        result_filename, error_msg = single_file_processing(mock_file)

        # check the result obtained from the test
        self.assertIsNone(result_filename)
        self.assertIsNotNone(error_msg)

        # rollback is called once
        mock_db_session.rollback.assert_called_once()

        # add, flush, commit is called zero times
        mock_db_session.add.assert_not_called()
        mock_db_session.flush.assert_not_called()
        mock_db_session.commit.assert_not_called()
        print("============================= single_file_processing test done! =============================")