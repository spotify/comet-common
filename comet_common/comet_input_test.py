# Copyright 2018 Spotify AB. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines something"""
import time
from concurrent.futures import ThreadPoolExecutor

from comet_core.plugin_interface import CometInput


class TestInput(CometInput):
    """PubSub input

    Args:
        message_callback (function): the function to call with incoming messages
    """
    def __init__(self, message_callback):
        super().__init__(message_callback)

        self.running = True
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.executor.submit(self.run)

    def run(self):
        """
        Generate test messages
        """
        while self.running:
            self.message_callback('random', '{}')
            time.sleep(1)

    def stop(self):
        self.running = False
        self.executor.shutdown()
