# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/mdb/mysql/v1alpha/user_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2
from yandex.cloud.mdb.mysql.v1alpha import user_pb2 as yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1alpha_dot_user__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/mdb/mysql/v1alpha/user_service.proto',
  package='yandex.cloud.mdb.mysql.v1alpha',
  syntax='proto3',
  serialized_options=b'\n\"yandex.cloud.api.mdb.mysql.v1alphaZHgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/mysql/v1alpha;mysql',
  serialized_pb=b'\n1yandex/cloud/mdb/mysql/v1alpha/user_service.proto\x12\x1eyandex.cloud.mdb.mysql.v1alpha\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a yandex/cloud/api/operation.proto\x1a&yandex/cloud/operation/operation.proto\x1a\x1dyandex/cloud/validation.proto\x1a)yandex/cloud/mdb/mysql/v1alpha/user.proto\"d\n\x0eGetUserRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x30\n\tuser_name\x18\x02 \x01(\tB\x1d\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=63\xf2\xc7\x31\r[a-zA-Z0-9_]*\"r\n\x10ListUsersRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06\x30-1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\"a\n\x11ListUsersResponse\x12\x33\n\x05users\x18\x01 \x03(\x0b\x32$.yandex.cloud.mdb.mysql.v1alpha.User\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"x\n\x11\x43reateUserRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x41\n\tuser_spec\x18\x02 \x01(\x0b\x32(.yandex.cloud.mdb.mysql.v1alpha.UserSpecB\x04\xe8\xc7\x31\x01\";\n\x12\x43reateUserMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\x12\x11\n\tuser_name\x18\x02 \x01(\t\"\xf6\x01\n\x11UpdateUserRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x30\n\tuser_name\x18\x02 \x01(\tB\x1d\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=63\xf2\xc7\x31\r[a-zA-Z0-9_]*\x12/\n\x0bupdate_mask\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x1b\n\x08password\x18\x04 \x01(\tB\t\x8a\xc8\x31\x05\x38-128\x12?\n\x0bpermissions\x18\x05 \x03(\x0b\x32*.yandex.cloud.mdb.mysql.v1alpha.Permission\";\n\x12UpdateUserMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\x12\x11\n\tuser_name\x18\x02 \x01(\t\"g\n\x11\x44\x65leteUserRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x30\n\tuser_name\x18\x02 \x01(\tB\x1d\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=63\xf2\xc7\x31\r[a-zA-Z0-9_]*\";\n\x12\x44\x65leteUserMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\x12\x11\n\tuser_name\x18\x02 \x01(\t\"\xb6\x01\n\x1aGrantUserPermissionRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x30\n\tuser_name\x18\x02 \x01(\tB\x1d\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=63\xf2\xc7\x31\r[a-zA-Z0-9_]*\x12\x44\n\npermission\x18\x03 \x01(\x0b\x32*.yandex.cloud.mdb.mysql.v1alpha.PermissionB\x04\xe8\xc7\x31\x01\"D\n\x1bGrantUserPermissionMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\x12\x11\n\tuser_name\x18\x02 \x01(\t\"\xa8\x01\n\x1bRevokeUserPermissionRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x30\n\tuser_name\x18\x02 \x01(\tB\x1d\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=63\xf2\xc7\x31\r[a-zA-Z0-9_]*\x12\x35\n\rdatabase_name\x18\x03 \x01(\tB\x1e\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=63\xf2\xc7\x31\x0e[a-zA-Z0-9_-]*\"E\n\x1cRevokeUserPermissionMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\x12\x11\n\tuser_name\x18\x02 \x01(\t2\xad\x0b\n\x0bUserService\x12\xa3\x01\n\x03Get\x12..yandex.cloud.mdb.mysql.v1alpha.GetUserRequest\x1a$.yandex.cloud.mdb.mysql.v1alpha.User\"F\x82\xd3\xe4\x93\x02@\x12>/managed-mysql/v1alpha/clusters/{cluster_id}/users/{user_name}\x12\xa7\x01\n\x04List\x12\x30.yandex.cloud.mdb.mysql.v1alpha.ListUsersRequest\x1a\x31.yandex.cloud.mdb.mysql.v1alpha.ListUsersResponse\":\x82\xd3\xe4\x93\x02\x34\x12\x32/managed-mysql/v1alpha/clusters/{cluster_id}/users\x12\xbb\x01\n\x06\x43reate\x12\x31.yandex.cloud.mdb.mysql.v1alpha.CreateUserRequest\x1a!.yandex.cloud.operation.Operation\"[\x82\xd3\xe4\x93\x02\x37\"2/managed-mysql/v1alpha/clusters/{cluster_id}/users:\x01*\xb2\xd2*\x1a\n\x12\x43reateUserMetadata\x12\x04User\x12\xc7\x01\n\x06Update\x12\x31.yandex.cloud.mdb.mysql.v1alpha.UpdateUserRequest\x1a!.yandex.cloud.operation.Operation\"g\x82\xd3\xe4\x93\x02\x43\x32>/managed-mysql/v1alpha/clusters/{cluster_id}/users/{user_name}:\x01*\xb2\xd2*\x1a\n\x12UpdateUserMetadata\x12\x04User\x12\xd5\x01\n\x06\x44\x65lete\x12\x31.yandex.cloud.mdb.mysql.v1alpha.DeleteUserRequest\x1a!.yandex.cloud.operation.Operation\"u\x82\xd3\xe4\x93\x02@*>/managed-mysql/v1alpha/clusters/{cluster_id}/users/{user_name}\xb2\xd2*+\n\x12\x44\x65leteUserMetadata\x12\x15google.protobuf.Empty\x12\xf3\x01\n\x0fGrantPermission\x12:.yandex.cloud.mdb.mysql.v1alpha.GrantUserPermissionRequest\x1a!.yandex.cloud.operation.Operation\"\x80\x01\x82\xd3\xe4\x93\x02S\"N/managed-mysql/v1alpha/clusters/{cluster_id}/users/{user_name}:grantPermission:\x01*\xb2\xd2*#\n\x1bGrantUserPermissionMetadata\x12\x04User\x12\xf7\x01\n\x10RevokePermission\x12;.yandex.cloud.mdb.mysql.v1alpha.RevokeUserPermissionRequest\x1a!.yandex.cloud.operation.Operation\"\x82\x01\x82\xd3\xe4\x93\x02T\"O/managed-mysql/v1alpha/clusters/{cluster_id}/users/{user_name}:revokePermission:\x01*\xb2\xd2*$\n\x1cRevokeUserPermissionMetadata\x12\x04UserBn\n\"yandex.cloud.api.mdb.mysql.v1alphaZHgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/mysql/v1alpha;mysqlb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,yandex_dot_cloud_dot_api_dot_operation__pb2.DESCRIPTOR,yandex_dot_cloud_dot_operation_dot_operation__pb2.DESCRIPTOR,yandex_dot_cloud_dot_validation__pb2.DESCRIPTOR,yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1alpha_dot_user__pb2.DESCRIPTOR,])




