# Image service

This service is designed to:
- provide information on existing images on server
- create new image from file
- create new image from base64 string
- delete existing image

## Endpoints
- GET /images - Return info for all images that contain server
- GET /image/{image_name} - Returns info for particular image
- GET /images/{image_name}/delete - Delete existed image
- POST /images/upload_image - Add new image to server from file
- POST /images/upload_image_from_bytes - Add new image to server from base64 str

## Install Poetry
Install poetry according to instructions from https://python-poetry.org/docs/

*If you have problem with MSStore Python:*

Change "run python3" to "run python" in %USERPROFILE%.poetry\bin\poetry.bat 

Use "poetry --version" to check that all is OK.  

Use "poetry install" to install all project dependencies from pyproject.toml

To activate venv use "poetry shell" or
.venv/Scripts/activate.bat (Windows), source .venv/bin/activate (Linux, Mac OS)
