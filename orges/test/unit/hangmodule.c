#include <Python.h>
#include <unistd.h>

static PyObject* hang(PyObject* self, PyObject* args)
{
    const int* i;
 
    if (!PyArg_ParseTuple(args, "i", &i))
        return NULL;
 
    sleep((unsigned int) i);
 
    Py_RETURN_NONE;
}
 
static PyMethodDef HangMethods[] =
{
     {"hang", hang, METH_VARARGS, "Hang"},
     {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
 
inithang(void)
{
     (void) Py_InitModule("hang", HangMethods);
}