_GETUSERREQUEST = _descriptor.Descriptor(
  name='GetUserRequest',
  full_name='yandex.cloud.mdb.mysql.v1alpha.GetUserRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.mysql.v1alpha.GetUserRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_name', full_name='yandex.cloud.mdb.mysql.v1alpha.GetUserRequest.user_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=63\362\3071\r[a-zA-Z0-9_]*', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=297,
  serialized_end=397,
)


_LISTUSERSREQUEST = _descriptor.Descriptor(
  name='ListUsersRequest',
  full_name='yandex.cloud.mdb.mysql.v1alpha.ListUsersRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.mysql.v1alpha.ListUsersRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page_size', full_name='yandex.cloud.mdb.mysql.v1alpha.ListUsersRequest.page_size', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372\3071\0060-1000', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page_token', full_name='yandex.cloud.mdb.mysql.v1alpha.ListUsersRequest.page_token', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\212\3101\005<=100', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=399,
  serialized_end=513,
)


_LISTUSERSRESPONSE = _descriptor.Descriptor(
  name='ListUsersResponse',
  full_name='yandex.cloud.mdb.mysql.v1alpha.ListUsersResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='users', full_name='yandex.cloud.mdb.mysql.v1alpha.ListUsersResponse.users', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next_page_token', full_name='yandex.cloud.mdb.mysql.v1alpha.ListUsersResponse.next_page_token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=515,
  serialized_end=612,
)


