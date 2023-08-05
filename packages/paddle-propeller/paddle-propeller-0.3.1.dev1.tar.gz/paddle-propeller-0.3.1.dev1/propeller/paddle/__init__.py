#   Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
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
"""
doc
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
import logging

log = logging.getLogger(__name__)


def enable_textone():
    try:
        import textone
    except ImportError:
        log.fatal('enable textone failed: textone not found!')
        raise
    global textone_enabled
    log.info('textone enabled')
    from propeller.paddle.train.monitored_executor import MonitoredExecutor, TextoneTrainer
    if TextoneTrainer is None:
        raise RuntimeError('enable textone failed: textone not found!')
    MonitoredExecutor.saver_class = TextoneTrainer


from propeller.types import *
from propeller.util import ArgumentParser, parse_hparam, parse_runconfig, parse_file

from propeller.paddle import data
from propeller.paddle import train
from propeller.paddle.train import *
