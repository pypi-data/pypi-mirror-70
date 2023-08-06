import logging
import uuid
from configparser import ConfigParser
from os import path

import kubernetes
import yaml
from flask import Blueprint, jsonify, request, Response
from kubernetes import client, config
from kubernetes.client.rest import ApiException

services = Blueprint('services', __name__)

# Configuration to connect to k8s.
if not path.exists('/.dockerenv'):
    config.load_kube_config()
else:
    config.load_incluster_config()

# create instances of the API classes
api_customobject = client.CustomObjectsApi()
api_core = client.CoreV1Api()

config_parser = ConfigParser()
configuration = config_parser.read('config.ini')
group = config_parser.get('resources', 'group')  # str | The custom resource's group name
version = config_parser.get('resources', 'version')  # str | The custom resource's version
namespace = config_parser.get('resources', 'namespace')  # str | The custom resource's namespace
plural = config_parser.get('resources',
                           'plural')  # str | The custom resource's plural name. For TPRs this


@services.route('/init', methods=['POST'])
def init_execution():
    """
    Initialize the execution when someone call to the execute endpoint in brizo.
    swagger_from_file: docs/init.yml
    """
    execution_id = generate_new_id()
    body = create_execution(request.json['workflow'], execution_id)
    try:
        api_response = api_customobject.create_namespaced_custom_object(group, version, namespace,
                                                                        plural, body)
        logging.info(api_response)
        return execution_id, 200

    except ApiException as e:
        logging.error(
            f'Exception when calling CustomObjectsApi->create_namespaced_custom_object: {e}')
        return 'Workflow could not start', 400


@services.route('/stop', methods=['DELETE'])
def stop_execution():
    """
    Stop the current workflow execution.
    swagger_from_file: docs/stop.yml
    """
    name = request.args['executionId']  # str | the custom object's name
    body = kubernetes.client.V1DeleteOptions()  # V1DeleteOptions |
    grace_period_seconds = 56  # int | The duration in seconds before the object should be
    # deleted. Value must be non-negative integer. The value zero indicates delete immediately.
    # If this value is nil, the default grace period for the specified type will be used.
    # Defaults to a per object value if not specified. zero means delete immediately. (optional)
    orphan_dependents = True  # bool | Deprecated: please use the PropagationPolicy, this field
    # will be deprecated in 1.7. Should the dependent objects be orphaned. If true/false,
    # the \"orphan\" finalizer will be added to/removed from the object's finalizers list. Either
    # this field or PropagationPolicy may be set, but not both. (optional)
    propagation_policy = 'propagation_policy_example'  # str | Whether and how garbage collection
    # will be performed. Either this field or OrphanDependents may be set, but not both. The
    # default policy is decided by the existing finalizer set in the metadata.finalizers and the
    # resource-specific default policy. (optional)

    try:
        api_response = api_customobject.delete_namespaced_custom_object(group, version, namespace,
                                                                        plural, name, body,
                                                                        grace_period_seconds=grace_period_seconds,
                                                                        orphan_dependents=orphan_dependents,
                                                                        propagation_policy=propagation_policy)
        logging.info(api_response)
    except ApiException as e:
        print("Exception when calling CustomObjectsApi->delete_namespaced_custom_object: %s\n" % e)
    return 'Successfully delete', 200


@services.route('/info/<execution_id>', methods=['GET'])
def get_execution_info(execution_id):
    """
    Get info for an execution id.
    swagger_from_file: docs/execution_info.yml
    """
    try:
        api_response = api_customobject.get_namespaced_custom_object(group, version, namespace,
                                                                     plural,
                                                                     execution_id)
        logging.info(api_response)
        return yaml.dump(api_response), 200
    except ApiException as e:
        logging.error(f'The executionId {execution_id} is not registered in your namespace.')
        return f'The executionId {execution_id} is not registered in your namespace.', 400


@services.route('/list', methods=['GET'])
def list_executions():
    """
    List all the execution workflows.
    swagger_from_file: docs/list_executions.yml
    """
    try:
        api_response = api_customobject.list_namespaced_custom_object(group, version, namespace,
                                                                      plural)
        result = list()
        for i in api_response['items']:
            result.append(i['metadata']['name'])
        logging.info(api_response)
        return jsonify(result), 200

    except ApiException as e:
        logging.error(
            f'Exception when calling CustomObjectsApi->list_cluster_custom_object: {e}')
        return 'Error listing workflows', 400


@services.route('/logs', methods=['GET'])
def get_logs():
    """
    Get the logs for an execution id.
    swagger_from_file: docs/logs.yml
    """
    data = request.args
    required_attributes = [
        'executionId',
        'component'
    ]
    try:
        execution_id = data.get('executionId')
        component = data.get('component')
        # First we need to get the name of the pods
        label_selector = f'workflow={execution_id},component={component}'
        logging.debug(f'Looking pods in ns {namespace} with labels {label_selector}')
        pod_response = api_core.list_namespaced_pod(namespace, label_selector=label_selector)
    except ApiException as e:
        logging.error(
            f'Exception when calling CustomObjectsApi->list_namespaced_pod: {e}')
        return 'Error getting the logs', 400

    try:
        pod_name = pod_response.items[0].metadata.name
        logging.debug(f'pods found: {pod_response}')
    except IndexError as e:
        logging.warning(f'Exception getting information about the pod with labels {label_selector}.'
                        f' Probably pod does not exist')
        return f'Pod with workflow={execution_id} and component={component} not found', 404

    try:
        logging.debug(f'looking logs for pod {pod_name} in namespace {namespace}')
        logs_response = api_core.read_namespaced_pod_log(name=pod_name, namespace=namespace)
        r = Response(response=logs_response, status=200, mimetype="text/plain")
        r.headers["Content-Type"] = "text/plain; charset=utf-8"
        return r

    except ApiException as e:
        logging.error(
            f'Exception when calling CustomObjectsApi->read_namespaced_pod_log: {e}')
        return 'Error getting the logs', 400


def create_execution(workflow, execution_id):
    execution = dict()
    execution['apiVersion'] = group + '/' + version
    execution['kind'] = 'WorkFlow'
    execution['metadata'] = dict()
    execution['metadata']['name'] = execution_id
    execution['metadata']['namespace'] = namespace
    execution['metadata']['labels'] = dict()
    execution['metadata']['labels']['workflow'] = execution_id
    execution['spec'] = dict()
    execution['spec']['metadata'] = workflow
    return execution


# TODO Use the commons utils library to do this when we set up the project.
def generate_new_id():
    """
    Generate a new id without prefix.
    :return: Id, str
    """
    return uuid.uuid4().hex
