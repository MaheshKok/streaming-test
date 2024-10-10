# gainzai_assignment

This project was generated using fastapi_template.

A Working Demo of this app can be found here:
https://www.loom.com/share/6286460092384496bafb973de460507a

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

# GainzAI Assignment

## Frontend

The frontend code is located in the `gainz_assignment_fe` directory.

### Prerequisites

- **Node.js**: Ensure you have Node.js installed on your machine. You can download it from [Node.js Official Website](https://nodejs.org/).

### Installation and Setup

1. **Navigate to the Frontend Directory**

   Open your terminal or command prompt and navigate to the frontend directory:

   ```bash
   cd gainz_assignment_fe
   ```

2. **Install Dependencies**

   Install the necessary Node.js packages by running:

   ```bash
   npm install
   ```

3. **Start the Development Server**

   Launch the frontend development server with the following command:

   ```bash
   npm start
   ```

4. **Access the Application**

   Once the server is running, open your web browser and navigate to:

   [http://localhost:3000](http://localhost:3000)

   Your application should now be up and running!

### Additional Scripts

Here are some additional scripts you might find useful:

- **Build for Production**

  To build the app for production, run:

  ```bash
  npm run build
  ```

  This will create an optimized production build in the `build` folder.

- **Run Tests**

  To execute tests, use:

  ```bash
  npm test
  ```

- **Eject Configuration**

  **Note:** This is a one-way operation. Once you eject, you can't go back!

  To eject the configuration, run:

  ```bash
  npm run eject
  ```

### Troubleshooting

- **Port Already in Use**

  If you encounter an error indicating that port `3000` is already in use, you can specify a different port by setting the `PORT` environment variable:

  ```bash
  PORT=3001 npm start
  ```

- **Missing Dependencies**

  If you run into issues related to missing packages, try reinstalling the dependencies:

  ```bash
  npm install --force
  ```

### Useful Links

- [Create React App Documentation](https://create-react-app.dev/docs/getting-started/)
- [Material-UI (MUI) Documentation](https://mui.com/getting-started/installation/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)

---

Feel free to reach out if you encounter any issues or have questions regarding the setup!

```bash
poetry install
poetry run python -m gainzai_assignment
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker-compose up --build
```

If you want to develop in docker with autoreload and exposed ports add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose build
```

## Project structure

```bash
$ tree "gainzai_assignment"
gainzai_assignment/
├── gainz_assignment_fe/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   └── Assistant.js
│   │   ├── services/
│   │   │   └── WebSocketManager.js
│   │   ├── theme.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   ├── package-lock.json
│   └── .env
├── web/
│   ├── static/
│   │   └── assistant_index.html
│   ├── templates/
│   │   └── build/
│   │       └── index.html
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
│   ├── urls.py
│   └── views.py
├── README.md
└── ... (other project files)
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here. 

All environment variables should start with "GAINZAI_ASSIGNMENT_" prefix.

For example if you see in your "gainzai_assignment/settings.py" a variable named like
`random_parameter`, you should provide the "GAINZAI_ASSIGNMENT_RANDOM_PARAMETER" 
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `gainzai_assignment.settings.Settings.Config`.

An example of .env file:
```bash
GAINZAI_ASSIGNMENT_RELOAD="True"
GAINZAI_ASSIGNMENT_PORT="8000"
GAINZAI_ASSIGNMENT_ENVIRONMENT="dev"
GAINZAI_ASSIGMENT_OPENAI_KEY="open-api-key"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/
## OpenTelemetry 

If you want to start your project with OpenTelemetry collector 
you can add `-f ./deploy/docker-compose.otlp.yml` to your docker command.

Like this:

```bash
docker-compose -f docker-compose.yml -f deploy/docker-compose.otlp.yml --project-directory . up
```

This command will start OpenTelemetry collector and jaeger. 
After sending a requests you can see traces in jaeger's UI
at http://localhost:16686/.

This docker configuration is not supposed to be used in production. 
It's only for demo purpose.

You can read more about OpenTelemetry here: https://opentelemetry.io/

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* ruff (spots possible bugs);


You can read more about pre-commit here: https://pre-commit.com/

## Migrations

If you want to migrate your database, you should run following commands:
```bash
# To run all migrations until the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

### Reverting migrations

If you want to revert migrations, you should run:
```bash
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
```

### Migration generation

To generate migrations you should run:
```bash
# For automatic change detection.
alembic revision --autogenerate

# For empty file generation.
alembic revision
```


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose run --build --rm api pytest -vv .
docker-compose down
```

For running tests on your local machine.
1. you need to start a database.

I prefer doing it with docker:
```
docker run -p "5432:5432" -e "POSTGRES_PASSWORD=gainzai_assignment" -e "POSTGRES_USER=gainzai_assignment" -e "POSTGRES_DB=gainzai_assignment" postgres:16.3-bullseye
```


2. Run the pytest.
```bash
pytest -vv .
```
