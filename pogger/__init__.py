import os
import h5py
import datetime as dt


class Pogger():
    def __init__(self, pogger_path=None):
        self._path = pogger_path
        self._initialise_paths()
        self._initialise_h5()

    def _initialise_paths(self):
        if self._path is None:
            self._path = os.path.expanduser("~")
            self._path += "/pogger_archives/"

        # Script name
        self._python_name = __name__
        self._path += self._python_name + "/"

        # Timestamp
        self._datetime = dt.datetime.now()
        self._datetime_string = dt.datetime.strftime(
            self._datetime,
            "%Y-%m-%dT%H-%M-%S"
        )
        self._datetime_path = dt.datetime.strftime(
            self._datetime,
            "%Y/%m/%d/%H-%M-%S/"
        )
        self._path_dir = self._path + self._datetime_path
        self._path_full = self._path_dir \
            + self._datetime_string + "_" + self._python_name
        if not os.path.exists(self._path_dir):
            os.makedirs(self._path_dir)

    def _initialise_h5(self):
        self._path_h5 = self._path_full + ".h5"
        with h5py.File(self._path_h5, "w") as file_h5:
            file_h5.create_group("data")

    def write_array(self, path, array, units=None):
        path_full = "data/" + path
        with h5py.File(self._path_h5, "w") as file_h5:
            file_h5[path_full] = array
            if units is not None:
                file_h5[path_full].attrs["units"] = units
