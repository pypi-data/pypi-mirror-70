
# AUTO-GENERATED file from IFMapApiGenerator. Do Not Edit!

from builtins import str
from builtins import range
from contrail_heat.resources import contrail
try:
    from heat.common.i18n import _
except ImportError:
    pass
from heat.engine import attributes
from heat.engine import constraints
from heat.engine import properties
try:
    from heat.openstack.common import log as logging
except ImportError:
    from oslo_log import log as logging
import uuid

from vnc_api import vnc_api

LOG = logging.getLogger(__name__)


class ContrailDsaRule(contrail.ContrailResource):
    PROPERTIES = (
        NAME, FQ_NAME, DSA_RULE_ENTRY, DSA_RULE_ENTRY_PUBLISHER, DSA_RULE_ENTRY_PUBLISHER_EP_TYPE, DSA_RULE_ENTRY_PUBLISHER_EP_ID, DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX, DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX, DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX_LEN, DSA_RULE_ENTRY_PUBLISHER_EP_VERSION, DSA_RULE_ENTRY_SUBSCRIBER, DSA_RULE_ENTRY_SUBSCRIBER_EP_TYPE, DSA_RULE_ENTRY_SUBSCRIBER_EP_ID, DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX, DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX, DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX_LEN, DSA_RULE_ENTRY_SUBSCRIBER_EP_VERSION, ID_PERMS, ID_PERMS_PERMISSIONS, ID_PERMS_PERMISSIONS_OWNER, ID_PERMS_PERMISSIONS_OWNER_ACCESS, ID_PERMS_PERMISSIONS_GROUP, ID_PERMS_PERMISSIONS_GROUP_ACCESS, ID_PERMS_PERMISSIONS_OTHER_ACCESS, ID_PERMS_UUID, ID_PERMS_UUID_UUID_MSLONG, ID_PERMS_UUID_UUID_LSLONG, ID_PERMS_ENABLE, ID_PERMS_CREATED, ID_PERMS_LAST_MODIFIED, ID_PERMS_DESCRIPTION, ID_PERMS_USER_VISIBLE, ID_PERMS_CREATOR, DISPLAY_NAME, ANNOTATIONS, ANNOTATIONS_KEY_VALUE_PAIR, ANNOTATIONS_KEY_VALUE_PAIR_KEY, ANNOTATIONS_KEY_VALUE_PAIR_VALUE, PERMS2, PERMS2_OWNER, PERMS2_OWNER_ACCESS, PERMS2_GLOBAL_ACCESS, PERMS2_SHARE, PERMS2_SHARE_TENANT, PERMS2_SHARE_TENANT_ACCESS, TAG_REFS, DISCOVERY_SERVICE_ASSIGNMENT
    ) = (
        'name', 'fq_name', 'dsa_rule_entry', 'dsa_rule_entry_publisher', 'dsa_rule_entry_publisher_ep_type', 'dsa_rule_entry_publisher_ep_id', 'dsa_rule_entry_publisher_ep_prefix', 'dsa_rule_entry_publisher_ep_prefix_ip_prefix', 'dsa_rule_entry_publisher_ep_prefix_ip_prefix_len', 'dsa_rule_entry_publisher_ep_version', 'dsa_rule_entry_subscriber', 'dsa_rule_entry_subscriber_ep_type', 'dsa_rule_entry_subscriber_ep_id', 'dsa_rule_entry_subscriber_ep_prefix', 'dsa_rule_entry_subscriber_ep_prefix_ip_prefix', 'dsa_rule_entry_subscriber_ep_prefix_ip_prefix_len', 'dsa_rule_entry_subscriber_ep_version', 'id_perms', 'id_perms_permissions', 'id_perms_permissions_owner', 'id_perms_permissions_owner_access', 'id_perms_permissions_group', 'id_perms_permissions_group_access', 'id_perms_permissions_other_access', 'id_perms_uuid', 'id_perms_uuid_uuid_mslong', 'id_perms_uuid_uuid_lslong', 'id_perms_enable', 'id_perms_created', 'id_perms_last_modified', 'id_perms_description', 'id_perms_user_visible', 'id_perms_creator', 'display_name', 'annotations', 'annotations_key_value_pair', 'annotations_key_value_pair_key', 'annotations_key_value_pair_value', 'perms2', 'perms2_owner', 'perms2_owner_access', 'perms2_global_access', 'perms2_share', 'perms2_share_tenant', 'perms2_share_tenant_access', 'tag_refs', 'discovery_service_assignment'
    )

    properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('NAME.'),
            update_allowed=True,
            required=False,
        ),
        FQ_NAME: properties.Schema(
            properties.Schema.STRING,
            _('FQ_NAME.'),
            update_allowed=True,
            required=False,
        ),
        DSA_RULE_ENTRY: properties.Schema(
            properties.Schema.MAP,
            _('DSA_RULE_ENTRY.'),
            update_allowed=True,
            required=False,
            schema={
                DSA_RULE_ENTRY_PUBLISHER: properties.Schema(
                    properties.Schema.MAP,
                    _('DSA_RULE_ENTRY_PUBLISHER.'),
                    update_allowed=True,
                    required=False,
                    schema={
                        DSA_RULE_ENTRY_PUBLISHER_EP_TYPE: properties.Schema(
                            properties.Schema.STRING,
                            _('DSA_RULE_ENTRY_PUBLISHER_EP_TYPE.'),
                            update_allowed=True,
                            required=False,
                        ),
                        DSA_RULE_ENTRY_PUBLISHER_EP_ID: properties.Schema(
                            properties.Schema.STRING,
                            _('DSA_RULE_ENTRY_PUBLISHER_EP_ID.'),
                            update_allowed=True,
                            required=False,
                        ),
                        DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX: properties.Schema(
                            properties.Schema.MAP,
                            _('DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX.'),
                            update_allowed=True,
                            required=False,
                            schema={
                                DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX: properties.Schema(
                                    properties.Schema.STRING,
                                    _('DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX.'),
                                    update_allowed=True,
                                    required=False,
                                ),
                                DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX_LEN: properties.Schema(
                                    properties.Schema.INTEGER,
                                    _('DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX_LEN.'),
                                    update_allowed=True,
                                    required=False,
                                ),
                            }
                        ),
                        DSA_RULE_ENTRY_PUBLISHER_EP_VERSION: properties.Schema(
                            properties.Schema.STRING,
                            _('DSA_RULE_ENTRY_PUBLISHER_EP_VERSION.'),
                            update_allowed=True,
                            required=False,
                        ),
                    }
                ),
                DSA_RULE_ENTRY_SUBSCRIBER: properties.Schema(
                    properties.Schema.LIST,
                    _('DSA_RULE_ENTRY_SUBSCRIBER.'),
                    update_allowed=True,
                    required=False,
                    schema=properties.Schema(
                        properties.Schema.MAP,
                        schema={
                            DSA_RULE_ENTRY_SUBSCRIBER_EP_TYPE: properties.Schema(
                                properties.Schema.STRING,
                                _('DSA_RULE_ENTRY_SUBSCRIBER_EP_TYPE.'),
                                update_allowed=True,
                                required=False,
                            ),
                            DSA_RULE_ENTRY_SUBSCRIBER_EP_ID: properties.Schema(
                                properties.Schema.STRING,
                                _('DSA_RULE_ENTRY_SUBSCRIBER_EP_ID.'),
                                update_allowed=True,
                                required=False,
                            ),
                            DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX: properties.Schema(
                                properties.Schema.MAP,
                                _('DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX.'),
                                update_allowed=True,
                                required=False,
                                schema={
                                    DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX: properties.Schema(
                                        properties.Schema.STRING,
                                        _('DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX.'),
                                        update_allowed=True,
                                        required=False,
                                    ),
                                    DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX_LEN: properties.Schema(
                                        properties.Schema.INTEGER,
                                        _('DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX_LEN.'),
                                        update_allowed=True,
                                        required=False,
                                    ),
                                }
                            ),
                            DSA_RULE_ENTRY_SUBSCRIBER_EP_VERSION: properties.Schema(
                                properties.Schema.STRING,
                                _('DSA_RULE_ENTRY_SUBSCRIBER_EP_VERSION.'),
                                update_allowed=True,
                                required=False,
                            ),
                        }
                    )
                ),
            }
        ),
        ID_PERMS: properties.Schema(
            properties.Schema.MAP,
            _('ID_PERMS.'),
            update_allowed=True,
            required=False,
            schema={
                ID_PERMS_PERMISSIONS: properties.Schema(
                    properties.Schema.MAP,
                    _('ID_PERMS_PERMISSIONS.'),
                    update_allowed=True,
                    required=False,
                    schema={
                        ID_PERMS_PERMISSIONS_OWNER: properties.Schema(
                            properties.Schema.STRING,
                            _('ID_PERMS_PERMISSIONS_OWNER.'),
                            update_allowed=True,
                            required=False,
                        ),
                        ID_PERMS_PERMISSIONS_OWNER_ACCESS: properties.Schema(
                            properties.Schema.INTEGER,
                            _('ID_PERMS_PERMISSIONS_OWNER_ACCESS.'),
                            update_allowed=True,
                            required=False,
                            constraints=[
                                constraints.Range(0, 7),
                            ],
                        ),
                        ID_PERMS_PERMISSIONS_GROUP: properties.Schema(
                            properties.Schema.STRING,
                            _('ID_PERMS_PERMISSIONS_GROUP.'),
                            update_allowed=True,
                            required=False,
                        ),
                        ID_PERMS_PERMISSIONS_GROUP_ACCESS: properties.Schema(
                            properties.Schema.INTEGER,
                            _('ID_PERMS_PERMISSIONS_GROUP_ACCESS.'),
                            update_allowed=True,
                            required=False,
                            constraints=[
                                constraints.Range(0, 7),
                            ],
                        ),
                        ID_PERMS_PERMISSIONS_OTHER_ACCESS: properties.Schema(
                            properties.Schema.INTEGER,
                            _('ID_PERMS_PERMISSIONS_OTHER_ACCESS.'),
                            update_allowed=True,
                            required=False,
                            constraints=[
                                constraints.Range(0, 7),
                            ],
                        ),
                    }
                ),
                ID_PERMS_UUID: properties.Schema(
                    properties.Schema.MAP,
                    _('ID_PERMS_UUID.'),
                    update_allowed=True,
                    required=False,
                    schema={
                        ID_PERMS_UUID_UUID_MSLONG: properties.Schema(
                            properties.Schema.MAP,
                            _('ID_PERMS_UUID_UUID_MSLONG.'),
                            update_allowed=True,
                            required=False,
                        ),
                        ID_PERMS_UUID_UUID_LSLONG: properties.Schema(
                            properties.Schema.MAP,
                            _('ID_PERMS_UUID_UUID_LSLONG.'),
                            update_allowed=True,
                            required=False,
                        ),
                    }
                ),
                ID_PERMS_ENABLE: properties.Schema(
                    properties.Schema.BOOLEAN,
                    _('ID_PERMS_ENABLE.'),
                    update_allowed=True,
                    required=False,
                ),
                ID_PERMS_CREATED: properties.Schema(
                    properties.Schema.INTEGER,
                    _('ID_PERMS_CREATED.'),
                    update_allowed=True,
                    required=False,
                ),
                ID_PERMS_LAST_MODIFIED: properties.Schema(
                    properties.Schema.INTEGER,
                    _('ID_PERMS_LAST_MODIFIED.'),
                    update_allowed=True,
                    required=False,
                ),
                ID_PERMS_DESCRIPTION: properties.Schema(
                    properties.Schema.STRING,
                    _('ID_PERMS_DESCRIPTION.'),
                    update_allowed=True,
                    required=False,
                ),
                ID_PERMS_USER_VISIBLE: properties.Schema(
                    properties.Schema.BOOLEAN,
                    _('ID_PERMS_USER_VISIBLE.'),
                    update_allowed=True,
                    required=False,
                ),
                ID_PERMS_CREATOR: properties.Schema(
                    properties.Schema.STRING,
                    _('ID_PERMS_CREATOR.'),
                    update_allowed=True,
                    required=False,
                ),
            }
        ),
        DISPLAY_NAME: properties.Schema(
            properties.Schema.STRING,
            _('DISPLAY_NAME.'),
            update_allowed=True,
            required=False,
        ),
        ANNOTATIONS: properties.Schema(
            properties.Schema.MAP,
            _('ANNOTATIONS.'),
            update_allowed=True,
            required=False,
            schema={
                ANNOTATIONS_KEY_VALUE_PAIR: properties.Schema(
                    properties.Schema.LIST,
                    _('ANNOTATIONS_KEY_VALUE_PAIR.'),
                    update_allowed=True,
                    required=False,
                    schema=properties.Schema(
                        properties.Schema.MAP,
                        schema={
                            ANNOTATIONS_KEY_VALUE_PAIR_KEY: properties.Schema(
                                properties.Schema.STRING,
                                _('ANNOTATIONS_KEY_VALUE_PAIR_KEY.'),
                                update_allowed=True,
                                required=False,
                            ),
                            ANNOTATIONS_KEY_VALUE_PAIR_VALUE: properties.Schema(
                                properties.Schema.STRING,
                                _('ANNOTATIONS_KEY_VALUE_PAIR_VALUE.'),
                                update_allowed=True,
                                required=False,
                            ),
                        }
                    )
                ),
            }
        ),
        PERMS2: properties.Schema(
            properties.Schema.MAP,
            _('PERMS2.'),
            update_allowed=True,
            required=False,
            schema={
                PERMS2_OWNER: properties.Schema(
                    properties.Schema.STRING,
                    _('PERMS2_OWNER.'),
                    update_allowed=True,
                    required=False,
                ),
                PERMS2_OWNER_ACCESS: properties.Schema(
                    properties.Schema.INTEGER,
                    _('PERMS2_OWNER_ACCESS.'),
                    update_allowed=True,
                    required=False,
                    constraints=[
                        constraints.Range(0, 7),
                    ],
                ),
                PERMS2_GLOBAL_ACCESS: properties.Schema(
                    properties.Schema.INTEGER,
                    _('PERMS2_GLOBAL_ACCESS.'),
                    update_allowed=True,
                    required=False,
                    constraints=[
                        constraints.Range(0, 7),
                    ],
                ),
                PERMS2_SHARE: properties.Schema(
                    properties.Schema.LIST,
                    _('PERMS2_SHARE.'),
                    update_allowed=True,
                    required=False,
                    schema=properties.Schema(
                        properties.Schema.MAP,
                        schema={
                            PERMS2_SHARE_TENANT: properties.Schema(
                                properties.Schema.STRING,
                                _('PERMS2_SHARE_TENANT.'),
                                update_allowed=True,
                                required=False,
                            ),
                            PERMS2_SHARE_TENANT_ACCESS: properties.Schema(
                                properties.Schema.INTEGER,
                                _('PERMS2_SHARE_TENANT_ACCESS.'),
                                update_allowed=True,
                                required=False,
                                constraints=[
                                    constraints.Range(0, 7),
                                ],
                            ),
                        }
                    )
                ),
            }
        ),
        TAG_REFS: properties.Schema(
            properties.Schema.LIST,
            _('TAG_REFS.'),
            update_allowed=True,
            required=False,
        ),
        DISCOVERY_SERVICE_ASSIGNMENT: properties.Schema(
            properties.Schema.STRING,
            _('DISCOVERY_SERVICE_ASSIGNMENT.'),
            update_allowed=True,
            required=False,
        ),
    }

    attributes_schema = {
        NAME: attributes.Schema(
            _('NAME.'),
        ),
        FQ_NAME: attributes.Schema(
            _('FQ_NAME.'),
        ),
        DSA_RULE_ENTRY: attributes.Schema(
            _('DSA_RULE_ENTRY.'),
        ),
        ID_PERMS: attributes.Schema(
            _('ID_PERMS.'),
        ),
        DISPLAY_NAME: attributes.Schema(
            _('DISPLAY_NAME.'),
        ),
        ANNOTATIONS: attributes.Schema(
            _('ANNOTATIONS.'),
        ),
        PERMS2: attributes.Schema(
            _('PERMS2.'),
        ),
        TAG_REFS: attributes.Schema(
            _('TAG_REFS.'),
        ),
        DISCOVERY_SERVICE_ASSIGNMENT: attributes.Schema(
            _('DISCOVERY_SERVICE_ASSIGNMENT.'),
        ),
    }

    update_allowed_keys = ('Properties',)

    @contrail.set_auth_token
    def handle_create(self):
        parent_obj = None
        if parent_obj is None and self.properties.get(self.DISCOVERY_SERVICE_ASSIGNMENT) and self.properties.get(self.DISCOVERY_SERVICE_ASSIGNMENT) != 'config-root':
            try:
                parent_obj = self.vnc_lib().discovery_service_assignment_read(fq_name_str=self.properties.get(self.DISCOVERY_SERVICE_ASSIGNMENT))
            except vnc_api.NoIdError:
                parent_obj = self.vnc_lib().discovery_service_assignment_read(id=str(uuid.UUID(self.properties.get(self.DISCOVERY_SERVICE_ASSIGNMENT))))
            except:
                parent_obj = None

        if parent_obj is None and self.properties.get(self.DISCOVERY_SERVICE_ASSIGNMENT) != 'config-root':
            raise Exception('Error: parent is not specified in template!')

        obj_0 = vnc_api.DsaRule(name=self.properties[self.NAME],
            parent_obj=parent_obj)

        if self.properties.get(self.DSA_RULE_ENTRY) is not None:
            obj_1 = vnc_api.DiscoveryServiceAssignmentType()
            if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER) is not None:
                obj_2 = vnc_api.DiscoveryPubSubEndPointType()
                if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_TYPE) is not None:
                    obj_2.set_ep_type(self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_TYPE))
                if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_ID) is not None:
                    obj_2.set_ep_id(self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_ID))
                if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX) is not None:
                    obj_3 = vnc_api.SubnetType()
                    if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX) is not None:
                        obj_3.set_ip_prefix(self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX))
                    if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX_LEN) is not None:
                        obj_3.set_ip_prefix_len(self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX_LEN))
                    obj_2.set_ep_prefix(obj_3)
                if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_VERSION) is not None:
                    obj_2.set_ep_version(self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_VERSION))
                obj_1.set_publisher(obj_2)
            if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER) is not None:
                for index_1 in range(len(self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER))):
                    obj_2 = vnc_api.DiscoveryPubSubEndPointType()
                    if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_TYPE) is not None:
                        obj_2.set_ep_type(self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_TYPE))
                    if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_ID) is not None:
                        obj_2.set_ep_id(self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_ID))
                    if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX) is not None:
                        obj_3 = vnc_api.SubnetType()
                        if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX) is not None:
                            obj_3.set_ip_prefix(self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX))
                        if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX_LEN) is not None:
                            obj_3.set_ip_prefix_len(self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX_LEN))
                        obj_2.set_ep_prefix(obj_3)
                    if self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_VERSION) is not None:
                        obj_2.set_ep_version(self.properties.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_VERSION))
                    obj_1.add_subscriber(obj_2)
            obj_0.set_dsa_rule_entry(obj_1)
        if self.properties.get(self.ID_PERMS) is not None:
            obj_1 = vnc_api.IdPermsType()
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS) is not None:
                obj_2 = vnc_api.PermType()
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OWNER) is not None:
                    obj_2.set_owner(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OWNER))
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OWNER_ACCESS) is not None:
                    obj_2.set_owner_access(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OWNER_ACCESS))
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_GROUP) is not None:
                    obj_2.set_group(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_GROUP))
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_GROUP_ACCESS) is not None:
                    obj_2.set_group_access(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_GROUP_ACCESS))
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OTHER_ACCESS) is not None:
                    obj_2.set_other_access(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OTHER_ACCESS))
                obj_1.set_permissions(obj_2)
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID) is not None:
                obj_2 = vnc_api.UuidType()
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID, {}).get(self.ID_PERMS_UUID_UUID_MSLONG) is not None:
                    obj_2.set_uuid_mslong(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID, {}).get(self.ID_PERMS_UUID_UUID_MSLONG))
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID, {}).get(self.ID_PERMS_UUID_UUID_LSLONG) is not None:
                    obj_2.set_uuid_lslong(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID, {}).get(self.ID_PERMS_UUID_UUID_LSLONG))
                obj_1.set_uuid(obj_2)
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_ENABLE) is not None:
                obj_1.set_enable(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_ENABLE))
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_CREATED) is not None:
                obj_1.set_created(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_CREATED))
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_LAST_MODIFIED) is not None:
                obj_1.set_last_modified(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_LAST_MODIFIED))
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_DESCRIPTION) is not None:
                obj_1.set_description(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_DESCRIPTION))
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_USER_VISIBLE) is not None:
                obj_1.set_user_visible(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_USER_VISIBLE))
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_CREATOR) is not None:
                obj_1.set_creator(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_CREATOR))
            obj_0.set_id_perms(obj_1)
        if self.properties.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(self.properties.get(self.DISPLAY_NAME))
        if self.properties.get(self.ANNOTATIONS) is not None:
            obj_1 = vnc_api.KeyValuePairs()
            if self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR) is not None:
                for index_1 in range(len(self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR))):
                    obj_2 = vnc_api.KeyValuePair()
                    if self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_KEY) is not None:
                        obj_2.set_key(self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_KEY))
                    if self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_VALUE) is not None:
                        obj_2.set_value(self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_VALUE))
                    obj_1.add_key_value_pair(obj_2)
            obj_0.set_annotations(obj_1)
        if self.properties.get(self.PERMS2) is not None:
            obj_1 = vnc_api.PermType2()
            if self.properties.get(self.PERMS2, {}).get(self.PERMS2_OWNER) is not None:
                obj_1.set_owner(self.properties.get(self.PERMS2, {}).get(self.PERMS2_OWNER))
            if self.properties.get(self.PERMS2, {}).get(self.PERMS2_OWNER_ACCESS) is not None:
                obj_1.set_owner_access(self.properties.get(self.PERMS2, {}).get(self.PERMS2_OWNER_ACCESS))
            if self.properties.get(self.PERMS2, {}).get(self.PERMS2_GLOBAL_ACCESS) is not None:
                obj_1.set_global_access(self.properties.get(self.PERMS2, {}).get(self.PERMS2_GLOBAL_ACCESS))
            if self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE) is not None:
                for index_1 in range(len(self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE))):
                    obj_2 = vnc_api.ShareType()
                    if self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT) is not None:
                        obj_2.set_tenant(self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT))
                    if self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT_ACCESS) is not None:
                        obj_2.set_tenant_access(self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT_ACCESS))
                    obj_1.add_share(obj_2)
            obj_0.set_perms2(obj_1)

        # reference to tag_refs
        if self.properties.get(self.TAG_REFS):
            for index_0 in range(len(self.properties.get(self.TAG_REFS))):
                try:
                    ref_obj = self.vnc_lib().tag_read(
                        id=self.properties.get(self.TAG_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().tag_read(
                        fq_name_str=self.properties.get(self.TAG_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_tag(ref_obj)

        try:
            obj_uuid = super(ContrailDsaRule, self).resource_create(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

        self.resource_id_set(obj_uuid)

    @contrail.set_auth_token
    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        try:
            obj_0 = self.vnc_lib().dsa_rule_read(
                id=self.resource_id
            )
        except Exception as e:
            raise Exception(_('%s') % str(e))

        if prop_diff.get(self.DSA_RULE_ENTRY) is not None:
            obj_1 = vnc_api.DiscoveryServiceAssignmentType()
            if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER) is not None:
                obj_2 = vnc_api.DiscoveryPubSubEndPointType()
                if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_TYPE) is not None:
                    obj_2.set_ep_type(prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_TYPE))
                if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_ID) is not None:
                    obj_2.set_ep_id(prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_ID))
                if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX) is not None:
                    obj_3 = vnc_api.SubnetType()
                    if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX) is not None:
                        obj_3.set_ip_prefix(prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX))
                    if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX_LEN) is not None:
                        obj_3.set_ip_prefix_len(prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_PREFIX_IP_PREFIX_LEN))
                    obj_2.set_ep_prefix(obj_3)
                if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_VERSION) is not None:
                    obj_2.set_ep_version(prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_PUBLISHER, {}).get(self.DSA_RULE_ENTRY_PUBLISHER_EP_VERSION))
                obj_1.set_publisher(obj_2)
            if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER) is not None:
                for index_1 in range(len(prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER))):
                    obj_2 = vnc_api.DiscoveryPubSubEndPointType()
                    if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_TYPE) is not None:
                        obj_2.set_ep_type(prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_TYPE))
                    if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_ID) is not None:
                        obj_2.set_ep_id(prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_ID))
                    if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX) is not None:
                        obj_3 = vnc_api.SubnetType()
                        if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX) is not None:
                            obj_3.set_ip_prefix(prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX))
                        if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX_LEN) is not None:
                            obj_3.set_ip_prefix_len(prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_PREFIX_IP_PREFIX_LEN))
                        obj_2.set_ep_prefix(obj_3)
                    if prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_VERSION) is not None:
                        obj_2.set_ep_version(prop_diff.get(self.DSA_RULE_ENTRY, {}).get(self.DSA_RULE_ENTRY_SUBSCRIBER, {})[index_1].get(self.DSA_RULE_ENTRY_SUBSCRIBER_EP_VERSION))
                    obj_1.add_subscriber(obj_2)
            obj_0.set_dsa_rule_entry(obj_1)
        if prop_diff.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(prop_diff.get(self.DISPLAY_NAME))
        if prop_diff.get(self.ANNOTATIONS) is not None:
            obj_1 = vnc_api.KeyValuePairs()
            if prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR) is not None:
                for index_1 in range(len(prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR))):
                    obj_2 = vnc_api.KeyValuePair()
                    if prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_KEY) is not None:
                        obj_2.set_key(prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_KEY))
                    if prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_VALUE) is not None:
                        obj_2.set_value(prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_VALUE))
                    obj_1.add_key_value_pair(obj_2)
            obj_0.set_annotations(obj_1)

        # reference to tag_refs
        ref_obj_list = []
        if self.TAG_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.TAG_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().tag_read(
                        id=prop_diff.get(self.TAG_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().tag_read(
                        fq_name_str=prop_diff.get(self.TAG_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_tag_list(ref_obj_list)
            # End: reference to tag_refs

        try:
            self.vnc_lib().dsa_rule_update(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

    @contrail.set_auth_token
    def handle_delete(self):
        if self.resource_id is None:
            return

        try:
            self.vnc_lib().dsa_rule_delete(id=self.resource_id)
        except Exception as ex:
            self._ignore_not_found(ex)
            LOG.warn(_('dsa_rule %s already deleted.') % self.name)

    @contrail.set_auth_token
    def _show_resource(self):
        obj = self.vnc_lib().dsa_rule_read(id=self.resource_id)
        obj_dict = obj.serialize_to_json()
        return obj_dict


def resource_mapping():
    return {
        'OS::ContrailV2::DsaRule': ContrailDsaRule,
    }
