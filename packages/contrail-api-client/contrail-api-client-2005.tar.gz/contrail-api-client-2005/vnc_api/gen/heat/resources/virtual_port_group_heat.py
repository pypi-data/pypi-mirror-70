
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


class ContrailVirtualPortGroup(contrail.ContrailResource):
    PROPERTIES = (
        NAME, FQ_NAME, DISPLAY_NAME, ANNOTATIONS, ANNOTATIONS_KEY_VALUE_PAIR, ANNOTATIONS_KEY_VALUE_PAIR_KEY, ANNOTATIONS_KEY_VALUE_PAIR_VALUE, PERMS2, PERMS2_OWNER, PERMS2_OWNER_ACCESS, PERMS2_GLOBAL_ACCESS, PERMS2_SHARE, PERMS2_SHARE_TENANT, PERMS2_SHARE_TENANT_ACCESS, ID_PERMS, ID_PERMS_PERMISSIONS, ID_PERMS_PERMISSIONS_OWNER, ID_PERMS_PERMISSIONS_OWNER_ACCESS, ID_PERMS_PERMISSIONS_GROUP, ID_PERMS_PERMISSIONS_GROUP_ACCESS, ID_PERMS_PERMISSIONS_OTHER_ACCESS, ID_PERMS_UUID, ID_PERMS_UUID_UUID_MSLONG, ID_PERMS_UUID_UUID_LSLONG, ID_PERMS_ENABLE, ID_PERMS_CREATED, ID_PERMS_LAST_MODIFIED, ID_PERMS_DESCRIPTION, ID_PERMS_USER_VISIBLE, ID_PERMS_CREATOR, VIRTUAL_PORT_GROUP_TRUNK_PORT_ID, VIRTUAL_PORT_GROUP_TYPE, VIRTUAL_PORT_GROUP_LACP_ENABLED, VIRTUAL_PORT_GROUP_USER_CREATED, SECURITY_GROUP_REFS, PORT_PROFILE_REFS, PHYSICAL_INTERFACE_REFS, PHYSICAL_INTERFACE_REFS_DATA, PHYSICAL_INTERFACE_REFS_DATA_AE_NUM, VIRTUAL_MACHINE_INTERFACE_REFS, TAG_REFS, FABRIC, PROJECT
    ) = (
        'name', 'fq_name', 'display_name', 'annotations', 'annotations_key_value_pair', 'annotations_key_value_pair_key', 'annotations_key_value_pair_value', 'perms2', 'perms2_owner', 'perms2_owner_access', 'perms2_global_access', 'perms2_share', 'perms2_share_tenant', 'perms2_share_tenant_access', 'id_perms', 'id_perms_permissions', 'id_perms_permissions_owner', 'id_perms_permissions_owner_access', 'id_perms_permissions_group', 'id_perms_permissions_group_access', 'id_perms_permissions_other_access', 'id_perms_uuid', 'id_perms_uuid_uuid_mslong', 'id_perms_uuid_uuid_lslong', 'id_perms_enable', 'id_perms_created', 'id_perms_last_modified', 'id_perms_description', 'id_perms_user_visible', 'id_perms_creator', 'virtual_port_group_trunk_port_id', 'virtual_port_group_type', 'virtual_port_group_lacp_enabled', 'virtual_port_group_user_created', 'security_group_refs', 'port_profile_refs', 'physical_interface_refs', 'physical_interface_refs_data', 'physical_interface_refs_data_ae_num', 'virtual_machine_interface_refs', 'tag_refs', 'fabric', 'project'
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
        VIRTUAL_PORT_GROUP_TRUNK_PORT_ID: properties.Schema(
            properties.Schema.STRING,
            _('VIRTUAL_PORT_GROUP_TRUNK_PORT_ID.'),
            update_allowed=True,
            required=False,
        ),
        VIRTUAL_PORT_GROUP_TYPE: properties.Schema(
            properties.Schema.STRING,
            _('VIRTUAL_PORT_GROUP_TYPE.'),
            update_allowed=True,
            required=False,
        ),
        VIRTUAL_PORT_GROUP_LACP_ENABLED: properties.Schema(
            properties.Schema.BOOLEAN,
            _('VIRTUAL_PORT_GROUP_LACP_ENABLED.'),
            update_allowed=True,
            required=False,
        ),
        VIRTUAL_PORT_GROUP_USER_CREATED: properties.Schema(
            properties.Schema.BOOLEAN,
            _('VIRTUAL_PORT_GROUP_USER_CREATED.'),
            update_allowed=True,
            required=False,
        ),
        SECURITY_GROUP_REFS: properties.Schema(
            properties.Schema.LIST,
            _('SECURITY_GROUP_REFS.'),
            update_allowed=True,
            required=False,
        ),
        PORT_PROFILE_REFS: properties.Schema(
            properties.Schema.LIST,
            _('PORT_PROFILE_REFS.'),
            update_allowed=True,
            required=False,
        ),
        PHYSICAL_INTERFACE_REFS: properties.Schema(
            properties.Schema.LIST,
            _('PHYSICAL_INTERFACE_REFS.'),
            update_allowed=True,
            required=False,
        ),
        PHYSICAL_INTERFACE_REFS_DATA: properties.Schema(
            properties.Schema.LIST,
            _('PHYSICAL_INTERFACE_REFS_DATA.'),
            update_allowed=True,
            required=False,
            schema=properties.Schema(
                properties.Schema.MAP,
                schema={
                    PHYSICAL_INTERFACE_REFS_DATA_AE_NUM: properties.Schema(
                        properties.Schema.INTEGER,
                        _('PHYSICAL_INTERFACE_REFS_DATA_AE_NUM.'),
                        update_allowed=True,
                        required=False,
                    ),
                }
            )
        ),
        VIRTUAL_MACHINE_INTERFACE_REFS: properties.Schema(
            properties.Schema.LIST,
            _('VIRTUAL_MACHINE_INTERFACE_REFS.'),
            update_allowed=True,
            required=False,
        ),
        TAG_REFS: properties.Schema(
            properties.Schema.LIST,
            _('TAG_REFS.'),
            update_allowed=True,
            required=False,
        ),
        FABRIC: properties.Schema(
            properties.Schema.STRING,
            _('FABRIC.'),
            update_allowed=True,
            required=False,
        ),
        PROJECT: properties.Schema(
            properties.Schema.STRING,
            _('PROJECT.'),
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
        DISPLAY_NAME: attributes.Schema(
            _('DISPLAY_NAME.'),
        ),
        ANNOTATIONS: attributes.Schema(
            _('ANNOTATIONS.'),
        ),
        PERMS2: attributes.Schema(
            _('PERMS2.'),
        ),
        ID_PERMS: attributes.Schema(
            _('ID_PERMS.'),
        ),
        VIRTUAL_PORT_GROUP_TRUNK_PORT_ID: attributes.Schema(
            _('VIRTUAL_PORT_GROUP_TRUNK_PORT_ID.'),
        ),
        VIRTUAL_PORT_GROUP_TYPE: attributes.Schema(
            _('VIRTUAL_PORT_GROUP_TYPE.'),
        ),
        VIRTUAL_PORT_GROUP_LACP_ENABLED: attributes.Schema(
            _('VIRTUAL_PORT_GROUP_LACP_ENABLED.'),
        ),
        VIRTUAL_PORT_GROUP_USER_CREATED: attributes.Schema(
            _('VIRTUAL_PORT_GROUP_USER_CREATED.'),
        ),
        SECURITY_GROUP_REFS: attributes.Schema(
            _('SECURITY_GROUP_REFS.'),
        ),
        PORT_PROFILE_REFS: attributes.Schema(
            _('PORT_PROFILE_REFS.'),
        ),
        PHYSICAL_INTERFACE_REFS: attributes.Schema(
            _('PHYSICAL_INTERFACE_REFS.'),
        ),
        PHYSICAL_INTERFACE_REFS_DATA: attributes.Schema(
            _('PHYSICAL_INTERFACE_REFS_DATA.'),
        ),
        VIRTUAL_MACHINE_INTERFACE_REFS: attributes.Schema(
            _('VIRTUAL_MACHINE_INTERFACE_REFS.'),
        ),
        TAG_REFS: attributes.Schema(
            _('TAG_REFS.'),
        ),
        FABRIC: attributes.Schema(
            _('FABRIC.'),
        ),
        PROJECT: attributes.Schema(
            _('PROJECT.'),
        ),
    }

    update_allowed_keys = ('Properties',)

    @contrail.set_auth_token
    def handle_create(self):
        parent_obj = None
        if parent_obj is None and self.properties.get(self.FABRIC) and self.properties.get(self.FABRIC) != 'config-root':
            try:
                parent_obj = self.vnc_lib().fabric_read(fq_name_str=self.properties.get(self.FABRIC))
            except vnc_api.NoIdError:
                parent_obj = self.vnc_lib().fabric_read(id=str(uuid.UUID(self.properties.get(self.FABRIC))))
            except:
                parent_obj = None
        if parent_obj is None and self.properties.get(self.PROJECT) and self.properties.get(self.PROJECT) != 'config-root':
            try:
                parent_obj = self.vnc_lib().project_read(fq_name_str=self.properties.get(self.PROJECT))
            except vnc_api.NoIdError:
                parent_obj = self.vnc_lib().project_read(id=str(uuid.UUID(self.properties.get(self.PROJECT))))
            except:
                parent_obj = None

        if parent_obj is None and self.properties.get(self.PROJECT) != 'config-root':
            tenant_id = self.stack.context.tenant_id
            parent_obj = self.vnc_lib().project_read(id=str(uuid.UUID(tenant_id)))

        if parent_obj is None and self.properties.get(self.PROJECT) != 'config-root':
            raise Exception('Error: parent is not specified in template!')

        obj_0 = vnc_api.VirtualPortGroup(name=self.properties[self.NAME],
            parent_obj=parent_obj)

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
        if self.properties.get(self.VIRTUAL_PORT_GROUP_TRUNK_PORT_ID) is not None:
            obj_0.set_virtual_port_group_trunk_port_id(self.properties.get(self.VIRTUAL_PORT_GROUP_TRUNK_PORT_ID))
        if self.properties.get(self.VIRTUAL_PORT_GROUP_TYPE) is not None:
            obj_0.set_virtual_port_group_type(self.properties.get(self.VIRTUAL_PORT_GROUP_TYPE))
        if self.properties.get(self.VIRTUAL_PORT_GROUP_LACP_ENABLED) is not None:
            obj_0.set_virtual_port_group_lacp_enabled(self.properties.get(self.VIRTUAL_PORT_GROUP_LACP_ENABLED))
        if self.properties.get(self.VIRTUAL_PORT_GROUP_USER_CREATED) is not None:
            obj_0.set_virtual_port_group_user_created(self.properties.get(self.VIRTUAL_PORT_GROUP_USER_CREATED))

        # reference to security_group_refs
        if self.properties.get(self.SECURITY_GROUP_REFS):
            for index_0 in range(len(self.properties.get(self.SECURITY_GROUP_REFS))):
                try:
                    ref_obj = self.vnc_lib().security_group_read(
                        id=self.properties.get(self.SECURITY_GROUP_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().security_group_read(
                        fq_name_str=self.properties.get(self.SECURITY_GROUP_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_security_group(ref_obj)

        # reference to port_profile_refs
        if self.properties.get(self.PORT_PROFILE_REFS):
            for index_0 in range(len(self.properties.get(self.PORT_PROFILE_REFS))):
                try:
                    ref_obj = self.vnc_lib().port_profile_read(
                        id=self.properties.get(self.PORT_PROFILE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().port_profile_read(
                        fq_name_str=self.properties.get(self.PORT_PROFILE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_port_profile(ref_obj)

        # reference to physical_interface_refs
        if len(self.properties.get(self.PHYSICAL_INTERFACE_REFS) or []) != len(self.properties.get(self.PHYSICAL_INTERFACE_REFS_DATA) or []):
            raise Exception(_('virtual-port-group: specify physical_interface_refs for each physical_interface_refs_data.'))
        obj_1 = None
        if self.properties.get(self.PHYSICAL_INTERFACE_REFS_DATA) is not None:
            for index_0 in range(len(self.properties.get(self.PHYSICAL_INTERFACE_REFS_DATA))):
                obj_1 = vnc_api.VpgInterfaceParametersType()
                if self.properties.get(self.PHYSICAL_INTERFACE_REFS_DATA, {})[index_0].get(self.PHYSICAL_INTERFACE_REFS_DATA_AE_NUM) is not None:
                    obj_1.set_ae_num(self.properties.get(self.PHYSICAL_INTERFACE_REFS_DATA, {})[index_0].get(self.PHYSICAL_INTERFACE_REFS_DATA_AE_NUM))

                if self.properties.get(self.PHYSICAL_INTERFACE_REFS):
                    try:
                        ref_obj = self.vnc_lib().physical_interface_read(
                            id=self.properties.get(self.PHYSICAL_INTERFACE_REFS)[index_0]
                        )
                    except vnc_api.NoIdError:
                        ref_obj = self.vnc_lib().physical_interface_read(
                            fq_name_str=self.properties.get(self.PHYSICAL_INTERFACE_REFS)[index_0]
                        )
                    except Exception as e:
                        raise Exception(_('%s') % str(e))
                    obj_0.add_physical_interface(ref_obj, obj_1)

        # reference to virtual_machine_interface_refs
        if self.properties.get(self.VIRTUAL_MACHINE_INTERFACE_REFS):
            for index_0 in range(len(self.properties.get(self.VIRTUAL_MACHINE_INTERFACE_REFS))):
                try:
                    ref_obj = self.vnc_lib().virtual_machine_interface_read(
                        id=self.properties.get(self.VIRTUAL_MACHINE_INTERFACE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().virtual_machine_interface_read(
                        fq_name_str=self.properties.get(self.VIRTUAL_MACHINE_INTERFACE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_virtual_machine_interface(ref_obj)

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
            obj_uuid = super(ContrailVirtualPortGroup, self).resource_create(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

        self.resource_id_set(obj_uuid)

    @contrail.set_auth_token
    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        try:
            obj_0 = self.vnc_lib().virtual_port_group_read(
                id=self.resource_id
            )
        except Exception as e:
            raise Exception(_('%s') % str(e))

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
        if prop_diff.get(self.VIRTUAL_PORT_GROUP_TYPE) is not None:
            obj_0.set_virtual_port_group_type(prop_diff.get(self.VIRTUAL_PORT_GROUP_TYPE))
        if prop_diff.get(self.VIRTUAL_PORT_GROUP_LACP_ENABLED) is not None:
            obj_0.set_virtual_port_group_lacp_enabled(prop_diff.get(self.VIRTUAL_PORT_GROUP_LACP_ENABLED))
        if prop_diff.get(self.VIRTUAL_PORT_GROUP_USER_CREATED) is not None:
            obj_0.set_virtual_port_group_user_created(prop_diff.get(self.VIRTUAL_PORT_GROUP_USER_CREATED))

        # reference to security_group_refs
        ref_obj_list = []
        if self.SECURITY_GROUP_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.SECURITY_GROUP_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().security_group_read(
                        id=prop_diff.get(self.SECURITY_GROUP_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().security_group_read(
                        fq_name_str=prop_diff.get(self.SECURITY_GROUP_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_security_group_list(ref_obj_list)
            # End: reference to security_group_refs

        # reference to port_profile_refs
        ref_obj_list = []
        if self.PORT_PROFILE_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.PORT_PROFILE_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().port_profile_read(
                        id=prop_diff.get(self.PORT_PROFILE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().port_profile_read(
                        fq_name_str=prop_diff.get(self.PORT_PROFILE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_port_profile_list(ref_obj_list)
            # End: reference to port_profile_refs

        # reference to physical_interface
        update = 0
        if not self.PHYSICAL_INTERFACE_REFS in prop_diff:
            ref_obj_list = [ref['to'] for ref in obj_0.get_physical_interface_refs() or []]
        else:
            ref_obj_list = []
            update = 1
        if not self.PHYSICAL_INTERFACE_REFS_DATA in prop_diff:
            ref_data_list = [ref['attr'] for ref in obj_0.get_physical_interface_refs() or []]
        else:
            ref_data_list = []

        if prop_diff.get(self.PHYSICAL_INTERFACE_REFS_DATA) is not None:
            for index_0 in range(len(prop_diff.get(self.PHYSICAL_INTERFACE_REFS_DATA))):
                obj_1 = vnc_api.VpgInterfaceParametersType()
                if prop_diff.get(self.PHYSICAL_INTERFACE_REFS_DATA, {})[index_0].get(self.PHYSICAL_INTERFACE_REFS_DATA_AE_NUM) is not None:
                    obj_1.set_ae_num(prop_diff.get(self.PHYSICAL_INTERFACE_REFS_DATA, {})[index_0].get(self.PHYSICAL_INTERFACE_REFS_DATA_AE_NUM))
                ref_data_list.append(obj_1)
        if self.PHYSICAL_INTERFACE_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.PHYSICAL_INTERFACE_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().physical_interface_read(
                        id=prop_diff.get(self.PHYSICAL_INTERFACE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().physical_interface_read(
                        fq_name_str=prop_diff.get(self.PHYSICAL_INTERFACE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append(ref_obj.fq_name)

        if len(ref_obj_list) != len(ref_data_list):
            raise Exception(_('virtual-port-group: specify physical_interface_refs_data for each physical_interface_refs.'))

        if update or ref_obj_list or ref_data_list:
            obj_0.set_physical_interface_list(ref_obj_list, ref_data_list)
        # End: reference to physical_interface_refs

        # reference to virtual_machine_interface_refs
        ref_obj_list = []
        if self.VIRTUAL_MACHINE_INTERFACE_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.VIRTUAL_MACHINE_INTERFACE_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().virtual_machine_interface_read(
                        id=prop_diff.get(self.VIRTUAL_MACHINE_INTERFACE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().virtual_machine_interface_read(
                        fq_name_str=prop_diff.get(self.VIRTUAL_MACHINE_INTERFACE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_virtual_machine_interface_list(ref_obj_list)
            # End: reference to virtual_machine_interface_refs

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
            self.vnc_lib().virtual_port_group_update(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

    @contrail.set_auth_token
    def handle_delete(self):
        if self.resource_id is None:
            return

        try:
            self.vnc_lib().virtual_port_group_delete(id=self.resource_id)
        except Exception as ex:
            self._ignore_not_found(ex)
            LOG.warn(_('virtual_port_group %s already deleted.') % self.name)

    @contrail.set_auth_token
    def _show_resource(self):
        obj = self.vnc_lib().virtual_port_group_read(id=self.resource_id)
        obj_dict = obj.serialize_to_json()
        return obj_dict


def resource_mapping():
    return {
        'OS::ContrailV2::VirtualPortGroup': ContrailVirtualPortGroup,
    }