_CREATEUSERREQUEST = _descriptor.Descriptor(
  name='CreateUserRequest',
  full_name='yandex.cloud.mdb.mysql.v1alpha.CreateUserRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.mysql.v1alpha.CreateUserRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_spec', full_name='yandex.cloud.mdb.mysql.v1alpha.CreateUserRequest.user_spec', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=614,
  serialized_end=734,
)


_CREATEUSERMETADATA = _descriptor.Descriptor(
  name='CreateUserMetadata',
  full_name='yandex.cloud.mdb.mysql.v1alpha.CreateUserMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.mysql.v1alpha.CreateUserMetadata.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_name', full_name='yandex.cloud.mdb.mysql.v1alpha.CreateUserMetadata.user_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=736,
  serialized_end=795,
)


_UPDATEUSERREQUEST = _descriptor.Descriptor(
  name='UpdateUserRequest',
  full_name='yandex.cloud.mdb.mysql.v1alpha.UpdateUserRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.mysql.v1alpha.UpdateUserRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_name', full_name='yandex.cloud.mdb.mysql.v1alpha.UpdateUserRequest.user_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=63\362\3071\r[a-zA-Z0-9_]*', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='yandex.cloud.mdb.mysql.v1alpha.UpdateUserRequest.update_mask', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='password', full_name='yandex.cloud.mdb.mysql.v1alpha.UpdateUserRequest.password', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\212\3101\0058-128', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='permissions', full_name='yandex.cloud.mdb.mysql.v1alpha.UpdateUserRequest.permissions', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=798,
  serialized_end=1044,
)


_UPDATEUSERMETADATA = _descriptor.Descriptor(
  name='UpdateUserMetadata',
  full_name='yandex.cloud.mdb.mysql.v1alpha.UpdateUserMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.mysql.v1alpha.UpdateUserMetadata.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_name', full_name='yandex.cloud.mdb.mysql.v1alpha.UpdateUserMetadata.user_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1046,
  serialized_end=1105,
)


_DELETEUSERREQUEST = _descriptor.Descriptor(
  name='DeleteUserRequest',
  full_name='yandex.cloud.mdb.mysql.v1alpha.DeleteUserRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.mysql.v1alpha.DeleteUserRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_name', full_name='yandex.cloud.mdb.mysql.v1alpha.DeleteUserRequest.user_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=63\362\3071\r[a-zA-Z0-9_]*', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1107,
  serialized_end=1210,
)


_DELETEUSERMETADATA = _descriptor.Descriptor(
  name='DeleteUserMetadata',
  full_name='yandex.cloud.mdb.mysql.v1alpha.DeleteUserMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.mysql.v1alpha.DeleteUserMetadata.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_name', full_name='yandex.cloud.mdb.mysql.v1alpha.DeleteUserMetadata.user_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1212,
  serialized_end=1271,
)


_GRANTUSERPERMISSIONREQUEST = _descriptor.Descriptor(
  name='GrantUserPermissionRequest',
  full_name='yandex.cloud.mdb.mysql.v1alpha.GrantUserPermissionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.mysql.v1alpha.GrantUserPermissionRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_name', full_name='yandex.cloud.mdb.mysql.v1alpha.GrantUserPermissionRequest.user_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=63\362\3071\r[a-zA-Z0-9_]*', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='permission', full_name='yandex.cloud.mdb.mysql.v1alpha.GrantUserPermissionRequest.permission', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1274,
  serialized_end=1456,
)


