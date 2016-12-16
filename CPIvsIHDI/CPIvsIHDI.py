"""
Created on Mon Dec 12 16:16:33 2016

@author: Ruben Dorado

Merging data and creating visualizations for Bernie's paper on corruption
in development countries
"""

import csv
import numpy as np
import matplotlib.pyplot as plt

cpi_file = "CPI_2015_data.csv"
ihdi_file = "IHDI_2015_Statistical_Annex_Table_3.csv"


def load_data_table(data_url):
    """
    Import a table of country-based data from a csv format file
    """
    data_file = open(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data lines from file", data_url
    data_tokens = [line.split(',') for line in data_lines]
    return data_tokens[:-1]


def prepare_data_table():
    """
    Prepares the data for plotting
    Returns a data table which contents are the countries for which we have
    full information, in the format [[Country, CPI, IHDI, inequality index], ...]

    """
    # Trimming and formatting the CPI 2015 table
    cpi_data = load_data_table(cpi_file)
    cpi_data = cpi_data[1:]
    cpi_data_cutout = [[str(cpi_row[2]), float(cpi_row[1]), str(cpi_row[4]), str(cpi_row[3])] for cpi_row in cpi_data]

    # Trimming and formatting the IHDI 2015 table
    ihdi_data = load_data_table(ihdi_file)
    ihdi_data_cutout = []
    for ihdi_row in ihdi_data:
        if ihdi_row[0] != '' and ihdi_row[4] != '..':
            ihdi_data_cutout.append([str(ihdi_row[1]),
                                     round(float(ihdi_row[4]), 4),
                                     round(float(ihdi_row[10]), 2)])

    # Merging both data tables and creating the final data table
    # fields are [Country, CPI, IHDI, inequality index, wbcode, region]
    # The data file contains only the countries with literal coincidence in
    # Their names and with all the data available
    return [[cpi_row[0], cpi_row[1], ihdi_row[1], ihdi_row[2], cpi_row[2], cpi_row[3]] for ihdi_row in ihdi_data_cutout for cpi_row in cpi_data_cutout if cpi_row[0] == ihdi_row[0]]


def print_data_table():
    """
    Saves the data table created with prepare_data_table() to a csv file
    """
    data_table = prepare_data_table()
    data_table.insert(0, ['Country', 'CPI', 'IHDI', 'inequality index', 'wbcode', 'region'])

    with open('CPItoIHDI.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        [writer.writerow(row) for row in data_table]

def statistical_analysis(x_serie, y_serie):
    """
    Code for statistical analysis goes here

    It's enough here just to print the data on screen
    """


    # Import the data in a ready format
    cpi_to_ihdi_data = prepare_data_table()
    print "Number of cases with full information:", len(cpi_to_ihdi_data)

    # Defining the data series for the plot
    cpi_serie = [country[1] for country in cpi_to_ihdi_data]
    ihdi_serie = [country[2] for country in cpi_to_ihdi_data]
    ineq_serie = [country[3] for country in cpi_to_ihdi_data]

    # This dictionary handles the different combinations
    series = {"CPI": cpi_serie, "IHDI": ihdi_serie, "inequality": ineq_serie}

    print np.corrcoef([series[x_serie], series[y_serie]])[0][1]
    print np.polyfit(series[x_serie], series[y_serie], 3)


def plot_the_data(x_serie, y_serie, a_serie, countries=[]):
    """
    Plots the charts
    """

    # Import the data in a ready format
    cpi_to_ihdi_data = prepare_data_table()
    print "Number of cases with full information:", len(cpi_to_ihdi_data)

    # Defining the data series for the plot
    cpi_serie = [country[1] for country in cpi_to_ihdi_data]
    ihdi_serie = [country[2] for country in cpi_to_ihdi_data]
    ineq_serie = [country[3] for country in cpi_to_ihdi_data]

    # This dictionary handles the different combinations
    series = {"CPI": cpi_serie, "IHDI": ihdi_serie, "inequality": ineq_serie}

    # This table locates the labels for the specified countries
    labels = []
    for country in countries:
        for line in range(len(cpi_to_ihdi_data)):
            if country == cpi_to_ihdi_data[line][0]:
                labels.append([country,
                               series[x_serie][line],
                               series[y_serie][line]])

    # Tweaking the circle weight to make it more significant


    # Creating the plot
    plt.scatter(series[x_serie],
                series[y_serie],
                s=series[a_serie],
                c=cpi_serie,
                alpha=0.65,
                label=y_serie + ' to ' + x_serie)

    plt.xlabel(x_serie)
    plt.ylabel(y_serie)
    plt.title(y_serie + ' to ' + x_serie)
    plt.grid(b=True)

    for label in labels:
        plt.annotate(
            label[0],
            xy = (label[1], label[2]),
            xytext = (-10, 20),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.2', fc = 'cyan', alpha = 0.3),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    plt.show()

### Running the functions

#print_data_table()
countries_to_label = ["Denmark",
                      "Italy",
                      "Uruguay",
                      "Rwanda",
                      "Bhutan",
                      "Spain",
                      "United Arab Emirates",
                      "Argentina",
                      "Russian Federation",
                      "United States of America"]
#plot_the_data("IHDI", "CPI", "inequality", countries=countries_to_label)
#plot_the_data("inequality", "CPI", "inequality", countries_to_label)
#plot_the_data("inequality", "IHDI", "inequality", countries_to_label)
statistical_analysis("IHDI", "CPI")
statistical_analysis("inequality", "CPI")
statistical_analysis("IHDI", "inequality")