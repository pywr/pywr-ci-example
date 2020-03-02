""" Example Pywr model using a simple reservoir system.
"""
from pywr.model import Model
from pywr.recorders import TablesRecorder
from pywr.recorders.progress import ProgressRecorder
import click
import os
import logging
logger = logging.getLogger(__name__)

MODEL_FILENAME = 'model/thames.json'
OUT_DIR = 'outputs/'


@click.group()
def cli():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


@cli.command()
def historic_run():
    """Run the model."""
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


if __name__ == '__main__':
    cli()