_GRANTUSERPERMISSIONMETADATA = _descriptor.Descriptor(
  name='GrantUserPermissionMetadata',
  full_name='yandex.cloud.mdb.mysql.v1alpha.GrantUserPermissionMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.mysql.v1alpha.GrantUserPermissionMetadata.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_name', full_name='yandex.cloud.mdb.mysql.v1alpha.GrantUserPermissionMetadata.user_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1458,
  serialized_end=1526,
)


_REVOKEUSERPERMISSIONREQUEST = _descriptor.Descriptor(
  name='RevokeUserPermissionRequest',
  full_name='yandex.cloud.mdb.mysql.v1alpha.RevokeUserPermissionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.mysql.v1alpha.RevokeUserPermissionRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_name', full_name='yandex.cloud.mdb.mysql.v1alpha.RevokeUserPermissionRequest.user_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=63\362\3071\r[a-zA-Z0-9_]*', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='database_name', full_name='yandex.cloud.mdb.mysql.v1alpha.RevokeUserPermissionRequest.database_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=63\362\3071\016[a-zA-Z0-9_-]*', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1529,
  serialized_end=1697,
)


_REVOKEUSERPERMISSIONMETADATA = _descriptor.Descriptor(
  name='RevokeUserPermissionMetadata',
  full_name='yandex.cloud.mdb.mysql.v1alpha.RevokeUserPermissionMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.mysql.v1alpha.RevokeUserPermissionMetadata.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_name', full_name='yandex.cloud.mdb.mysql.v1alpha.RevokeUserPermissionMetadata.user_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1699,
  serialized_end=1768,
)

_LISTUSERSRESPONSE.fields_by_name['users'].message_type = yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1alpha_dot_user__pb2._USER
_CREATEUSERREQUEST.fields_by_name['user_spec'].message_type = yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1alpha_dot_user__pb2._USERSPEC
_UPDATEUSERREQUEST.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_UPDATEUSERREQUEST.fields_by_name['permissions'].message_type = yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1alpha_dot_user__pb2._PERMISSION
_GRANTUSERPERMISSIONREQUEST.fields_by_name['permission'].message_type = yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1alpha_dot_user__pb2._PERMISSION
DESCRIPTOR.message_types_by_name['GetUserRequest'] = _GETUSERREQUEST
DESCRIPTOR.message_types_by_name['ListUsersRequest'] = _LISTUSERSREQUEST
DESCRIPTOR.message_types_by_name['ListUsersResponse'] = _LISTUSERSRESPONSE
DESCRIPTOR.message_types_by_name['CreateUserRequest'] = _CREATEUSERREQUEST
DESCRIPTOR.message_types_by_name['CreateUserMetadata'] = _CREATEUSERMETADATA
DESCRIPTOR.message_types_by_name['UpdateUserRequest'] = _UPDATEUSERREQUEST
DESCRIPTOR.message_types_by_name['UpdateUserMetadata'] = _UPDATEUSERMETADATA
DESCRIPTOR.message_types_by_name['DeleteUserRequest'] = _DELETEUSERREQUEST
DESCRIPTOR.message_types_by_name['DeleteUserMetadata'] = _DELETEUSERMETADATA
DESCRIPTOR.message_types_by_name['GrantUserPermissionRequest'] = _GRANTUSERPERMISSIONREQUEST
DESCRIPTOR.message_types_by_name['GrantUserPermissionMetadata'] = _GRANTUSERPERMISSIONMETADATA
DESCRIPTOR.message_types_by_name['RevokeUserPermissionRequest'] = _REVOKEUSERPERMISSIONREQUEST
DESCRIPTOR.message_types_by_name['RevokeUserPermissionMetadata'] = _REVOKEUSERPERMISSIONMETADATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetUserRequest = _reflection.GeneratedProtocolMessageType('GetUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERREQUEST,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.GetUserRequest)
  })
_sym_db.RegisterMessage(GetUserRequest)

ListUsersRequest = _reflection.GeneratedProtocolMessageType('ListUsersRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTUSERSREQUEST,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.ListUsersRequest)
  })
_sym_db.RegisterMessage(ListUsersRequest)

ListUsersResponse = _reflection.GeneratedProtocolMessageType('ListUsersResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTUSERSRESPONSE,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.ListUsersResponse)
  })
