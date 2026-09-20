# # [Sprint 2] Unit tests สำหรับ Interaction API
# from src.interaction import Interaction
# from unittest.mock import patch, MagicMock

# def _fake_response(json_data):
#     resp = MagicMock()
#     resp.json.return_value = json_data
#     return resp

# def test_fetch_dog_image_success():
#     with patch("src.interaction.requests.get", return_value=_fake_response({"message": "dog.jpg"})):
#         assert "dog.jpg" in Interaction.fetch_dog_image()

# def test_fetch_weather_success():
#     fake_data = {"current_condition":[{"weatherDesc":[{"value":"Sunny"}]}]}
#     with patch("src.interaction.requests.get", return_value=_fake_response(fake_data)):
#         assert "Sunny" in Interaction.fetch_weather("Bangkok")
