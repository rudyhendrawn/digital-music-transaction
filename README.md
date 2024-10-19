# Digital Music Transaction

Digital Music Transaction is a microservice backend application using FastAPI. It consists of two main services: Read Service and Write Service.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/digital-music-transaction.git
   cd digital-music-transaction

2. **Install the dependencies:**
   ```sh
   poetry install

3. **Run the application:**
   - Run the Read Service:
   ```sh
   cd read-service
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

   - Run the Write Service:
   ```sh
   cd write-service
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
   ```

4. **API Endpoints**
	Read Service:
		- `GET /albums/{album_id}`: Retrieve a specific album by ID.
		- `GET /albums`: Retrieve a list of all albums.
	Write Service:
		- `POST /albums`: Create a new album.
		- `PUT /albums/{album_id}`: Update an existing album.
		- `DELETE /albums/{album_id}`: Delete an album.

## License
This project is licensed under the MIT License.