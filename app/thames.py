""" Example Pywr model using a simple reservoir system.
"""
from pywr.model import Model
from pywr.recorders import TablesRecorder
from pywr.recorders.progress import ProgressRecorder
from azure.storage.blob import BlobServiceClient
import click
import os
import logging
logger = logging.getLogger(__name__)

MODEL_FILENAME = 'model/thames.json'
OUT_DIR = 'outputs/'
DATA_DIR = 'data/'


@click.group()
def cli():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


@cli.command()
def historic_run():
    """Run the model."""
    logger.info('Initialising cloud storage client ...')
    client = init_azure_storage()
    download_hydrology(client)
    logger.info('Starting model run ...')
    # Run the model
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    model = Model.load(MODEL_FILENAME)
    # Add a storage recorder
    TablesRecorder(model, os.path.join(OUT_DIR, 'thames_output.h5'), parameters=[p for p in model.parameters])
    ProgressRecorder(model)

    # Run the model
    stats = model.run()
    logger.info(stats)
    stats_df = stats.to_dataframe()
    logger.info(stats_df)


def download_hydrology(blob_service_client: BlobServiceClient):
    """Download the hydrology data"""

    filename = 'thames_stochastic_flow.gz'
    version = 'v1.0.0'
    download_file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    # Create a blob client using the local file name as the name for the blob
    blob_path = f'hydrology/ref/{version}/{filename}'
    blob_client = blob_service_client.get_blob_client(container='data', blob=blob_path)

    logger.info(f'Downloading hydrology data from:\n  "{blob_path}"\nto:\n  "{download_file_path}"')
    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())


def init_azure_storage() -> BlobServiceClient:
    connect_str = os.getenv('AZURE_BLOB_CONNECT_STR')
    return BlobServiceClient.from_connection_string(connect_str)


if __name__ == '__main__':
    cli()
