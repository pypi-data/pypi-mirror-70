"""
This module defines the "Dataset" class that is used to load the .csv
files holding the data to be fitted. After the fit is performed it also
stores the initial parameters, the fitted parameters and the fit
estimations.

This module also defines the function "load" used in the
"Dataset.load_c" and "Dataset.load_q" functions to load the .csv files.
"""


import pandas as pd


class Dataset:

    """Loads and stores kinetics data, also stores fit results and axes labels.

    Arguments:
        files_c (list):
            The path(s) of the concentration vs time files.
        files_q (list, optional):
            The path(s) of the charge passed vs time files, if this
            argument is not set, further fitting will proceed without
            taking the charge passed in account.
        t_label|c_label|q_label (str, optional):
            Set the corresponding attributes values. Used to set the
            x and y axes labels when plotting.
    
    Attributes:
        df_c|df_c_std|df_c_fit (pandas.DataFrame):
            Store respectively the mean concentration, the concentration
            standard deviations and the corresponding fit results.
            Defined by the load_c method or directly at initialization
            using the files_c argument.
        df_q|df_q_std|df_q_fit (pandas.DataFrame):
            Store respectively the mean charge passed, the charge passed
            standard deviations and the corresponding fit results.
            Defined by the load_q method or directly at initialization
            using the files_q argument.
        t_label|c_label|q_label (str):
            Labels to be used for the x and y axes when plotting the
            datasets.
        fit_results (lmfit.MinimizerResult):
            Stores the results of the fit, for details see the
            lmfit.minimizer.MinimizerResult documentation:
            https://lmfit.github.io/lmfit-py/fitting.html

            Defined when the fit.fit_dataset() function is run on the
            Dataset object.
        init_params (lmfit.parameter.Parameters):
            Stores the initial parameters for the fit, for details on
            this object class see:
            https://lmfit.github.io/lmfit-py/parameters.html
            
            Defined when the fit.fit_dataset() function is run on the
            Dataset object.
        names (list):
            Species names which concentration evolution over time is
            tracked. Used in particular to label the data when plotting.
            Defined in the load_c method.
    """

    def __init__(
        self,
        files_c,
        files_q = None,
        t_label = "t [s]",
        c_label = "C [M]",
        q_label = "Q [C]"
        ):
        """ Class constructor """

        # initialize attributes

        self.df_c = None
        self.df_c_std = None
        self.df_c_fit = None

        self.df_q = None
        self.df_q_std = None
        self.df_q_fit = None

        self.t_label = t_label
        self.c_label = c_label
        self.q_label = q_label

        self.names = None
        self.fit_results = None
        self.init_params = None

        # load data from list of files
        self.load_c(files_c)
        if files_q is not None: self.load_q(files_q)


    def load_c(self, files):

        """Loads / processes .csv files holding concentration over time data.

        Recommendations for the .csv file formatting: the files headers
        are formatted in this fashion: "t, species name 1, species name
        2..."; first column is time, other columns are concentrations.

        An example file can be found here: https://is.gd/GZPZFK

        Relies on the load() function from this module, see also this
        function documentation for more details.

        Arguments:
            files (list):
                Path(s) of the .csv files.
        """

        # load the files in Dataframes
        self.df_c, self.df_c_std = load(files)

        # initialize the species names
        self.names = [name for name in self.df_c.columns if name != "t"]


    def load_q(self, files):

        """Loads / processes .csv files holding charge passed over time data.

        Recommendations for the .csv file formatting: the files headers
        should be formatted in this fashion: "t,Q"; first column is the
        time, second column is the charge passed.

        An example file can be found here: https://is.gd/0Ma7Ii

        Relies on the load() function from this module, see also this
        function Docstring for more details.

        Arguments:
            files (list):
                Paths of the .csv files.
        """

        self.df_q, self.df_q_std = load(files)


def load(files):
    """Loads and processes data from .csv files, stores it in Dataframes.

    The .csv files should have the same headers, the same number of
    columns and the same number of rows. The header should be held in
    the first row.

    These .csv files are typically generated from raw data files from
    experiments using custom code to satisfy these requirements.

    Arguments:
        files (list):
            Path(s) to the file(s), each column in each file must have
            the same number of rows.

    Returns:
        pandas.DataFrame, pandas.DataFrame:
            Averages DataFrame and standard deviation DataFrame.

    """

    # load files in a list of DataFrames
    dfs = [pd.read_csv(fr"{file}") for file in files]

    # concatenate DataFrames along their rows and merge the rows with same
    # index by calculating their average or their standard deviation
    df_concat = pd.concat(dfs)
    df = df_concat.groupby(level=0).mean()
    df_std = df_concat.groupby(level=0).std()
    
    return df, df_std