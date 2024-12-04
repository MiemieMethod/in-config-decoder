# perfect

This library implements the custom serialization format used in Infinity Nikki.

## Installation

```console
pip install -U git+https://github.com/NikkiTools/perfect.git
```

Or clone the repository, and run the following command in the cloned directory:

```console
pip install -e .
```

## License

`perfect` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Documentation

This library just implements the serialization format itself. Notably, it does not come with any type definitions for the objects the game serializes; These have to be provided seperately. The base classes `SerializableObject` and `SerializableUnion` respectively represent the base form of the different types of game objects, which you should overwrite when creating your own classes.

Another noteworthy addition is that the config table serialization omits the data tags alongside some other unnecessary information, serialization of these types should have the respective `read/write_tag` and `read/write_size` parameters set to `False` when calling methods on the ByteBuf.
