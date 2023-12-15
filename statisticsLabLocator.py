from pubmedarticle import PubmedArticle
from typing import List
from collections import Counter
from request import Request

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd
import json



def articlecount_per_region(all_articles_data: List[PubmedArticle]):
    attribute_counts = Counter(x.last_author.country for x in all_articles_data if
                               x.last_author is not None and x.last_author.region is not None)
    return attribute_counts


def generate_collection_statics_image(article_count_per_region, similarities, functions_timing,request: Request):
    """Replaced by heatmap_generator"""
    # first plot (Plot 1) worldmap of count of articles per country
    df = pd.DataFrame(article_count_per_region.items(), columns=['Country', 'Count'])

    # Load the world shapefile
    world = gpd.read_file('data/GeoMapData/ne_110m_admin_0_countries.shp')

    # Load the GeoInformation JSON file containing country-region mappings
    with open('data/GeoInformation.json', 'r') as geo_file:
        geo_data = json.load(geo_file)

    # Get countries belonging to the selected ROI (e.g., Europe)
    roi_countries = [country['Country'] for country in geo_data if country['Region'] == request.region_of_interest]

    # Filter the world map for countries present in the ROI
    world_roi = world[world['NAME'].isin(roi_countries)]

    # Merge the world shapefile with the DataFrame containing ROI countries' data
    world = world_roi.merge(df, left_on='NAME', right_on='Country', how='left')

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
    fig = plt.figure(figsize=(10, 6))

    # Add Plot 1 to the top subplot
    ax1 = plt.subplot()
    ax1.set_facecolor('white')  # Set background color to white
    world.boundary.plot(ax=ax1, color='green', linewidth=0.2)
    world.plot(column='Count', cmap='YlGnBu', ax=ax1)
    for x, y, label in zip(top_countries.geometry.centroid.x, top_countries.geometry.centroid.y,
                           top_countries['Count']):
        ax1.text(x, y, f'{label:.0f}', fontsize=8, ha='center', va='center', color='black')
    ax1.set_title(f'Top {top_n} Countries with the most references')
    ax1.set_xticks([])
    ax1.set_yticks([])

    ax1.set_aspect('equal')

    # Create a separate legend for the colorbar for Plot 1
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


def heatmap_generator(request: Request, article_count_per_region):
    data = pd.DataFrame(article_count_per_region.items(), columns=['Country', 'Count'])

    # Dictionary mapping regions to their bounding box coordinates
    regions = {
        'Europe': (-25, 50, 35, 75),
        'North America': (-170, -20, 5, 90),
        'South/Latin America': (-100, -30, -60, 30),
        'Africa': (-25, 55, -40, 40),
        'Arab States': (-25, 60, 10, 40),
        'Asia & Pacific': (30, 185, -60, 75),
        'Middle east':(25,70,5,40)
    }

    # Load the world map using GeoPandas
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    region = request.region_of_interest

    if region in regions:
         bbox = regions[region]
         # Create a figure and axis
         fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figsize as needed

         # Set the extent of the plot based on the bounding box coordinates
         ax.set_xlim(bbox[0], bbox[1])  # Adjust the x-axis limits for longitude
         ax.set_ylim(bbox[2], bbox[3])  # Adjust the y-axis limits for latitude

         # Plot the entire world map
         world.plot(ax=ax, edgecolor='black',color='lightgrey',linewidth=0.5)

         # Get countries belonging to the selected ROI (e.g., Europe)

         with open('data/GeoInformation.json', 'r') as geo_file:
             geo_data = json.load(geo_file)

         roi_countries = [country['Country'] for country in geo_data if country['Region'] == region]

         region_count_data = data[data['Country'].isin(roi_countries)]

         merged = world.merge(region_count_data, how='left', left_on='name', right_on='Country')

         # Plot the world map for the selected region
         world.boundary.plot(ax=ax, color='black', linewidth=0.5)

         # Plot the heatmap based on count values for the selected countries
         merged.plot(column='Count', ax=ax, legend=True, cmap='YlOrRd', edgecolor='black')

         for idx, row in merged.iterrows():
             if not pd.isnull(row['Count']):  # Check if count value exists
                 label_point = row['geometry'].representative_point()
                 plt.annotate(text=f'{int(row["Count"])}', xy=(label_point.x, label_point.y), ha='center',
                              color='black')


         ax.set_title(f'Reference count in {region}')
         plt.savefig('stats_img1.png', dpi=300, bbox_inches='tight')
         statistics_image = ['stats_img1.png']

    return statistics_image





