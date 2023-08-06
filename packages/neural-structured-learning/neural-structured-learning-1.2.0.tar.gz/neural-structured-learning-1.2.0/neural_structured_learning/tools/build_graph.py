# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""Program & library to build a graph from dense features (embeddings)."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import time

from absl import app
from absl import flags
from absl import logging
import numpy as np
import six
import tensorflow as tf

# Norm used if the computed norm of an embedding is less than this value.
# This value is the same as the default for tf.math.l2_normalize.
_MIN_NORM = np.float64(1e-6)


def _read_tfrecord_examples(filenames, id_feature_name, embedding_feature_name):
  """Reads and returns the embeddings stored in the Examples in `filename`.

  Args:
    filenames: A list of names of TFRecord files containing `tf.train.Example`
      objects.
    id_feature_name: Name of the feature that identifies the Example's ID.
    embedding_feature_name: Name of the feature that identifies the Example's
        embedding.

  Returns:
    A dict mapping each instance ID to its L2-normalized embedding, represented
    by a 1-D numpy.ndarray. The ID is expected to be contained in the singleton
    bytes_list feature named by 'id_feature_name', and the embedding is
    expected to be contained in the float_list feature named by
    'embedding_feature_name'.
  """
  def parse_tf_record_examples(filename):
    """Generator that returns the tensorflow.Examples in `filename`.

    Args:
      filename: Name of the TFRecord file containing tensorflow.Examples.

    Yields:
      The tensorflow.Examples contained in the file.
    """
    for raw_record in tf.data.TFRecordDataset([filename]):
      example = tf.train.Example()
      example.ParseFromString(raw_record.numpy())
      yield example

  def l2_normalize(v):
    """Returns the L2-norm of the vector `v`.

    Args:
      v: A 1-D vector (either a list or numpy array).

    Returns:
      The L2-normalized version of `v`. The result will have an L2-norm of 1.0.
    """
    l2_norm = np.linalg.norm(v)
    return v / max(l2_norm, _MIN_NORM)

  embeddings = {}
  for filename in filenames:
    start_time = time.time()
    logging.info('Reading tf.train.Examples from TFRecord file: %s...',
                 filename)
    for tf_example in parse_tf_record_examples(filename):
      f_map = tf_example.features.feature
      if id_feature_name not in f_map:
        logging.error('No feature named "%s" found in input Example: %s',
                      id_feature_name, tf_example.ShortDebugString())
        continue
      ex_id = f_map[id_feature_name].bytes_list.value[0].decode('utf-8')
      if embedding_feature_name not in f_map:
        logging.error('No feature named "%s" found in input with ID "%s"',
                      embedding_feature_name, ex_id)
        continue
      embedding_list = f_map[embedding_feature_name].float_list.value
      embeddings[ex_id] = l2_normalize(embedding_list)
    logging.info('Done reading %d tf.train.Examples from: %s (%.2f seconds).',
                 len(embeddings), filename, (time.time() - start_time))
  return embeddings


def _write_edges(embeddings, threshold, f):
  """Writes relevant edges to `f` among pairs of the given `embeddings`.

  This function considers all distinct pairs of nodes in `embeddings`,
  computes the dot product between all such pairs, and writes any edge to `f`
  for which the similarity is at least the given `threshold`.

  Args:
    embeddings: A `dict`: node_id -> embedding.
    threshold: A `float` representing an inclusive lower-bound on the cosine
        similarity for an edge to be added.
    f: A file object to which all edges are written in TSV format. The caller is
        responsible for opening and closing this file.

  Returns:
    The number of bi-direction edges written to the file.
  """
  start_time = time.time()
  edge_cnt = 0
  all_combos = itertools.combinations(six.iteritems(embeddings), 2)
  for (i, emb_i), (j, emb_j) in all_combos:
    weight = np.dot(emb_i, emb_j)
    if weight >= threshold:
      f.write('%s\t%s\t%f\n' % (i, j, weight))
      f.write('%s\t%s\t%f\n' % (j, i, weight))
      edge_cnt += 1
      if (edge_cnt % 1000000) == 0:
        logging.info('Wrote %d edges in %.2f seconds....', edge_cnt,
                     (time.time() - start_time))

  return edge_cnt


