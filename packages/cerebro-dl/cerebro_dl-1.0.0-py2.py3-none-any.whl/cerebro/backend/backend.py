# Copyright 2020 Supun Nakandala, Yuhao Zhang, and Arun Kumar. All Rights Reserved.
# Copyright 2019 Uber Technologies, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import


class Backend(object):
    """Interface for remote execution of the distributed training function.

    A custom backend can be used in cases where the training environment running Cerebro is different
    from the Spark application running the CerebroEstimator.
    """

    def _num_workers(self):
        """Returns the number of workers to use for training."""
        raise NotImplementedError()

    def initialize_workers(self):
        """Initialize workers"""
        raise NotImplementedError()

    def initialize_data_loaders(self, store, dataset_idx, schema_fields):
        """Initialize data loaders"""
        raise NotImplementedError()

    def train_for_one_epoch(self, models, store, dataset_idx, feature_col, label_col, is_train=True):
        """
        Takes a set of Keras models and trains for one epoch. If is_train is False, validation is performed
         instead of training.
        :param models:
        :param store:
        :param dataset_idx:
        :param feature_col:
        :param label_col:
        :param is_train:
        """
        raise NotImplementedError()

    def teardown_workers(self):
        """Teardown workers"""
        raise NotImplementedError()

    def prepare_data(self, store, dataset, validation, label_columns=['label'], feature_columns=['features'],
                     compress_sparse=False, verbose=2):
        """
        Prepare data by writing out into persistent storage
        :param store:
        :param dataset:
        :param validation:
        :param label_columns:
        :param feature_columns:
        :param compress_sparse:
        :param verbose:
        """
        raise NotImplementedError()

    def get_metadata_from_parquet(self, store, label_columns=['label'], feature_columns=['features']):
        """
        Get metadata from existing data in the persistent storage
        :param store:
        :param label_columns:
        :param feature_columns:
        """
        raise NotImplementedError()