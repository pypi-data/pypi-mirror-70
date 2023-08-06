# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from copy import deepcopy
from typing import Any, Set, Type

from dial_core.utils.exceptions import InvalidPortTypeError, PortNotConnectedError
from dial_core.utils.log import DEBUG, ERROR, log_on_end, log_on_error


class Port:
    """The Port class provides a connection point between different nodes.

    A Port object allows two types of connections:
        * one-to-one: This Port can be only connected to another port.
        * many-to-many: This Port can be connected to multiple ports, and multiple ports
            can be connected to this one.

    A Port object also has an associated Type. Two Port objects can only be connected if
    they share the same Type.

    Attributes:
        name: The name (identifier) of the port. Can't be changed once the Port is
            created.
        port_type: The type of this port. A Port object can only be connected to other
            Ports that share its same type.
        connections: Set with all the Ports this port is currently connected to.
        compatible_port_classes: Set of Port subclasses that are compatible (and can be
            connected) with this port if they share the same type.
        node: The Node object this Port belongs to, if any.
        allows_multiple_connections: A boolean option, indicating the type of connection
        this port allows (one-to-one or many-to-many)
    """

    def __init__(
        self, name: str, port_type: Any, allows_multiple_connections: bool = True
    ):
        self._name = name
        self._port_type = port_type
        self._connected_to: Set["Port"] = set()  # Avoid repeated ports
        self.compatible_port_classes: Set[Type["Port"]] = set([Port])

        self.node = None  # type: ignore

        self.allows_multiple_connections = allows_multiple_connections

    @property
    def name(self) -> str:
        """Returns the name (identifier) of the port."""
        return self._name

    @property
    def port_type(self) -> Any:
        """Returns the Type allowed by this port.

        Used to check which ports can be connected between them.
        """
        return self._port_type

    @property
    def connections(self) -> Set["Port"]:
        """Returns the ports this port is currently connected.

        Shouldn't be manipulated directly. Use the `connect_to`, `disconnect_from`
        functions to handle port connections.

        Returns:
           A set with all the Ports connected to this port.
        """
        return self._connected_to

    def is_compatible_with(self, port: "Port") -> bool:
        """Checks if this port is compatible with another port.

        Two ports are compatible if they're of the same type and don't belong to the
        same node.

        Args:
            port: Port being compared with.
        """
        return (
            self._port_type == port.port_type
            and (not self.node or self.node != port.node)
            and type(port) in self.compatible_port_classes
        )

    @log_on_end(DEBUG, "{self} connected to {port}")
    @log_on_error(ERROR, "Error on connection: {e}", on_exceptions=(ValueError))
    def connect_to(self, port: "Port"):
        """Connects the current port to another port.

        Its a two way connection (the two ports will be connected to each other)

        Examples:
            a = Port()
            b = Port()
            a.connect_to(b) # now, `a` is in `b.connections`, and `b` in `a.connections`

        Args:
            port: `Port` object being connected to.

        Raises:
            ValueError: If the port is connected to itself.
            ValueError: If the ports aren't compatible (can't be connected).
        """
        if port is self:  # Avoid connecting a port to itself
            raise PortNotConnectedError(f"Can't connect {port} to itself!")

        if not self.is_compatible_with(port):
            raise InvalidPortTypeError(
                f"This port ({self}) type is not compatible with the"
                f" other port. ({port})"
            )

        if not self.allows_multiple_connections:
            # Disconnect from other ports before setting the new connection
            self.clear_all_connections()

        # Two way connection (Both ports will have a reference to each other)
        self._connected_to.add(port)
        if self not in port.connections:
            port.connect_to(self)

    @log_on_end(DEBUG, "Port {self} disconnected from {port}")
    def disconnect_from(self, port: "Port"):
        """Disconnects the current port from the other port.

        Args:
            port: `Port` object being disconnect from.
        """
        if port not in self._connected_to:  # Can't remove port if not found
            return

        # Two way disconnection
        self._connected_to.discard(port)
        port.disconnect_from(self)

    @log_on_end(DEBUG, "All connections cleared on {self}")
    def clear_all_connections(self):
        """Removes all connections to this port."""
        # Use a list to avoid removing an item from self._connected_to while iterating
        for port in list(self._connected_to):
            port.disconnect_from(self)

        self._connected_to.clear()

    def word_id(self) -> str:
        """Returns a string identifier for this port. Can be used as a variable for
        notebooks."""
        return (
            (f"{self.node.title if self.node else 'none'}_{self.name}")
            .lower()
            .replace(" ", "_")
        )

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        setattr(result, "_name", deepcopy(self._name, memo))
        setattr(result, "_port_type", deepcopy(self._port_type, memo))
        setattr(result, "_connected_to", set())
        setattr(
            result,
            "compatible_port_classes",
            deepcopy(self.compatible_port_classes, memo),
        )
        setattr(result, "node", None)
        setattr(
            result,
            "allows_multiple_connections",
            deepcopy(self.allows_multiple_connections, memo),
        )

        return result

    def __getstate__(self):
        return {"connected_to": self._connected_to, "node": self.node}

    def __setstate__(self, new_state):
        self._connected_to = new_state["connected_to"]
        self.node = new_state["node"]

    def __reduce__(self):
        return (
            Port,
            (self.name, self.port_type, self.allows_multiple_connections),
            self.__getstate__(),
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.name == other.name
            and self.port_type == other.port_type
            and self.allows_multiple_connections == other.allows_multiple_connections
        )

    def __hash__(self):
        return hash((self.name, self.port_type, self.allows_multiple_connections))

    def __str__(self):
        """Retuns the string representation of the Port object."""
        type_str = (
            self.port_type.__name__
            if isinstance(self.port_type, type)
            else self.port_type
        )
        return f'{self.__class__.__name__} "{self.name}" [{type_str}]'

    def __repr__(self):
        """Returns the object representation of the Port object (with mem address)."""
        type_str = (
            self.port_type.__name__
            if isinstance(self.port_type, type)
            else self.port_type
        )
        return (
            f'{self.__class__.__name__} "{self.name}"'
            f" ({str(id(self))[:4]}...{str(id(self))[-4:]})"
            f" [{type_str}] from {self.node}"
        )
