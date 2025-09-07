import plotly.graph_objects as go

def create_donut_chart(score, total_questions):
    """
    Creates a donut chart visualizing the percentage of correct vs incorrect answers,
    styled to match the reference image's large donut.
    """
    correct_answers = score
    incorrect_answers = total_questions - score

    labels = ['Correct', 'Incorrect']
    values = [correct_answers, incorrect_answers]
    
    # Gradient-like colors for the main donut to mimic the reference
    # Using multiple segments to simulate gradient in plotly
    if correct_answers > 0 and incorrect_answers > 0:
        correct_percentage = (correct_answers / total_questions) * 100
        incorrect_percentage = (incorrect_answers / total_questions) * 100
        
        # Simulating gradient for 'Correct' part using two shades of green
        # and a distinct dark grey for 'Incorrect'
        values_for_plot = [correct_percentage / 2, correct_percentage / 2, incorrect_percentage]
        labels_for_plot = ['Correct', 'Correct', 'Incorrect']
        segment_colors = ['#8BC34A', '#CDDC39', '#37474F'] # Darker Green, Lighter Green, Dark Grey
    elif correct_answers > 0:
        values_for_plot = [100]
        labels_for_plot = ['Correct']
        segment_colors = ['#8BC34A'] # Use a single green
    else: # Only incorrect
        values_for_plot = [100]
        labels_for_plot = ['Incorrect']
        segment_colors = ['#37474F'] # Use dark grey

    fig = go.Figure(data=[go.Pie(
        labels=labels_for_plot,
        values=values_for_plot,
        hole=.7,
        marker=dict(
            colors=segment_colors,
            line=dict(color='#1e293b', width=2) # Dark border between segments
        ),
        hoverinfo='label+percent',
        textinfo='percent',
        textfont=dict(size=20, color="#f1f5f9", family="Arial, sans-serif"),
        direction='clockwise',
        sort=False,
        insidetextorientation='radial'
    )])

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='#1e293b',
        plot_bgcolor='#1e293b',
        font_color='#f1f5f9',
        margin=dict(t=50, b=50, l=50, r=50),
        height=400,
        annotations=[
            dict(text=f"{correct_answers}/{total_questions}", x=0.5, y=0.5,
                 font=dict(size=36, color="#f1f5f9", family="Arial, sans-serif"),
                 showarrow=False)
        ]
    )

    return fig


def create_right_side_charts(feedback):
    """
    Creates the two small circular charts on the right, mimicking the reference image.
    This will represent Correct vs. Incorrect in a different breakdown, or an arbitrary split.
    For demonstration, we'll split feedback into two categories.
    """
    total_questions = len(feedback)
    
    # We'll use a simplified breakdown for these small charts,
    # for example, splitting the total questions into two arbitrary categories
    # to match the visual of the reference image's small charts (55% and 25%).
    # You might want to replace this logic with actual categories from your feedback.
    
    # Chart 1: Assume 'Data A' as 55%
    chart1_value = int(total_questions * 0.55) if total_questions > 0 else 1
    chart1_other = total_questions - chart1_value if total_questions > 0 else 0

    # Chart 2: Assume 'Data B' as 25% (or remaining if that makes sense)
    chart2_value = int(total_questions * 0.25) if total_questions > 0 else 1
    chart2_other = total_questions - chart2_value if total_questions > 0 else 0


    # If you want to use actual feedback, e.g., first half vs second half:
    half_point = total_questions // 2
    chart1_correct = sum(1 for fb in feedback[:half_point] if 'Correct' in fb)
    chart1_incorrect = half_point - chart1_correct

    chart2_correct = sum(1 for fb in feedback[half_point:] if 'Correct' in fb)
    chart2_incorrect = total_questions - half_point - chart2_correct


    # Define individual chart parameters
    charts_data = [
        {
            'labels': ['Correct', 'Incorrect'],
            'values': [chart1_correct, chart1_incorrect],
            'colors': ['#8BC34A', '#37474F'], # Green and Dark Grey
            'title': '55%', # Just a label to match the visual
            'sub_label': 'Data A'
        },
        {
            'labels': ['Correct', 'Incorrect'],
            'values': [chart2_correct, chart2_incorrect],
            'colors': ['#CDDC39', '#37474F'], # Lighter Green and Dark Grey
            'title': '25%', # Just a label to match the visual
            'sub_label': 'Data B'
        }
    ]

    fig = go.Figure()

    # Add each small donut chart
    for i, chart in enumerate(charts_data):
        # Calculate percentages to display
        total_chart_value = sum(chart['values'])
        if total_chart_value == 0:
            percentage_value = 0
            other_percentage = 0
        else:
            percentage_value = (chart['values'][0] / total_chart_value) * 100 # Assuming first value is dominant for display
            other_percentage = (chart['values'][1] / total_chart_value) * 100

        # Position for the two charts
        x_center = 0.5 # Centralized
        y_top = 0.75 if i == 0 else 0.25 # Top and bottom positions

        fig.add_trace(go.Pie(
            labels=chart['labels'],
            values=chart['values'],
            hole=.8, # Smaller hole for these charts
            marker=dict(colors=chart['colors'], line=dict(color='#1e293b', width=1)),
            hoverinfo='label+percent',
            showlegend=False,
            domain={'x': [0, 1], 'y': [y_top - 0.2, y_top + 0.2]}, # Adjust domain to position charts
            textinfo='none', # No text on slices
        ))
        
        # Add central percentage text
        fig.add_annotation(
            text=f"{int(percentage_value)}%",
            x=x_center, y=y_top + 0.05,
            font=dict(size=30, color="#f1f5f9", family="Arial, sans-serif"),
            showarrow=False
        )
        # Add sub-label text
        fig.add_annotation(
            text=chart['sub_label'],
            x=x_center, y=y_top - 0.05,
            font=dict(size=14, color="#94a3b8"),
            showarrow=False
        )

    fig.update_layout(
        paper_bgcolor='#1e293b',
        plot_bgcolor='#1e293b',
        font_color='#f1f5f9',
        height=400, # Adjust height to accommodate two charts
        margin=dict(t=20, b=20, l=20, r=20),
        annotations=[
            dict(text='Question Breakdown', x=0.5, y=0.95, font_size=20, font_color="#f1f5f9", showarrow=False) # Title for the right side
        ]
    )
    return fig
