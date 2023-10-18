import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import os
import matplotlib.patches as mpatches

def plot_barplot(data: pd.DataFrame, x_axis: pd.Series, y_axis: pd.Series, sem_values: pd.Series, x_axis_2: pd.Series, individual_points: pd.Series, y_label: str, save_path:str):
    """Create a barplot with error bars and individual points, and save it as a file

    Args:
        data (pd.DataFrame): data frame of the data for the graph
        x_axis (pd.Series): groups for the x axis for the bars
        y_axis (pd.Series): length of the y axis (mean)
        sem_values (pd.Series): sem of the y axis for error bars
        x_axis_2 (pd.Series): groups of the x axis for the individual points
        individual_points (pd.Series): individual values
        y_label (str): name for the y axis
        save_path (str): path to the directory to save the files
    """    
    fig, ax = plt.subplots()

    # Determine the colors based on the save_path
    if "females" in os.path.split(save_path)[0]:  
        colors = ["lightgrey", "lightpink"]
    elif "males" in os.path.split(save_path)[0]:  
        colors = ["white", "cornflowerblue"]
    else:
        # Default colors or raise an error if neither 'males' nor 'females' is found
        colors = ["moccasin", "cornflowerblue"]  # or you can raise an error or use some default colors

    ax = sns.barplot(x = x_axis, y = y_axis, data = data, palette = colors, errorbar = None)
    # Set the edgecolor for all bars
    [edge.set_edgecolor("black") for edge in ax.patches]

    # Manually adding error bars:
    for i, sem in enumerate(sem_values):
        ax.errorbar(i, y_axis.iloc[i], yerr = sem, fmt = "none", capsize = 5, color = "black")
    # Add indiviual data points
    for i, category in enumerate(x_axis.unique()): # Assuming x_axis is a column in data with unique categories
        y_values = individual_points[x_axis_2 == category]
        x_values = np.random.normal(loc = i, scale = 0.1, size = (len(y_values))) # random jitter (0.1) for all individual points (not spread on a straight line)
        ax.scatter(x_values, y_values, color = "black")

     # Remove x-axis labels (ticks and tick labels)
    ax.set_xticks([])  # This will remove the ticks
    ax.set_xticklabels([])  # This will remove the tick labels
    # Create custom legend handles
    legend_handles = [mpatches.Patch(facecolor=color, label=label, edgecolor="black", linewidth=1.0) for color, label in zip(colors, x_axis.unique())]
    # Add the legend to the plot
    ax.legend(handles=legend_handles, loc='upper right')  # You can adjust the legend's location with the 'loc' parameter

    # Set title and x and y axis labels
    ax.set_xlabel("")
    ax.set_ylabel(y_label)

    # Show and save the plot
    plt.show()
    print("saving graph...")
    fig.savefig(save_path, dpi=300)