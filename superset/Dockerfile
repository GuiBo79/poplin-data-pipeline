FROM apache/superset:latest

# Install PostgreSQL CLI for database operations
USER root
RUN pip install psycopg2-binary
RUN apt-get update && apt-get install -y postgresql-client && apt-get clean
RUN pip install pillow

# Switch back to the Superset user
USER superset
