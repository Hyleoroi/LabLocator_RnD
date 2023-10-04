from pubmedarticle import PubmedArticle
from typing import List
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd


def articlecount_per_region(all_articles_data: List[PubmedArticle]):
    attribute_counts = Counter(x.last_author.country for x in all_articles_data if
                               x.last_author is not None and x.last_author.region is not None)
    return attribute_counts


def generate_collection_statics_image(article_count_per_region, similarities, functions_timing):
    # first plot (Plot 1) worldmap of count of articles per country
    df = pd.DataFrame(article_count_per_region.items(), columns=['Country', 'Count'])

    # Load the world shapefile
    world = gpd.read_file('data/GeoMapData/ne_110m_admin_0_countries.shp')

    # Merge the world shapefile with my data
    world = world.merge(df, left_on='NAME', right_on='Country', how='left')

    # Determine the number of countries to label (e.g., top 10)
    top_n = 10
    top_countries = world.nlargest(top_n, 'Count')

    # Your second plot (Plot 2): similarity
    data_percentage = [val * 100 for val in similarities]

    # Your third plot (Plot 3)
    execution_times = [i[1] for i in functions_timing]
    labels = [i[0] for i in functions_timing]

    # Create a single figure and arrange the subplots
    # Calculate the size of the plot to match 90% of A4 landscape
    a4_width_mm = 297
    a4_height_mm = 210
    width_percentage = 0.9  # Adjust this value as needed
    fig_width = a4_width_mm * width_percentage / 25.4  # Convert mm to inches
    fig_height = a4_height_mm / 25.4  # Convert mm to inches

    # Save the plot to an image file (e.g., PNG or JPEG) with the adjusted size
    fig = plt.figure(figsize=(fig_width, fig_height))

    # Add Plot 1 to the top subplot
    ax1 = plt.subplot()
    ax1.set_facecolor('white')  # Set background color to white
    world.boundary.plot(ax=ax1, color='green', linewidth=0.2)
    world.plot(column='Count', cmap='YlGnBu', ax=ax1)
    for x, y, label in zip(top_countries.geometry.centroid.x, top_countries.geometry.centroid.y,
                           top_countries['Count']):
        ax1.text(x, y, f'{label:.0f}', fontsize=8, ha='center', va='center', color='black')
    ax1.set_title(f'Top {top_n} Countries with the most articles')
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Create a separate legend for the colorbar for Plot 1
    # TODO: layout change
    cax1 = fig.add_axes([0.90, 0.26, 0.02, 0.47])  # Adjust the values as needed
    sm1 = plt.cm.ScalarMappable(cmap='YlGnBu',
                                norm=plt.Normalize(vmin=world['Count'].min(), vmax=world['Count'].max()))
    sm1._A = []
    cbar1 = fig.colorbar(sm1, cax=cax1, orientation='vertical')
    cbar1.set_label('Country Count')

    plt.savefig('stats_img1.png', dpi=300, bbox_inches='tight')

    fig = plt.figure(figsize=(fig_width, fig_height))

    # Add Plot 2 to the second subplot
    ax2 = plt.subplot2grid((2, 1), (0, 0))
    bars = ax2.bar(range(len(data_percentage)), data_percentage, width=1.01, color='darkgreen', edgecolor='none',
                   linewidth=0, align='edge')
    ax2.set_xticklabels([])
    ax2.set_title('Similarity Map of {} Articles'.format(len(data_percentage)))
    ax2.set_ylim(0, 100)
    ax2.set_yticks(np.arange(0, 101, 10))
    ax2.yaxis.grid(True, linestyle='--', color='lightgrey', alpha=0.7)
    ax2.set_ylabel('Similarity (%)')

    # Add Plot 3 to the third subplot
    ax3 = plt.subplot2grid((2, 1), (1, 0))
    bars = ax3.bar(labels, execution_times, color='darkgreen')
    ax3.set_ylabel('Execution Time (seconds)')
    ax3.set_title('Execution Time for Different Tasks')
    for i, value in enumerate(execution_times):
        formatted_value = "{:.3f}".format(value)
        plt.text(i,value+1, str(formatted_value), ha='center', va='top')
    plt.tight_layout()

    plt.savefig('stats_img2.png', dpi=300, bbox_inches='tight')
    statistics_image = ['stats_img1.png','stats_img2.png']

    return statistics_image
