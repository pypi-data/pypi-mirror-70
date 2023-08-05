# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from yandex.cloud.loadbalancer.v1 import network_load_balancer_pb2 as yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__pb2
from yandex.cloud.loadbalancer.v1 import network_load_balancer_service_pb2 as yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2


class NetworkLoadBalancerServiceStub(object):
  """A set of methods for managing NetworkLoadBalancer resources.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Get = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/Get',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.GetNetworkLoadBalancerRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__pb2.NetworkLoadBalancer.FromString,
        )
    self.List = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/List',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.ListNetworkLoadBalancersRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.ListNetworkLoadBalancersResponse.FromString,
        )
    self.Create = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/Create',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.CreateNetworkLoadBalancerRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )
    self.Update = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/Update',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.UpdateNetworkLoadBalancerRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )
    self.Delete = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/Delete',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.DeleteNetworkLoadBalancerRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )
    self.Start = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/Start',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.StartNetworkLoadBalancerRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )
    self.Stop = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/Stop',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.StopNetworkLoadBalancerRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )
    self.AttachTargetGroup = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/AttachTargetGroup',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.AttachNetworkLoadBalancerTargetGroupRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )
    self.DetachTargetGroup = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/DetachTargetGroup',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.DetachNetworkLoadBalancerTargetGroupRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )
    self.GetTargetStates = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/GetTargetStates',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.GetTargetStatesRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.GetTargetStatesResponse.FromString,
        )
    self.AddListener = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/AddListener',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.AddNetworkLoadBalancerListenerRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )
    self.RemoveListener = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/RemoveListener',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.RemoveNetworkLoadBalancerListenerRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )
    self.ListOperations = channel.unary_unary(
        '/yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService/ListOperations',
        request_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.ListNetworkLoadBalancerOperationsRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.ListNetworkLoadBalancerOperationsResponse.FromString,
        )


class NetworkLoadBalancerServiceServicer(object):
  """A set of methods for managing NetworkLoadBalancer resources.
  """

  def Get(self, request, context):
    """Returns the specified NetworkLoadBalancer resource.

    Get the list of available NetworkLoadBalancer resources by making a [List] request.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def List(self, request, context):
    """Retrieves the list of NetworkLoadBalancer resources in the specified folder.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Create(self, request, context):
    """Creates a network load balancer in the specified folder using the data specified in the request.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Update(self, request, context):
    """Updates the specified network load balancer.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Delete(self, request, context):
    """Deletes the specified network load balancer.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Start(self, request, context):
    """Starts load balancing and health checking with the specified network load balancer with specified settings.
    Changes network load balancer status to `` ACTIVE ``.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Stop(self, request, context):
    """Stops load balancing and health checking with the specified network load balancer.
    Changes load balancer status to `` STOPPED ``.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AttachTargetGroup(self, request, context):
    """Attaches a target group to the specified network load balancer.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DetachTargetGroup(self, request, context):
    """Detaches the target group from the specified network load balancer.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetTargetStates(self, request, context):
    """Gets states of target resources in the attached target group.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddListener(self, request, context):
    """Adds a listener to the specified network load balancer.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemoveListener(self, request, context):
    """Removes the listener from the specified network load balancer.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListOperations(self, request, context):
    """Lists operations for the specified network load balancer.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_NetworkLoadBalancerServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Get': grpc.unary_unary_rpc_method_handler(
          servicer.Get,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.GetNetworkLoadBalancerRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__pb2.NetworkLoadBalancer.SerializeToString,
      ),
      'List': grpc.unary_unary_rpc_method_handler(
          servicer.List,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.ListNetworkLoadBalancersRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.ListNetworkLoadBalancersResponse.SerializeToString,
      ),
      'Create': grpc.unary_unary_rpc_method_handler(
          servicer.Create,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.CreateNetworkLoadBalancerRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
      'Update': grpc.unary_unary_rpc_method_handler(
          servicer.Update,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.UpdateNetworkLoadBalancerRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
      'Delete': grpc.unary_unary_rpc_method_handler(
          servicer.Delete,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.DeleteNetworkLoadBalancerRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
      'Start': grpc.unary_unary_rpc_method_handler(
          servicer.Start,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.StartNetworkLoadBalancerRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
      'Stop': grpc.unary_unary_rpc_method_handler(
          servicer.Stop,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.StopNetworkLoadBalancerRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
      'AttachTargetGroup': grpc.unary_unary_rpc_method_handler(
          servicer.AttachTargetGroup,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.AttachNetworkLoadBalancerTargetGroupRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
      'DetachTargetGroup': grpc.unary_unary_rpc_method_handler(
          servicer.DetachTargetGroup,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.DetachNetworkLoadBalancerTargetGroupRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
      'GetTargetStates': grpc.unary_unary_rpc_method_handler(
          servicer.GetTargetStates,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.GetTargetStatesRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.GetTargetStatesResponse.SerializeToString,
      ),
      'AddListener': grpc.unary_unary_rpc_method_handler(
          servicer.AddListener,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.AddNetworkLoadBalancerListenerRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
      'RemoveListener': grpc.unary_unary_rpc_method_handler(
          servicer.RemoveListener,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.RemoveNetworkLoadBalancerListenerRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
      'ListOperations': grpc.unary_unary_rpc_method_handler(
          servicer.ListOperations,
          request_deserializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.ListNetworkLoadBalancerOperationsRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_loadbalancer_dot_v1_dot_network__load__balancer__service__pb2.ListNetworkLoadBalancerOperationsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'yandex.cloud.loadbalancer.v1.NetworkLoadBalancerService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
