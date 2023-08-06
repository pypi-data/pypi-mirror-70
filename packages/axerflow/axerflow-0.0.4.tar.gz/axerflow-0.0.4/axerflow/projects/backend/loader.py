import entrypoints
import logging

ENTRYPOINT_GROUP_NAME = "axerflow.project_backend"

__logger__ = logging.getLogger(__name__)


# Statically register backend defined in axerflow
axerflow_BACKENDS = dict()


def load_backend(backend_name):
    # Static backends
    if backend_name in axerflow_BACKENDS:
        return axerflow_BACKENDS[backend_name]()

    # backends from plugin
    try:
        backend_builder = entrypoints.get_single(ENTRYPOINT_GROUP_NAME,
                                                 backend_name).load()
        return backend_builder()
    except entrypoints.NoSuchEntryPoint:
        # TODO Should be a error when all backends are migrated here
        available_entrypoints = entrypoints.get_group_all(
            ENTRYPOINT_GROUP_NAME)
        available_plugins = [
            entrypoint.name for entrypoint in available_entrypoints]
        __logger__.warning("Backend '%s' is not available. Available plugins are %s",
                           backend_name, available_plugins + list(axerflow_BACKENDS.keys()))

    return None
