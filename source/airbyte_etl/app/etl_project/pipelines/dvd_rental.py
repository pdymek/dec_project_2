from jinja2 import Environment, FileSystemLoader
from etl_project.connectors.postgresql import PostgreSqlClient
from etl_project.connectors.airbyte import AirbyteClient
from dotenv import load_dotenv
import os 
from etl_project.assets.extract_load_transform import extract_load, transform, SqlTransform
from graphlib import TopologicalSorter
from etl_project.assets.pipeline_logging import PipelineLogging
from etl_project.assets.metadata_logging import MetaDataLogging, MetaDataLoggingStatus
from sqlalchemy.exc import SQLAlchemyError

if __name__ == "__main__":
    load_dotenv()
    LOGGING_SERVER_NAME = os.environ.get("LOGGING_SERVER_NAME")
    LOGGING_DATABASE_NAME = os.environ.get("LOGGING_DATABASE_NAME")
    LOGGING_USERNAME = os.environ.get("LOGGING_USERNAME")
    LOGGING_PASSWORD = os.environ.get("LOGGING_PASSWORD")
    LOGGING_PORT = os.environ.get("LOGGING_PORT")

    postgresql_logging_client = PostgreSqlClient(
        server_name=LOGGING_SERVER_NAME,
        database_name=LOGGING_DATABASE_NAME,
        username=LOGGING_USERNAME,
        password=LOGGING_PASSWORD,
        port=LOGGING_PORT
    )

    metadata_logging = MetaDataLogging(pipeline_name="dvd_rental", postgresql_client=postgresql_logging_client)
    pipeline_logging = PipelineLogging(pipeline_name="dvd_rental", log_folder_path="etl_project/logs")

    TARGET_DATABASE_NAME = os.environ.get("TARGET_DATABASE_NAME")
    TARGET_SERVER_NAME = os.environ.get("TARGET_SERVER_NAME")
    TARGET_DB_USERNAME = os.environ.get("TARGET_DB_USERNAME")
    TARGET_DB_PASSWORD = os.environ.get("TARGET_DB_PASSWORD")
    TARGET_PORT = os.environ.get("TARGET_PORT")
    AIRBYTE_USERNAME = os.environ.get("AIRBYTE_USERNAME")
    AIRBYTE_PASSWORD = os.environ.get("AIRBYTE_PASSWORD")
    AIRBYTE_SERVER_NAME = os.environ.get("AIRBYTE_SERVER_NAME")

    try:
        metadata_logging.log() # start run
        pipeline_logging.logger.info("Creating target client")
        target_postgresql_client = PostgreSqlClient(
            server_name=TARGET_SERVER_NAME, 
            database_name=TARGET_DATABASE_NAME,
            username=TARGET_DB_USERNAME,
            password=TARGET_DB_PASSWORD,
            port=TARGET_PORT
        )
        airbyte_client = AirbyteClient(server_name=AIRBYTE_SERVER_NAME, username=AIRBYTE_USERNAME, password=AIRBYTE_PASSWORD)
        if airbyte_client.valid_connection(): 
            airbyte_client.trigger_sync(connection_id="fb01d4c8-2be7-433e-8b7c-5875b2685c8")
        
        transform_template_environment = Environment(loader=FileSystemLoader("etl_project/assets/sql/transform"))
        
        # create nodes
        
        dim_films = SqlTransform(table_name="dim_films", postgresql_client=target_postgresql_client, environment=transform_template_environment)
        dim_dates = SqlTransform(table_name="dim_dates", postgresql_client=target_postgresql_client, environment=transform_template_environment)
        dim_customers = SqlTransform(table_name="dim_customers", postgresql_client=target_postgresql_client, environment=transform_template_environment)
        fact_rental = SqlTransform(table_name="fact_rental", postgresql_client=target_postgresql_client, environment=transform_template_environment)
        report_monthly_cumulative_amount_by_country = SqlTransform(table_name="report_monthly_cumulative_amount_by_country", postgresql_client=target_postgresql_client, environment=transform_template_environment)
        report_top_10_rented_films = SqlTransform(table_name="report_top_10_rented_films", postgresql_client=target_postgresql_client, environment=transform_template_environment)
        report_films_rented_more_than_20_times = SqlTransform(table_name="report_films_rented_more_than_20_times", postgresql_client=target_postgresql_client, environment=transform_template_environment)
        # create DAG 
        dag = TopologicalSorter()
        dag.add(dim_films)
        dag.add(dim_dates)
        dag.add(dim_customers)
        dag.add(fact_rental)
        dag.add(report_monthly_cumulative_amount_by_country, fact_rental, dim_dates, dim_customers)
        dag.add(report_top_10_rented_films, fact_rental, dim_films)
        dag.add(report_films_rented_more_than_20_times, fact_rental, dim_films)

        # run transform 
        pipeline_logging.logger.info("Perform transform")
        transform(dag=dag)
        pipeline_logging.logger.info("Pipeline complete")
        metadata_logging.log(status=MetaDataLoggingStatus.RUN_SUCCESS, logs=pipeline_logging.get_logs()) 
        pipeline_logging.logger.handlers.clear()
    except SQLAlchemyError as e:
        pipeline_logging.logger.error(f"Pipeline failed with exception {e}")
        metadata_logging.log(status=MetaDataLoggingStatus.RUN_FAILURE, logs=pipeline_logging.get_logs()) 
        pipeline_logging.logger.handlers.clear()
