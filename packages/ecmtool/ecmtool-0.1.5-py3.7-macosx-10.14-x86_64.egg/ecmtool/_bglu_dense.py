def __bootstrap__():
    global __bootstrap__, __loader__, __file__
    import sys, pkg_resources, imp
    # __file__ = pkg_resources.resource_filename(__name__, '_bglu_dense.cpython-36m-x86_64-linux-gnu.so')
    __file__ = pkg_resources.resource_filename(__name__, '_bglu_dense.o')
    __loader__ = None; del __bootstrap__, __loader__
    imp.load_dynamic(__name__,__file__)
__bootstrap__()

