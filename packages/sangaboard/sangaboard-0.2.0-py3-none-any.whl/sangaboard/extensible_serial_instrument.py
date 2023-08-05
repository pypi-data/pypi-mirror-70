# -*- coding: utf-8 -*-
"""
This module has been modified from the chopped-out of class from nplab_.
It is a serial instrument class to simplify the process of interfacing with 
equipment that talks on a serial port.  The idea is that your instrument can
subclass :class:`ExtensibleSerialInstrument` and provide methods to control the
hardware, which will mostly consist of `self.query()` commands. It also has
options for adding OptionalModules so that you don't have to have multiple
classes for lots of instruments with different configurations

The :class:`QueriedProperty` class is a convenient shorthand to create a property
that is read and/or set with a single serial query (i.e. a read followed by a write).

.. module_author: Richard Rowman (c) 2017, released under GNU GPL
.. _nplab: http://www.github.com/nanophotonics/nplab
"""


from __future__ import division
import re
from functools import partial
import threading
import serial
from serial import FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
from serial import PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE
from serial import STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO
import io
import time
import logging
import warnings


class ExtensibleSerialInstrument(object):
    """
    An instrument that communicates by sending strings back and forth over serial

    This base class provides commonly-used mechanisms that support the use of
    serial instruments.  Most interactions with this class involve
    a call to the `query` method.  This writes a message and returns the reply.
    This has been hacked together from the nplab_ MessageBusInstrument and SerialInstrument
    classes.
    
    **Threading Notes**
    
    The message bus protocol includes a property, `communications_lock`.  All
    commands that use the communications bus should be protected by this lock.
    It's also permissible to use it to protect sequences of calls to the bus 
    that must be atomic (e.g. a multi-part exchange of messages).  However, try
    not to hold it too long - or odd things might happen if other threads are 
    blocked for a long time.  The lock is reentrant so there's no issue with
    acquiring it twice.
    """

    termination_character = (
        "\n"
    )  #: All messages to or from the instrument end with this character.
    termination_line = (
        None
    )  #: If multi-line responses are recieved, they must end with this string
    ignore_echo = False
    port_settings = {}

    def __init__(self, port=None, **kwargs):
        """
        Set up the serial port and so on.
        """
        logging.info("Updating ESI port settings")
        logging.debug(kwargs)
        self.port_settings.update(kwargs)
        logging.info("Opening ESI connection to port {}".format(port))
        self.open(port, False)  # Eventually this shouldn't rely on init...
        logging.info("Opened ESI connection to port {}".format(port))

    def open(self, port=None, quiet=True):
        """Open communications with the serial port.
        
        If no port is specified, it will attempt to autodetect.  If quiet=True
        then we don't warn when ports are opened multiple times.
        """
        with self.communications_lock:
            if hasattr(self, "_ser") and self._ser.isOpen():
                if not quiet:
                    logging.warning("Attempted to open an already-open port!")
                return
            if port is None:
                port = self.find_port()
            assert (
                port is not None
            ), "We don't have a serial port to open, meaning you didn't specify a valid port.  Are you sure the instrument is connected?"
            logging.info("Creating serial.Serial instance...")
            self._ser = serial.Serial(port, **self.port_settings)
            logging.info(f"Created {self._ser}")
            # the block above wraps the serial IO layer with a text IO layer
            # this allows us to read/write in neat lines.  NB the buffer size must
            # be set to 1 byte for maximum responsiveness.
            assert (
                self.test_communications()
            ), "The instrument doesn't seem to be responding.  Did you specify the right port?"

    def close(self):
        """Cleanly close the device. Includes proper logging statements."""
        logging.debug("Closing serial connection")
        with self.communications_lock:
            try:
                self._ser.close()
            except Exception as e:
                logging.warning("The serial port didn't close cleanly: {}".format(e))
            logging.debug("Connection closed")

    def __del__(self):
        """Emergency close the device. Try to avoid having to use this."""
        if hasattr(self, "_ser") and self._ser.isOpen():
            with self.communications_lock:
                print(
                    "Closing an open serial communication has been triggered by garbage collection!\n"
                    "Please close this device more sensibly in future."
                )
                try:
                    self._ser.close()
                except Exception as e:
                    print("The serial port didn't close cleanly: {}".format(e))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Cleanly close down the instrument at end of a with block."""
        self.close()

    def write(self, query_string):
        """Write a string to the serial port"""
        with self.communications_lock:
            assert (
                self._ser.isOpen()
            ), "Attempted to write to the serial port before it was opened.  Perhaps you need to call the 'open' method first?"
            logging.debug("Encoding message...")
            data = query_string + self.termination_character
            data = data.encode()
            logging.debug(f"Writing message: {data}")
            self._ser.write(data)
            logging.debug("Write successful")

    def flush_input_buffer(self):
        """Make sure there's nothing waiting to be read, and clear the buffer if there is."""
        with self.communications_lock:
            if self._ser.inWaiting() > 0:
                self._ser.flushInput()

    def readline(self, timeout=None):
        """Read one line from the serial port."""
        self._ser.timeout = timeout
        with self.communications_lock:
            return (
                self._ser.readline()
                .decode("utf8")
                .replace(self.termination_character, "\n")
            )

    _communications_lock = None

    @property
    def communications_lock(self):
        """A lock object used to protect access to the communications bus"""
        # This requires initialisation but our init method won't be called - so
        # the property initialises it on first use.
        if self._communications_lock is None:
            self._communications_lock = threading.RLock()
        return self._communications_lock

    def read_multiline(self, termination_line=None, timeout=None):
        """Read one line from the underlying bus.  Must be overriden.

        This should not need to be reimplemented unless there's a more efficient
        way of reading multiple lines than multiple calls to readline()."""
        with self.communications_lock:
            if termination_line is None:
                termination_line = self.termination_line
            assert isinstance(
                termination_line, str
            ), "If you perform a multiline query, you must specify a termination line either through the termination_line keyword argument or the termination_line property of the NPSerialInstrument."
            response = ""
            last_line = "dummy"
            while (
                termination_line not in last_line and len(last_line) > 0
            ):  # read until we get the termination line.
                last_line = self.readline(timeout)
                response += last_line
            return response

    def query(self, queryString, multiline=False, termination_line=None, timeout=None):
        """
        Write a string to the stage controller and return its response.

        It will block until a response is received.  The multiline and termination_line commands
        will keep reading until a termination phrase is reached.
        """
        with self.communications_lock:
            self.flush_input_buffer()
            logging.debug(f"Writing query: {queryString}")
            self.write(queryString)
            logging.debug("Waiting for query response...")
            if self.ignore_echo == True:  # Needs Implementing for a multiline read!
                first_line = self.readline(timeout).strip()
                if first_line == queryString:
                    return self.readline(timeout).strip()
                else:
                    logging.info("This command did not echo!!!")
                    return first_line

            if termination_line is not None:
                multiline = True
            if multiline:
                return self.read_multiline(termination_line)
            else:
                line = self.readline(
                    timeout
                ).strip()  # question: should we strip the final newline?
                return line

    def parsed_query(
        self,
        query_string,
        response_string=r"%d",
        re_flags=0,
        parse_function=None,
        **kwargs,
    ):
        """
        Perform a query, returning a parsed form of the response.

        First query the instrument with the given query string, then compare
        the response against a template.  The template may contain text and
        placeholders (e.g. %i and %f for integer and floating point values
        respectively).  Regular expressions are also allowed - each group is
        considered as one item to be parsed.  However, currently it's not
        supported to use both % placeholders and regular expressions at the
        same time.

        If placeholders %i, %f, etc. are used, the returned values are
        automatically converted to integer or floating point, otherwise you
        must specify a parsing function (applied to all groups) or a list of
        parsing functions (applied to each group in turn).
        """

        response_regex = response_string
        noop = lambda x: x  # placeholder null parse function
        placeholders = [ #tuples of (regex matching placeholder, regex to replace it with, parse function)
            (r"%c", r".", noop),
            (r"%(\d+)c", r".{\1}", noop), #TODO support %cn where n is a number of chars
            (r"%d", r"[-+]?\\d+", int),
            (r"%[eEfg]", r"[-+]?(?:\\d+(?:\.\\d*)?|\.\\d+)(?:[eE][-+]?\\d+)?", float),
            (r"%i", r"[-+]?(?:0[xX][\\dA-Fa-f]+|0[0-7]*|\\d+)", lambda x: int(x, 0)), #0=autodetect base
            (r"%o", r"[-+]?[0-7]+", lambda x: int(x, 8)), #8 means octal
            (r"%s", r"\\s+", noop),
            (r"%u", r"\\d+", int),
            (r"%[xX]", r"[-+]?(?:0[xX])?[\\dA-Fa-f]+", lambda x: int(x, 16)), #16 forces hexadecimal
        ]
        matched_placeholders = []
        for placeholder, regex, parse_fun in placeholders:
            response_regex = re.sub(
                placeholder, "(" + regex + ")", response_regex
            )  # substitute regex for placeholder
            matched_placeholders.extend(
                [
                    (parse_fun, m.start())
                    for m in re.finditer(placeholder, response_string)
                ]
            )  # save the positions of the placeholders
        if parse_function is None:
            parse_function = [
                f for f, s in sorted(matched_placeholders, key=lambda m: m[1])
            ]  # order parse functions by their occurrence in the original string
        if not hasattr(parse_function, "__iter__"):
            parse_function = [parse_function]  # make sure it's a list.

        reply = self.query(query_string, **kwargs)  # do the query
        # if match this could be because another response entered the buffer between write and read. Sleep for short while then
        # check if something is now in the buffer, while the buffer is not empty repeat regex
        waited = False
        res = re.search(response_regex, reply, flags=re_flags)
        while res is None:
            if not waited:
                time.sleep(0.1)
                waited = True
                original_reply = reply
            if self._ser.inWaiting():
                reply = self.readline().strip()
                res = re.search(response_regex, reply, flags=re_flags)
                if res is not None:
                    warnings.warn(
                        "Query suceeded after initially receieving unmatched response ('%s') to '%s'. Match pattern /%s/ (generated regex /%s/)"
                        % (
                            original_reply,
                            query_string,
                            response_string,
                            response_regex,
                        ),
                        RuntimeWarning,
                    )
            else:
                raise ValueError(
                    "Stage response to '%s' ('%s') wasn't matched by /%s/ (generated regex /%s/)"
                    % (query_string, original_reply, response_string, response_regex)
                )
        try:
            parsed_result = [
                f(g) for f, g in zip(parse_function, res.groups())
            ]  # try to apply each parse function to its argument
            if len(parsed_result) == 1:
                return parsed_result[0]
            else:
                return parsed_result
        except ValueError:
            logging.info("Matched Groups: {}".format(res.groups()))
            logging.info("Parsing Functions {}:".format(parse_function))
            raise ValueError(
                "Stage response to %s ('%s') couldn't be parsed by the supplied function"
                % (query_string, reply)
            )

    def int_query(self, query_string, **kwargs):
        """Perform a query and return the result(s) as integer(s) (see parsedQuery)"""
        return self.parsed_query(query_string, "%d", **kwargs)

    def float_query(self, query_string, **kwargs):
        """Perform a query and return the result(s) as float(s) (see parsedQuery)"""
        return self.parsed_query(query_string, "%f", **kwargs)

    def test_communications(self):
        """Check if the device is available on the current port.  
        
        This should be overridden by subclasses.  Assume the port has been
        successfully opened and the settings are as defined by self.port_settings.
        Usually this function sends a command and checks for a known reply."""
        with self.communications_lock:
            return True

    def find_port(self):
        """Iterate through the available serial ports and query them to see
        if our instrument is there."""
        print("Auto-scanning ports")
        with self.communications_lock:
            success = False
            # Loop through serial ports, apparently 256 is the limit?!
            for port_name, _, _ in serial.tools.list_ports.comports():
                try:
                    logging.info("Trying port {}".format(port_name))
                    self.open(port_name)
                    success = True
                    logging.info("Success!")
                except:
                    pass
                finally:
                    try:
                        self.close()
                    except:
                        pass  # we don't care if there's an error closing the port...
                if success:
                    break  # again, make sure this happens *after* closing the port
            if success:
                return port_name
            else:
                return None


