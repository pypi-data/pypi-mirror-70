# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from copy import deepcopy
from typing import Any, Callable, Dict, Optional

from dial_core.utils import log
from dial_core.utils.exceptions import PortNotConnectedError

from .port import Port

LOGGER = log.get_logger(__name__)


class InputPort(Port):
    """The InputPort class is a subclass of Port that only allows single connections
    to an OutputPort object.
    """

    def __init__(self, name: str, port_type: Any):
        super().__init__(name, port_type, allows_multiple_connections=False)

        from .output_port import OutputPort

        self._triggered_ports = set()

        self.compatible_port_classes.add(OutputPort)

        self._processor_function: Callable = self._default_processor_function

        self.processing = False

    @property
    def port_connected_to(self) -> Optional["Port"]:
        """Returns the port connected to this one (can be None).
        Because this is an Input Port, we can ensure it can be connected to only one (1)
        another port.

        Returns:
            The port its connected to (or None if no port connected)
        """
        if self.connections:
            return list(self.connections)[0]

        return None

    def set_processor_function(self, processor_function: Callable):
        """Sets a new processor function that will be used by this port when a new value
        is received.

        `_processor_function` needs to be a Callable that receives one argument: the
        object being processed. It can should also return the processed value.

        Raises:
            TypeError: If processor_function is not Callable.
        """
        processor_function = (
            self._default_processor_function
            if processor_function is None
            else processor_function
        )

        if not callable(processor_function):
            raise TypeError(f"{processor_function} is not callable.")

        self._processor_function = processor_function

    def process_input(self, value: Any) -> Any:
        """Processes the passed value, calling the assigned processor function for it.
        """
        if self.processing or (self.node and self.node._ports_processing >= 1):
            return value

        try:
            self.processing = True
            if self.node:
                self.node._ports_processing += 1

            value = self._processor_function(value)

            return value

        except PortNotConnectedError as err:
            LOGGER.debug(
                "%s processor function failed (%s) Details:\n%s",
                self,
                self._processor_function.__name__,
                str(err),
            )
        finally:
            if self.node:
                self.node._ports_processing -= 1

            self.processing = False

            return value

    def receive(self) -> Any:
        """Receives and processes a value.

        This value can be passed by argument or fetched directly from the connected
        OutputPort.

        Raises:
            PortNotConnectedError: If not connected to any OutputPort and a raw_value
            was not provided.
        """
        if not self.port_connected_to:
            raise PortNotConnectedError(f"{self} is not connected to any other port.")

        nvalue = self.process_input(self.port_connected_to.generate_output())

        return nvalue

    def triggers(self, output_port):
        """Add the output_port to the list of ports that are triggered when this port
        is updated."""
        self._triggered_ports.add(output_port)

    def remove_trigger(self, output_port):
        """Removes a port from the list of triggered ports."""
        self._triggered_ports.pop(output_port, None)

    def propagate(self):
        """Calls `send` for all ports."""
        for t in self._triggered_ports:
            t.send()

    def _default_processor_function(self, value: Any) -> Any:
        """Default function used for `_processor_function` when its not overriden."""
        return value

    def __deepcopy__(self, memo):
        base = super().__deepcopy__(memo)

        setattr(base, "_processor_function", deepcopy(self._processor_function, memo))

        return base

    def __getstate__(self) -> Dict[str, Any]:
        state = super().__getstate__()
        state["processor_function"] = self._processor_function

        return state

    def __setstate__(self, new_state: Dict[str, Any]):
        super().__setstate__(new_state)

        self._processor_function = new_state["processor_function"]

    def __reduce__(self):
        return (InputPort, (self.name, self.port_type), self.__getstate__())
        return (InputPort, (self.name, self.port_type), self.__getstate__())
