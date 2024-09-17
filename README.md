# Image Processing Service

This is a FastAPI-based image processing service that allows users to upload images, perform various transformations, and store the processed images in Firebase Storage. The service provides endpoints to upload images, retrieve image details, and query transformation frequencies.

## Table of Contents

- [Setup](#setup)
- [Running the Service](#running-the-service)
- [Design Decisions](#design-decisions)
- [Endpoints](#endpoints)
- [Example Request for Upload Image](#example-request-for-upload-image)
- [Testing](#testing)
- [Firebase Setup](#firebase-setup)

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/image-processing-service.git
   cd image-processing-service
   ```

2. **Create a .env File**
   Create a `.env` file in the project directory and add the following variables:

   ```plaintext
   DATABASE_URL=your_database_url
   FIREBASE_CREDENTIALS=path/to/cred.json
   FIREBASE_STORAGE_BUCKET=image-processing-service-ce70c.appspot.com
   ```

3. **Install Dependencies**
   If you are using Docker, you can skip this step as the dependencies will be installed in the Docker container. Otherwise:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Service

### Using Docker

1. **Build the Docker Image**

   ```bash
   docker-compose build
   ```

2. **Run the Service**

   ```bash
   docker-compose up
   ```

The service will be available at `http://localhost:8000`.

### Without Docker

1. Start the application:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   Replace `main:app` with the appropriate module and app name if necessary.

## Design Decisions

- **Framework Choice**: FastAPI was chosen for its performance and ease of use with asynchronous programming.
- **Stateless Service**: The service is designed to be stateless, allowing for easy scaling and load balancing.
- **Database**: SQLAlchemy is used as the ORM for database interactions, providing a clear structure for data models.
- **Image Processing**: The image processing functionality is modularized in a separate utility function to keep the code clean and maintainable.
- **Testing**: Unit tests are included to ensure the functionality of key endpoints and business logic.

## Endpoints

| Method | Endpoint                     | Description                                                                                  |
|--------|------------------------------|----------------------------------------------------------------------------------------------|
| POST   | /upload-image/               | Upload an image and specify transformation parameters (resize, grayscale, rotation).       |
| GET    | /get-image/{image_id}        | Retrieve details of a processed image by its ID, including the public URL and transformations. |
| GET    | /most-frequent-transformation | Get the most frequently applied transformation across all images.                          |
| GET    | /latest-transformations       | Retrieve the latest transformations applied to images.                                      |
| GET    | /ranking-images               | Get a ranking of images based on the number of transformations applied to each.            |

## Example Request for Upload Image

To upload an image with various transformations, you can use the following `curl` command:

```bash
curl -X POST "http://127.0.0.1:8000/upload-image/?width=100&height=100&grayscale=true&rotation=90" -F "file=@test.jpeg"
```

### Description of the Request

- **Method**: POST
- **URL**: `http://127.0.0.1:8000/upload-image/`
- **Query Parameters**:
  - `width=100`: Resize the image to a width of 100 pixels.
  - `height=100`: Resize the image to a height of 100 pixels.
  - `grayscale=true`: Convert the image to grayscale.
  - `rotation=90`: Rotate the image by 90 degrees.
- **File**: `test.jpeg`: The image file to be uploaded and processed.

### Example Response

On a successful upload, the response would look like this:

```json
{
  "image_id": "123e4567-e89b-12d3-a456-426614174000",
  "public_url": "https://storage.googleapis.com/image-processing-service-ce70c.appspot.com/images/123e4567-e89b-12d3-a456-426614174000.png",
  "message": "Upload and transformation successful!"
}
```

## Testing

To run the unit tests for this service, you can use `pytest`.

### Running Tests

To execute the tests, run the following command in the root directory of the project:

```bash
pytest test/test_main.py
```

This command will discover and run all the test cases defined in the `test/test_main.py` file. You should see output indicating which tests passed or failed.

>Ensure that your database and any required services are running if your tests depend on them.

## Firebase Setup

### Step 1: Create a Firebase Project

- Go to the [Firebase Console](https://console.firebase.google.com/).
- Create a new project (or use an existing one).
- Enable Firebase Storage in the project settings.

### Step 2: Obtain Firebase Credentials

- Go to the **Project Settings** > **Service accounts**.
- Click on **Generate new private key** to download the JSON file.
- Place this JSON file in your project directory and update the path in your `.env` file.

### Step 3: Configure Firebase Storage Rules

Ensure that your Firebase Storage rules allow read and write access for testing purposes:

```plaintext
service firebase.storage {
  match /b/{bucket}/o {
    match /images/{imageId} {
      allow read, write: if request.auth != null;  // Adjust according to your security needs
    }
  }
}
```

### Note

- Adjust the security rules based on your application's authentication mechanism before deploying to production.

## Conclusion

This image processing service provides a robust and flexible way to handle image uploads and transformations, leveraging Firebase for storage. Follow the setup instructions to get started with your own instance of the service.