def build_graph(embedding_files,
                output_graph_path,
                similarity_threshold=0.8,
                id_feature_name='id',
                embedding_feature_name='embedding'):
  """Builds a graph based on dense embeddings and persists it in TSV format.

  This function reads input instances from one or more TFRecord files, each
  containing `tf.train.Example` protos. Each input example is expected to
  contain at least the following 2 features:

  *   `id`: A singleton `bytes_list` feature that identifies each example.
  *   `embedding`: A `float_list` feature that contains the (dense) embedding of
       each example.

  `id` and `embedding` are not necessarily the literal feature names; if your
  features have different names, you can specify them using the
  `id_feature_name` and `embedding_feature_name` arguments, respectively.

  This function then computes the cosine similarity between all pairs of input
  examples based on their associated embeddings. An edge is written to the TSV
  file named by `output_graph_path` for each pair whose similarity is at least
  as large as `similarity_threshold`. Each output edge is represented by a TSV
  line in the `output_graph_path` file with the following form:

  ```
  source_id<TAB>target_id<TAB>edge_weight
  ```

  All edges in the output will be symmetric (i.e., if edge `A--w-->B` exists in
  the output, then so will edge `B--w-->A`).

  Note that this function can also be invoked as a binary from a shell. Sample
  usage:

  `python -m neural_structured_learning.tools.build_graph` [*flags*]
  *embedding_file.tfr... output_graph.tsv*

  For details about this program's flags, run:

  ```
  python -m neural_structured_learning.tools.build_graph --help
  ```

  Args:
    embedding_files: A list of names of TFRecord files containing
      `tf.train.Example` objects, which in turn contain dense embeddings.
    output_graph_path: Name of the file to which the output graph in TSV format
      should be written.
    similarity_threshold: Threshold used to determine which edges to retain in
      the resulting graph.
    id_feature_name: The name of the feature in the input `tf.train.Example`
      objects representing the ID of examples.
    embedding_feature_name: The name of the feature in the input
      `tf.train.Example` objects representing the embedding of examples.
  """
  embeddings = _read_tfrecord_examples(embedding_files, id_feature_name,
                                       embedding_feature_name)
  start_time = time.time()
  logging.info('Building graph and writing edges to TSV file: %s',
               output_graph_path)
  with open(output_graph_path, 'w') as f:
    edge_cnt = _write_edges(embeddings, similarity_threshold, f)
    logging.info(
        'Wrote graph containing %d bi-directional edges (%.2f seconds).',
        edge_cnt, (time.time() - start_time))


def _main(argv):
  """Main function for invoking the `nsl.tools.build_graph` function."""
  flag = flags.FLAGS
  flag.showprefixforinfo = False
  if len(argv) < 3:
    raise app.UsageError(
        'Invalid number of arguments; expected 2 or more, got %d' %
        (len(argv) - 1))

  build_graph(argv[1:-1], argv[-1], flag.similarity_threshold,
              flag.id_feature_name, flag.embedding_feature_name)


if __name__ == '__main__':
  flags.DEFINE_string(
      'id_feature_name', 'id',
      """Name of the singleton bytes_list feature in each input Example
      whose value is the Example's ID.""")
  flags.DEFINE_string(
      'embedding_feature_name', 'embedding',
      """Name of the float_list feature in each input Example
      whose value is the Example's (dense) embedding.""")
  flags.DEFINE_float(
      'similarity_threshold', 0.8,
      """Lower bound on the cosine similarity required for an edge
      to be created between two nodes.""")

  # Ensure TF 2.0 behavior even if TF 1.X is installed.
  tf.compat.v1.enable_v2_behavior()
  app.run(_main)
