#include <pybind11/pybind11.h>
void dll_binding(pybind11::module_&);

#include "../../a_dll/a_dll.h"

PYBIND11_MODULE(mydll, m)
{
    m.doc() = "mydll binding";

    m.def("myprint", [](){

        Cadll a;
    });

}