_sym_db.RegisterMessage(ListUsersResponse)

CreateUserRequest = _reflection.GeneratedProtocolMessageType('CreateUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEUSERREQUEST,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.CreateUserRequest)
  })
_sym_db.RegisterMessage(CreateUserRequest)

CreateUserMetadata = _reflection.GeneratedProtocolMessageType('CreateUserMetadata', (_message.Message,), {
  'DESCRIPTOR' : _CREATEUSERMETADATA,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.CreateUserMetadata)
  })
_sym_db.RegisterMessage(CreateUserMetadata)

UpdateUserRequest = _reflection.GeneratedProtocolMessageType('UpdateUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEUSERREQUEST,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.UpdateUserRequest)
  })
_sym_db.RegisterMessage(UpdateUserRequest)

UpdateUserMetadata = _reflection.GeneratedProtocolMessageType('UpdateUserMetadata', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEUSERMETADATA,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.UpdateUserMetadata)
  })
_sym_db.RegisterMessage(UpdateUserMetadata)

DeleteUserRequest = _reflection.GeneratedProtocolMessageType('DeleteUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEUSERREQUEST,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.DeleteUserRequest)
  })
_sym_db.RegisterMessage(DeleteUserRequest)

DeleteUserMetadata = _reflection.GeneratedProtocolMessageType('DeleteUserMetadata', (_message.Message,), {
  'DESCRIPTOR' : _DELETEUSERMETADATA,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.DeleteUserMetadata)
  })
_sym_db.RegisterMessage(DeleteUserMetadata)

GrantUserPermissionRequest = _reflection.GeneratedProtocolMessageType('GrantUserPermissionRequest', (_message.Message,), {
  'DESCRIPTOR' : _GRANTUSERPERMISSIONREQUEST,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.GrantUserPermissionRequest)
  })
_sym_db.RegisterMessage(GrantUserPermissionRequest)

GrantUserPermissionMetadata = _reflection.GeneratedProtocolMessageType('GrantUserPermissionMetadata', (_message.Message,), {
  'DESCRIPTOR' : _GRANTUSERPERMISSIONMETADATA,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.GrantUserPermissionMetadata)
  })
_sym_db.RegisterMessage(GrantUserPermissionMetadata)

RevokeUserPermissionRequest = _reflection.GeneratedProtocolMessageType('RevokeUserPermissionRequest', (_message.Message,), {
  'DESCRIPTOR' : _REVOKEUSERPERMISSIONREQUEST,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.RevokeUserPermissionRequest)
  })
_sym_db.RegisterMessage(RevokeUserPermissionRequest)

RevokeUserPermissionMetadata = _reflection.GeneratedProtocolMessageType('RevokeUserPermissionMetadata', (_message.Message,), {
  'DESCRIPTOR' : _REVOKEUSERPERMISSIONMETADATA,
  '__module__' : 'yandex.cloud.mdb.mysql.v1alpha.user_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1alpha.RevokeUserPermissionMetadata)
  })
_sym_db.RegisterMessage(RevokeUserPermissionMetadata)


DESCRIPTOR._options = None
_GETUSERREQUEST.fields_by_name['cluster_id']._options = None
_GETUSERREQUEST.fields_by_name['user_name']._options = None
_LISTUSERSREQUEST.fields_by_name['cluster_id']._options = None
_LISTUSERSREQUEST.fields_by_name['page_size']._options = None
_LISTUSERSREQUEST.fields_by_name['page_token']._options = None
_CREATEUSERREQUEST.fields_by_name['cluster_id']._options = None
_CREATEUSERREQUEST.fields_by_name['user_spec']._options = None
_UPDATEUSERREQUEST.fields_by_name['cluster_id']._options = None
_UPDATEUSERREQUEST.fields_by_name['user_name']._options = None
_UPDATEUSERREQUEST.fields_by_name['password']._options = None
_DELETEUSERREQUEST.fields_by_name['cluster_id']._options = None
_DELETEUSERREQUEST.fields_by_name['user_name']._options = None
_GRANTUSERPERMISSIONREQUEST.fields_by_name['cluster_id']._options = None
_GRANTUSERPERMISSIONREQUEST.fields_by_name['user_name']._options = None
_GRANTUSERPERMISSIONREQUEST.fields_by_name['permission']._options = None
_REVOKEUSERPERMISSIONREQUEST.fields_by_name['cluster_id']._options = None
_REVOKEUSERPERMISSIONREQUEST.fields_by_name['user_name']._options = None
_REVOKEUSERPERMISSIONREQUEST.fields_by_name['database_name']._options = None

