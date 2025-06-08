import json
import matplotlib.pyplot as plt
import pandas as pd  # Required to create the table
from matplotlib.backends.backend_pdf import PdfPages  # Required for saving to PDF
from pathlib import Path # Required to check and create directories
    
def generate_equipment_report(report_dir, report_json):
    """
    This function takes in JSON data and generates a report with:
    - Pie chart (Equipment Status Distribution)
    - Bar chart (Number of Unique Equipment Worn by Each Person)
    - Table (Partial Equipment Missing Items)
    
    It returns the path to the generated PDF.

    Args:
    - data (dict): JSON data containing the detections and file info.

    Returns:
    - str: Path to the generated PDF file.
    """
    data = json.loads(report_json)
    # Total equipment list
    all_equipment = {"Helmet", "Gloves", "Goggles", "Boots", "Vest"}

    # Function to get the number of unique equipment for each person
    def count_equipment(detections):
        person_equipment_count = {}

        for person, equipment in detections.items():
            # Convert the equipment list to a set to remove duplicates
            unique_equipment = set(equipment)  # Removes duplicates (e.g., "Helmet", "Helmet" -> "Helmet")
            person_equipment_count[person] = unique_equipment  # Store the unique equipment list

        return person_equipment_count

    # Get the equipment count for each person
    person_equipment_count = count_equipment(data['detections'])

    # Prepare data for the bar graph
    persons = list(person_equipment_count.keys())
    equipment_counts = [len(equipment) for equipment in person_equipment_count.values()]

    # Calculate the number of people with all, partial, and no equipment
    all_equipment_count = len(all_equipment)
    all_equip_count = 0
    partial_equip_count = 0
    no_equip_count = 0
    partial_equipment_data = []  # For storing partial equipment persons and missing equipment

    for person, equipment in person_equipment_count.items():
        missing_equipment = all_equipment - equipment  # What is missing
        if len(equipment) == all_equipment_count:
            all_equip_count += 1
        elif len(equipment) == 0:
            no_equip_count += 1
        else:
            partial_equip_count += 1
            if missing_equipment:
                partial_equipment_data.append({
                    "Person": person,
                    "Missing Equipment": list(missing_equipment)
                })

    # Prepare data for the pie chart
    labels = ['All Equipment', 'Partial Equipment', 'No Equipment']
    sizes = [all_equip_count, partial_equip_count, no_equip_count]
    colors = ['#4CAF50', '#FFEB3B', '#F44336']  # Green, Yellow, Red

    # Filter out 0% categories
    labels_filtered = []
    sizes_filtered = []
    colors_filtered = []

    for i in range(len(sizes)):
        if sizes[i] > 0:
            labels_filtered.append(labels[i])
            sizes_filtered.append(sizes[i])
            colors_filtered.append(colors[i])

    # Add new functionality: checking if "Person" appears more than 15% of data for a person
    bar_colors = []
    for person, equipment in data['detections'].items():
        # Count how many "Person" entries are in the list
        person_count = equipment.count("Person")
        
        # Calculate the total entries for the person (i.e., total detections)
        total_entries = len(equipment)
        
        # Calculate percentage of "Person" entries
        person_percentage = (person_count / total_entries) * 100
        
        # If "Person" entries are more than 15%, color the bar red
        if person_percentage > 15:
            bar_colors.append('red')
        else:
            bar_colors.append('skyblue')

    # Create reports directory in /backend if it doesn't exist
    

# Assuming data['file'] is a string and complete_path is a Path object
    file_name = Path(data['file']).stem
    pdf_path = report_dir / f"{file_name}_report.pdf"


    # Plotting the Ring Pie Chart and Bar Chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Ring Pie Chart (with filtered labels)
    ax1.pie(sizes_filtered, labels=labels_filtered, colors=colors_filtered, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
    ax1.set_title('Equipment Status Distribution')

    # Bar Chart for unique equipment count
    ax2.bar(persons, equipment_counts, color=bar_colors)
    ax2.set_xlabel('Persons')
    ax2.set_ylabel('Number of Unique Equipment Items')
    ax2.set_title('Number of Unique Equipment Worn by Each Person')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    ax2.set_ylim(0, all_equipment_count)  # y-axis limit from 0 to max number of equipment
    ax2.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better visibility

    # Adjust layout to give space for the table
    plt.subplots_adjust(bottom=0.4)  # Adjust bottom margin to give space for the table

    # Add the table below the plot
    if partial_equipment_data:
        # Create the table below the plot
        table_data = []
        for entry in partial_equipment_data:
            table_data.append([entry['Person'], ', '.join(entry['Missing Equipment'])])

        # Add table to the figure
        table_columns = ['Person', 'Missing Equipment']
        table_ax = fig.add_axes([0.1, 0.02, 0.8, 0.2])  # Move the table lower
        table = table_ax.table(cellText=table_data, colLabels=table_columns, loc='center', cellLoc='center', colColours=['#f5f5f5']*2)

        # Hide axes for table
        table_ax.axis('off')

    # Save the plots to a PDF in /backend/reports directory
    with PdfPages(pdf_path) as pdf:
        pdf.savefig(fig)  # Save the figure as a page in the PDF
        plt.close(fig)  # Close the plot after saving

    # Return the path to the generated PDF
    return pdf_path
