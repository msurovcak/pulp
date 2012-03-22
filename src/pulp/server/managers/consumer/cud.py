# -*- coding: utf-8 -*-
#
# Copyright © 2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

"""
Contains manager class and exceptions for operations surrounding the creation,
removal, and update on a consumer.
"""

import logging
import re
import sys

from pulp.server import config
from pulp.common.bundle import Bundle
import pulp.server.auth.cert_generator as cert_generator

from pulp.server.db.model.gc_consumer import Consumer
from pulp.server.managers import factory
from pulp.server.exceptions import DuplicateResource, InvalidValue, \
    MissingResource, PulpExecutionException

# -- constants ----------------------------------------------------------------

_CONSUMER_ID_REGEX = re.compile(r'^[\-_A-Za-z0-9]+$') # letters, numbers, underscore, hyphen

_LOG = logging.getLogger(__name__)

# -- manager ------------------------------------------------------------------

class ConsumerManager(object):
    """
    Performs consumer related CRUD operations
    """

    def register(self, id, display_name=None, description=None, notes=None, capabilities=None):
        """
        Registers a new Consumer

        @param id: unique identifier for the consumer
        @type  id: str

        @param display_name: user-friendly name for the consumer
        @type  display_name: str

        @param description: user-friendly text describing the consumer
        @type  description: str

        @param notes: key-value pairs to programmatically tag the consumer
        @type  notes: dict

        @param capabilities:
        @type capabilities:

        @raises DuplicateResource: if there is already a consumer or a used with the requested ID
        @raises InvalidValue: if any of the fields is unacceptable
        """
        if not is_consumer_id_valid(id):
            raise InvalidValue(id)

        existing_consumer = Consumer.get_collection().find_one({'id' : id})
        if existing_consumer is not None:
            raise DuplicateResource(id)

        if notes is not None and not isinstance(notes, dict):
            raise InvalidValue(notes)

        if capabilities is not None and not isinstance(capabilities, dict):
            raise InvalidValue(capabilities)

        # Use the ID for the display name if one was not specified
        display_name = display_name or id

        # Generate certificate
        expiration_date = config.config.getint('security', 'consumer_cert_expiration')
        key, crt = cert_generator.make_cert(id, expiration_date)

        # Creation
        create_me = Consumer(id, display_name, description, notes, capabilities, certificate=crt.strip())
        Consumer.get_collection().save(create_me, safe=True)

#        self.consumer_history_api.consumer_registered(c.id)

        create_me.certificate = Bundle.join(key, crt)
        return create_me


    def unregister(self, id):
        """
        Unregisters given consumer.

        @param id: identifies the consumer being unregistered
        @type  id: str

        @raises MissingResource: if the given consumer does not exist
        @raises OperationFailed: if any part of the unregister process fails;
                the exception will contain information on which sections failed
        """

        consumer_coll = Consumer.get_collection()

        consumer = consumer_coll.find_one({'id' : id})
        if consumer is None:
            raise MissingResource(id)
        
        manager = factory.consumer_bind_manager()
        manager.consumer_deleted(id)

        # To do - Update consumergroups after we add consumergroup support in V2

        # To do - notify agent

        # Database Updates
        try:
            Consumer.get_collection().remove({'id' : id}, safe=True)
        except Exception:
            _LOG.exception('Error updating database collection while removing consumer [%s]' % id)
            raise PulpExecutionException("database-error"), None, sys.exc_info()[2]

#        self.consumer_history_api.consumer_unregistered(id)

    def update(self, id, delta):
        """
        Updates metadata about the given consumer. Only the following
        fields may be updated through this call:
        * display_name
        * description

        Other fields found in delta will be ignored.

        @param repo_id: identifies the consumer
        @type  repo_id: str

        @param delta: list of attributes and their new values to change
        @type  delta: dict

        @raises MissingResource: if there is no consumer with given id
        """
        consumer_coll = Consumer.get_collection()

        consumer = consumer_coll.find_one({'id' : id})
        if consumer is None:
            raise MissingResource(id)

        if 'display_name' in delta:
            consumer['display_name'] = delta['display_name']

        if 'description' in delta:
            consumer['description'] = delta['description']

        consumer_coll.save(consumer, safe=True)

        return consumer

# -- functions ----------------------------------------------------------------

def is_consumer_id_valid(id):
    """
    @return: true if the consumer ID is valid; false otherwise
    @rtype:  bool
    """
    result = _CONSUMER_ID_REGEX.match(id) is not None
    return result
