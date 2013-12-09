#include <Python.h>
#include <unistd.h>

static PyObject* hang(PyObject* self, PyObject* args)
{
    const int i;

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

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef hangmodule = {
  PyModuleDef_HEAD_INIT,
  "hang",           /* name of module */
  "A module that sleeps",  /* Doc string (may be NULL) */
  -1,                 /* Size of per-interpreter state or -1 */
  HangMethods       /* Method table */
};

PyMODINIT_FUNC
PyInit_hang(void)
{
    return PyModule_Create(&hangmodule);
}
#else
PyMODINIT_FUNC
inithang(void)
{
    (void) Py_InitModule("hang", HangMethods);
}
#endif
