"""
This module defines two functions to plot the data contained in an
object of class chemical_kinetics.data.Dataset. "plot_c" plots the
species concentration evolution over time and "plot_q" plots the charge
passed evolution over time. If no fit was performed on the dataset
object these functions only plot the raw data. If a fit was performed it
also plot the fit estimation.
"""


import matplotlib.pyplot as plt
import numpy as np


def plot_c(dataset, names = None):
    """Plots the species concentrations evolution over time and its fit.
    
    Plots the fit results only if the data has been fitted once, i.e.
    chemical_kinetics.fit.fit_dataset function was run once on the
    dataset. Else it only plots the raw data.

    Arguments:
        dataset (chemical_kinetics.data.Dataset):
            Object holding the DataFrame containing the data and the fit
            results.
        names (list, optional):
            List of names of the species concentration and fit to be 
            plotted, if None all concentrations are plotted.
    """

    # make names hold all the species names if names is None
    if names is None: names = dataset.names

    # rename variables to simplify code
    df = dataset.df_c
    df_std = dataset.df_c_std
    df_fit = dataset.df_c_fit

    # plot data
    plt.figure()
    # variable "colors" used to store the raw data plot color in order to use
    # the same color for the fit result
    colors = dict()
    for name in names:
        style = dict(
            linestyle = "none",
            marker = ".",
            label = name
            )
        # here we need to consider whether no error-bars were generated for any
        # of the raw data (i.e. only one data file was loaded when creating
        # "dataset"); if no standard deviation were generated use plot to plot
        # the data, else use error-bar to plot the data
        if np.all(np.isnan(df_std[name])):
            p = plt.plot(
                df["t"],
                df[name],
                **style
                )
        else:
            p = plt.errorbar(
                df["t"],
                df[name],
                yerr = df_std[name],
                **style
                )
        # store the plot color for the fit result plot
        colors[name] = p[0].get_color()

    # set labels and legend
    plt.xlabel(dataset.t_label)
    plt.ylabel(dataset.c_label)
    plt.legend()

    # if "dataset" contains fit result data, plot it
    if df_fit is not None:
        for name in names:
            plt.plot(
                df_fit["t"],
                df_fit[name],
                color = colors[name]
                )

    plt.show()


def plot_q(dataset):
    """Plots the charge passed over time and its fit.
    
    Plots the fit results only if the data has been fitted once, i.e.
    chemical_kinetics.fit.fit_dataset function was run once on the
    dataset. Else it only plots the raw data.

    Arguments:
        dataset (chemical_kinetics.data.Dataset):
            Object holding the DataFrame containing the data and the fit
            results.
    """

    # rename variables to simplify code
    df = dataset.df_q
    df_std = dataset.df_q_std
    df_fit = dataset.df_q_fit

    plt.figure()
    
    # use a filled area to simplify the raw data standard deviation
    # visualization
    plt.fill_between(
        df["t"],
        df["Q"] - df_std["Q"],
        df["Q"] + df_std["Q"],
        color = "C0", alpha = 0.3, lw = 0
        )

    # plot the raw data
    plt.plot(df["t"], df["Q"], label = "data")

    # if "dataset" contains fit result data, plot it
    if df_fit is not None:
        plt.plot(df_fit["t"], df_fit["Q"], "--", label = "fit")

    # set labels and legend
    plt.xlabel(dataset.t_label)
    plt.ylabel(dataset.q_label)
    plt.legend()

    plt.show()