_USERSERVICE = _descriptor.ServiceDescriptor(
  name='UserService',
  full_name='yandex.cloud.mdb.mysql.v1alpha.UserService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1771,
  serialized_end=3224,
  methods=[
  _descriptor.MethodDescriptor(
    name='Get',
    full_name='yandex.cloud.mdb.mysql.v1alpha.UserService.Get',
    index=0,
    containing_service=None,
    input_type=_GETUSERREQUEST,
    output_type=yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1alpha_dot_user__pb2._USER,
    serialized_options=b'\202\323\344\223\002@\022>/managed-mysql/v1alpha/clusters/{cluster_id}/users/{user_name}',
  ),
  _descriptor.MethodDescriptor(
    name='List',
    full_name='yandex.cloud.mdb.mysql.v1alpha.UserService.List',
    index=1,
    containing_service=None,
    input_type=_LISTUSERSREQUEST,
    output_type=_LISTUSERSRESPONSE,
    serialized_options=b'\202\323\344\223\0024\0222/managed-mysql/v1alpha/clusters/{cluster_id}/users',
  ),
  _descriptor.MethodDescriptor(
    name='Create',
    full_name='yandex.cloud.mdb.mysql.v1alpha.UserService.Create',
    index=2,
    containing_service=None,
    input_type=_CREATEUSERREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\0027\"2/managed-mysql/v1alpha/clusters/{cluster_id}/users:\001*\262\322*\032\n\022CreateUserMetadata\022\004User',
  ),
  _descriptor.MethodDescriptor(
    name='Update',
    full_name='yandex.cloud.mdb.mysql.v1alpha.UserService.Update',
    index=3,
    containing_service=None,
    input_type=_UPDATEUSERREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\002C2>/managed-mysql/v1alpha/clusters/{cluster_id}/users/{user_name}:\001*\262\322*\032\n\022UpdateUserMetadata\022\004User',
  ),
  _descriptor.MethodDescriptor(
    name='Delete',
    full_name='yandex.cloud.mdb.mysql.v1alpha.UserService.Delete',
    index=4,
    containing_service=None,
    input_type=_DELETEUSERREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\002@*>/managed-mysql/v1alpha/clusters/{cluster_id}/users/{user_name}\262\322*+\n\022DeleteUserMetadata\022\025google.protobuf.Empty',
  ),
  _descriptor.MethodDescriptor(
    name='GrantPermission',
    full_name='yandex.cloud.mdb.mysql.v1alpha.UserService.GrantPermission',
    index=5,
    containing_service=None,
    input_type=_GRANTUSERPERMISSIONREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\002S\"N/managed-mysql/v1alpha/clusters/{cluster_id}/users/{user_name}:grantPermission:\001*\262\322*#\n\033GrantUserPermissionMetadata\022\004User',
  ),
  _descriptor.MethodDescriptor(
    name='RevokePermission',
    full_name='yandex.cloud.mdb.mysql.v1alpha.UserService.RevokePermission',
    index=6,
    containing_service=None,
    input_type=_REVOKEUSERPERMISSIONREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\002T\"O/managed-mysql/v1alpha/clusters/{cluster_id}/users/{user_name}:revokePermission:\001*\262\322*$\n\034RevokeUserPermissionMetadata\022\004User',
  ),
])
_sym_db.RegisterServiceDescriptor(_USERSERVICE)

DESCRIPTOR.services_by_name['UserService'] = _USERSERVICE

# @@protoc_insertion_point(module_scope)
