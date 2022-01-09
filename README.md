# Image service

This service is designed to:
- provide information on existing images on server
- create new image from file
- create new image from base64 string
- delete existing image

## Endpoints
- GET /images - Return info for all images that contain server
- GET /image/{image_name} - Returns info for particular image
- DELETE /images/{image_name}/delete - Delete existed image
- POST /images/upload_image - Add new image to server from file or base64 str

## Start service
To start service using Docker use command:
`docker-compose up --build`
