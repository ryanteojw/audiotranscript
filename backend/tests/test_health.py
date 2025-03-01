import json
from test_base import SetUpTestCase

# test for GET health API endpoint
class HealthStatusTestCase(SetUpTestCase):
    def test_health_status(self):
        # receive json response from api and check if its success
        response = self.client.get('/health')
        response_json = json.loads(response.data.decode())
        # check the result obtained from the test
        self.assertEqual(response_json["status"], "success")
        print("============================= Health test done! =============================")
