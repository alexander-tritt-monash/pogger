import os
import h5py
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt


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

        self._figure_path_dir = self._path_dir + "figures/"
        if not os.path.exists(self._figure_path_dir):
            os.makedirs(self._figure_path_dir)
        self._figure_path = self._figure_path_dir \
            + self._datetime_string + "_" + self._python_name + "_"

    def record(self, result_names, result_units=None):
        def write_result(result, result_name, result_unit=None):
            if type(result) is tuple:
                for result_index, result_value in enumerate(result):
                    result_name_value = result_name[result_index]
                    if result_unit is None:
                        result_unit_value = None
                    else:
                        result_unit_value = result_unit[result_index]

                    write_result(
                        result_value,
                        result_name_value,
                        result_unit_value
                    )
            elif isinstance(result, np.ndarray):
                self.write_array(result_name, result, result_unit)
            else:
                self.write_value(result_name, result, result_unit)

        def wrapper(function: callable):
            def wrapped(*arguments, **keyword_arguments):
                results = function(*arguments, **keyword_arguments)
                write_result(results, result_names, result_units)

                figure_numbers = plt.get_fignums()
                figure_labels = plt.get_figlabels()
                for figure_number, figure_label in \
                        zip(figure_numbers, figure_labels):
                    plt.figure(figure_number)
                    plt.savefig(self._figure_path + figure_label + ".png")
                    plt.savefig(self._figure_path + figure_label + ".pdf")
                return results
            return wrapped
        return wrapper

    def _initialise_h5(self):
        self._path_h5 = self._path_full + ".h5"
        with h5py.File(self._path_h5, "w"):
            pass

    def write_array(self, path, array, units=None):
        path_full = "data/" + path
        path_split = path_full.split("/")
        with h5py.File(self._path_h5, "a") as file_h5:
            path_dir = ""
            for dir_index in range(1, len(path_split) - 1):
                path_dir += path_split[dir_index] + "/"
                file_h5.require_group(path_dir[:-1])

            file_h5[path_full] = array
            if units is not None:
                file_h5[path_full].attrs["_units"] = units

    def write_value(self, path, value, units=None):
        path_full = "data/" + path
        path_split = path_full.split("/")
        with h5py.File(self._path_h5, "a") as file_h5:
            path_dir = ""
            for dir_index in range(0, len(path_split) - 1):
                path_dir += path_split[dir_index] + "/"
                file_h5.require_group(path_dir[:-1])
            file_h5[path_dir].attrs[path_split[-1]] = value
            if units is not None:
                file_h5[path_dir].attrs[path_split[-1] + "_units"] = units