class OptionalModule(object):
    """This allows a `ExtensibleSerialInstrument` to have optional features.

    OptionalModule is designed as a base class
    for interfacing with optional modules which may or may not be included with
    the serial instrument, and can be added or removed at run-time.
    """

    def __init__(
        self, available, parent=None, module_type="Undefined", model="Generic"
    ):
        assert (
            type(available) is bool
        ), "Option module availablity should be a boolean not a {}".format(
            type(available)
        )
        self._available = available
        self._parent = parent
        assert (
            type(module_type) is str
        ), "Option module type should be a string not a {}".format(type(module_type))
        self.module_type = module_type
        if available:
            assert (
                type(model) is str
            ), "Option module type should be a string not a {}".format(type(model))
            self.model = model
        else:
            self.model = None

    @property
    def available(self):
        return self._available

    def confirm_available(self):
        """Check if module is available, no return, will raise exception if not available!"""
        assert self._available, 'No "{}" supported on firmware'.format(self.module_type)

    def describe(self):
        """Consistently spaced desciption for listing modules"""
        return self.module_type + " " * (25 - len(self.module_type)) + "- " + self.model


class QueriedProperty(object):
    """A Property interface that reads and writes from the instrument on the bus.
    
    This returns a property-like (i.e. a descriptor) object.  You can use it
    in a class definition just like a property.  The property it creates will
    interact with the instrument over the communication bus to set and retrieve
    its value.  It uses calls to `ExtensibleSerialInstrument.parsed_query` to set or
    get the value of the property.
    
    `QueriedProperty` can be used to define properties on a `ExtensibleSerialInstrument`
    or an `OptionalModule` (in which case the `ExtensibleSerialInstrument.parsed_query`
    method of the parent object will be used).
    
    Arguments:

    :get_cmd:
        the string sent to the instrument to obtain the value
    :set_cmd:
        the string used to set the value (use {} or % placeholders)
    :validate:
        a list of allowable values
    :valrange:
        a maximum and minimum value
    :fdel:
        a function to call when it's deleted
    :doc:
        the docstring
    :response_string:
        supply a % code (as you would for response_string in a
        ``ExtensibleSerialInstrument.parsed_query``)
    :ack_writes:
        set to "readline" to discard a line of input after writing.
    """

    def __init__(
        self,
        get_cmd=None,
        set_cmd=None,
        validate=None,
        valrange=None,
        fdel=None,
        doc=None,
        response_string=None,
        ack_writes="no",
    ):
        self.response_string = response_string
        self.get_cmd = get_cmd
        self.set_cmd = set_cmd
        self.validate = validate
        self.valrange = valrange
        self.fdel = fdel
        self.ack_writes = ack_writes
        self.__doc__ = doc

    # TODO: standardise the return (single value only vs parsed result), consider bool
    def __get__(self, obj, objtype=None):
        if issubclass(type(obj), OptionalModule):
            obj.confirm_available()
            obj = obj._parent
        if obj is None:
            return self
        assert issubclass(type(obj), ExtensibleSerialInstrument)
        if self.get_cmd is None:
            raise AttributeError("unreadable attribute")
        # Allow certain "magic" values to set the response string
        for key, val in [("float", r"%f"), ("int", r"%d")]:
            if self.response_string == key:
                self.response_string = val
        if self.response_string in ["bool", "raw", None]:
            value = obj.query(self.get_cmd)
            if self.response_string == "bool":
                value = bool(value)
        else:
            value = obj.parsed_query(self.get_cmd, self.response_string)
        return value

    def __set__(self, obj, value):
        if issubclass(type(obj), OptionalModule):
            obj.confirm_available()
            obj = obj._parent
        assert issubclass(type(obj), ExtensibleSerialInstrument)
        if self.set_cmd is None:
            raise AttributeError("can't set attribute")
        if self.validate is not None:
            if value not in self.validate:
                raise ValueError(
                    "invalid value supplied - value must be one of {}".format(
                        self.validate
                    )
                )
        if self.valrange is not None:
            if value < min(self.valrange) or value > max(self.valrange):
                raise ValueError(
                    "invalid value supplied - value must be in the range {}-{}".format(
                        *self.valrange
                    )
                )
        message = self.set_cmd
        if "{0" in message:
            message = message.format(value)
        elif "%" in message:
            message = message % value
        obj.write(message)
        if self.ack_writes == "readline":
            obj.readline()

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)
