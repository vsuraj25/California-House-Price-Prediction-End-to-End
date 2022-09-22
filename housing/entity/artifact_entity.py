# TO DEFINE OUTPUT OR ARTIFACT RESULTED FROM THE PIPELINE COMPONENTS
from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtifact", ['train_file_path', 'test_file_path',
                                   'is_ingested', 'message'])