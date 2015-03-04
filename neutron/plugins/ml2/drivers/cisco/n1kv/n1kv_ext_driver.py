# Copyright (c) 2014 Cisco Systems
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Extenions Driver for Cisco Nexus1000V."""

from oslo.config import cfg

from neutron.api import extensions as api_extensions
from neutron.api.v2 import attributes
from neutron.openstack.common import excutils
from neutron.openstack.common.gettextutils import _LE
from neutron.openstack.common import log
from neutron.openstack.common import uuidutils
from neutron.plugins.ml2.common import exceptions as ml2_exc
from neutron.plugins.ml2 import driver_api as api
from neutron.plugins.ml2.drivers.cisco.n1kv import constants
from neutron.plugins.ml2.drivers.cisco.n1kv import exceptions as n1kv_exc
from neutron.plugins.ml2.drivers.cisco.n1kv import extensions
from neutron.plugins.ml2.drivers.cisco.n1kv import n1kv_db

LOG = log.getLogger(__name__)


class CiscoN1kvExtensionDriver(api.ExtensionDriver):
    """Cisco N1KV ML2 Extension Driver."""

    # List of supported extensions for cisco Nexus1000V.
    _supported_extension_alias = "n1kv"

    def initialize(self):
        api_extensions.append_api_extensions_path(extensions.__path__)

    @property
    def extension_alias(self):
        """Supported extension alias.

        Return the alias identifying the core API extension supported
        by this driver.
        """
        return self._supported_extension_alias

    def process_create_port(self, session, data, result):
        port_id = result.get('id')
        policy_profile_attr = data.get(constants.N1KV_PROFILE)
        if not attributes.is_attr_set(policy_profile_attr):
            policy_profile_attr = (cfg.CONF.ml2_cisco_n1kv.
                                   default_policy_profile)
        try:
            n1kv_db.get_policy_binding(port_id, session)
        except n1kv_exc.PortBindingNotFound:
            if not uuidutils.is_uuid_like(policy_profile_attr):
                policy_profile = n1kv_db.get_policy_profile_by_name(
                    policy_profile_attr)
                if policy_profile:
                    policy_profile_attr = policy_profile.id
                else:
                    LOG.error(_LE("Policy Profile %(profile)s does "
                                  "not exist."),
                              {"profile": policy_profile_attr})
                    raise ml2_exc.MechanismDriverError()
            elif not n1kv_db.get_policy_profile_by_uuid(session,
                                                        policy_profile_attr):
                LOG.error(_LE("Policy Profile %(profile)s does not exist."),
                          {"profile": policy_profile_attr})
                raise ml2_exc.MechanismDriverError()
            n1kv_db.add_policy_binding(port_id, policy_profile_attr, session)
        result[constants.N1KV_PROFILE] = policy_profile_attr

    def extend_port_dict(self, session, result):
        port_id = result.get('id')
        try:
            res = n1kv_db.get_policy_binding(port_id, session)
        except n1kv_exc.PortBindingNotFound:
            res = None
        if res:
            result[constants.N1KV_PROFILE] = res.profile_id
