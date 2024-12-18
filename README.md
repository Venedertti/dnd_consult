
# DnD Consult API
The DnD Consult API is a Flask-based application that manages RPG spells, integrated with a PostgreSQL database.
The project leverages Docker for easy setup and dependency management.

## 📁 Project Structure

```
app.py
docker-compose.yml
rsc/
  └── DnD Consult.postman_collection.json
scripts/
  └── start_dev_env.bat
  └── update_web_container.bat
src/
  ├── Dockerfile
  ├── __init__.py
  ├── controller/
  ├── database/
  └── service/
```

## 🚀 How to Initialize the Project
### Prerequisites:
- Docker and Docker Compose installed.
- Python 3.12 installed (if running locally without Docker).

### Steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Venedertti/dnd_consult.git
   cd .../dnd_consult
   ```

2. Start the containers with Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the API at [http://localhost:5000](http://localhost:5000).

## 🔄 Update the Project (Rebuild the Web Image)
Run the `update_web_container.bat` script to rebuild the web container without deleting the database or Adminer data:
```bash
scripts\update_web_container.bat
```

## 🚀 Start the Developer Project
Run the `start_dev_env.bat` script to create and activate a virtual environment, install the dependencies from `requirements.txt`, and display the installed libraries:
```bash
scripts\start_dev_env.bat
```

This script performs the following steps:

- Creates a virtual environment in the `.venv` directory.
- Waits for 10 seconds to ensure the virtual environment is created properly.
- Activates the virtual environment.
- Installs the dependencies from the `requirements.txt` file.
- Displays the list of installed libraries with `pip freeze`.
- Pauses the terminal to allow you to review the output.

## 📚 API Endpoints

1. **Create a new spell**  
   **Route:** POST `/spells/create`  
   **Payload:**
   ```json
   {
       "name": "Fireball",
       "level": 3,
       "school": "Evocation",
       "casting_time": "1 action",
       "range": "150 feet",
       "components": "V, S, M",
       "duration": "Instantaneous",
       "description": "A bright streak...",
       "classes": ["Wizard", "Sorcerer"],
       "source": "PHB"
   }
   ```
   **Response:**
   ```json
   {
       "message": "Spell created with id: 1"
   }
   ```

2. **Retrieve all spells**  
   **Route:** GET `/spells/getAll`  
   **Response:**
   ```json
   [
       {
           "id": 1,
           "name": "Fireball",
           "level": 3,
           "school": "Evocation"
       }
   ]
   ```

3. **Retrieve spell by ID**  
   **Route:** GET `/spells/get/<id>`  
   **Response:**
   ```json
   {
       "id": 1,
       "name": "Fireball",
       "level": 3,
       "school": "Evocation",
       "castingTime": "1 action",
       "range": "150 feet",
       "components": "V, S, M",
       "duration": "Instantaneous",
       "description": "A bright streak...",
       "classes": [
           {"name": "Wizard", "type": "Magical", "source": "PHB"}
       ]
   }
   ```

4. **Find spells by name**  
   **Route:** GET `/spells/findAllByName?name=Fireball`  
   **Response:**
   ```json
   [
       {
           "id": 1,
           "name": "Fireball",
           "level": 3,
           "school": "Evocation",
           "description": "A bright streak...",
           "classes": [{"name": "Wizard", "type": "Magical", "source": "PHB"}]
       }
   ]
   ```

5. **Update a spell**  
   **Route:** PUT `/spells/update/<id>`  
   **Payload:**
   ```json
   {
       "name": "Fireball Updated",
       "level": 4,
       "school": "Evocation",
       "classes": ["Sorcerer"]
   }
   ```
   **Response:**
   ```json
   {
       "id": 1,
       "name": "Fireball Updated",
       "level": 4,
       "school": "Evocation"
   }
   ```

6. **Delete a spell**  
   **Route:** DELETE `/spells/delete/<id>`  
   **Response:**
   ```json
   {
       "message": "Spell deleted"
   }
   ```

7. **Bulk Import from Open5E Source**  
   **Route:** POST `/dnd/import/<string:source>`  
   **Request Parameters:**
   - **source (path parameter):** The name of the external data source (e.g., Open5E_SDR).

   **Description:**
   - Starts a new import process for the specified source.
   - Creates a new process entry in the system.
   - The import operation is performed asynchronously in a separate thread to avoid blocking the main thread.

   **Response:**
   ```json
   {
       "message": "Process started",
       "process_id": "96349075-b0e0-4fdc-9e29-bc8444440a58"
   }
   ```
   
8. **Monitor Bulk Import Status**  
   **Route:** GET `/monitor/<string:process_id>`  
   **Request Parameters:**
   - **process_id (path parameter):** The unique identifier of the import process.

   **Description:**
   - Retrieves the status of the import process by querying the system using the given process_id.
   - Returns information such as whether the process is still ongoing, completed, or encountered an error.

   **Response:**
   ```json
   {
       "status": "completed",
       "message": "Import process completed successfully"
   }



## 🛠️ Included Tools
- **Adminer:** Access the database using the browser at [http://localhost:8080](http://localhost:8080).
- **Postman Collection:** `rsc/DnD Consult.postman_collection.json`

## ⚙️ Environment Variables
Environment variables are defined in the `docker-compose.yml` file:

| Variable                    | Default Value                                                |
| --------------------------- | ------------------------------------------------------------ |
| PORT                        | 5000                                                         |
| FLASK_APP                   | app.py                                                       |
| FLASK_ENV                   | development                                                  |
| SQLALCHEMY_DATABASE_URI     | postgresql://root:ImRoot_2024@db:5432/dnd_consult            |

## 🐳 Docker Containers
- **web:** Flask application running on port 5000.
- **db:** PostgreSQL database initialized via `init.sql`.
- **adminer:** Database management interface accessible at port 8080.

## 📦 Start/Stop the Project
- **Build the project:**
  ```bash
  docker-compose up --build
  ```

- **Start the project:**
  ```bash
  docker-compose start
  ```

- **Stop the project:**
  ```bash
  docker-compose down
  ```

- **Stop and remove volumes (delete database data):**
  ```bash
  docker-compose down -v
  ```

## ✅ Testing the Endpoints
Use Postman by importing:
```bash
rsc/DnD Consult.postman_collection.json
```

Or test using curl:
```bash
curl -X GET "http://localhost:5000/spells/getAll"
```

## 📝 Notes
- Ensure Docker is running before starting the project.
- Use the `update_web_container.bat` script to quickly rebuild the web container without losing data.
