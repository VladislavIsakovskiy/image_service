# Image service

This service is designed to:
- provide information on existing images on server
- create new image from file
- create new image from base64 string
- delete existing image

## Endpoints
- GET /images - Return info for all images that contain server
- GET /images/{image_name} - Returns info for particular image
- POST /images/{image_name} - Add new image to server from base64 str
- DELETE /images/{image_name} - Delete existed image

## Start service
To start service using Docker use command:
`docker-compose up --build`
