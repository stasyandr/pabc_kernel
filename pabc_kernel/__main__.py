from ipykernel.kernelapp import IPKernelApp
from . import PabcKernel

IPKernelApp.launch_instance(kernel_class=PabcKernel)
