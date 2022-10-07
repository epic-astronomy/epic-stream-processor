"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class empty(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___empty = empty

class epic_image(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEADER_FIELD_NUMBER: builtins.int
    IMAGE_CUBE_FIELD_NUMBER: builtins.int
    header: builtins.str
    """full fits header dumped into a string"""
    image_cube: builtins.bytes
    """numpy ndarray"""
    def __init__(
        self,
        *,
        header: builtins.str = ...,
        image_cube: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["header", b"header", "image_cube", b"image_cube"]) -> None: ...

global___epic_image = epic_image