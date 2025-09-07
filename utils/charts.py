import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_donut_chart(score, total_questions):
    """
    Creates a donut chart visualizing the percentage of correct vs incorrect answers.
    """
    correct_answers = score
    incorrect_answers = total_questions - score

    values_for_plot = []
    labels_for_plot = []
    segment_colors = []

    if correct_answers > 0:
        # Split the 'correct' value to simulate a gradient with two colors
        val1 = correct_answers / 2
        val2 = correct_answers / 2
        values_for_plot.extend([val1, val2])
        labels_for_plot.extend(['Correct', 'Correct'])
        segment_colors.extend(['#8BC34A', '#CDDC39']) # Two shades of green

    if incorrect_answers > 0:
        values_for_plot.append(incorrect_answers)
        labels_for_plot.append('Incorrect')
        segment_colors.append('#37474F') # Dark grey

    if not values_for_plot: # Handle case with 0 questions
        values_for_plot = [1]
        labels_for_plot = ['No Questions']
        segment_colors = ['#37474F']

    fig = go.Figure(data=[go.Pie(
        labels=labels_for_plot,
        values=values_for_plot,
        hole=.75,
        marker=dict(
            colors=segment_colors,
            line=dict(color='#1e293b', width=3)
        ),
        hoverinfo='label+percent',
        textinfo='none',
        direction='clockwise',
        sort=False
    )])

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#f1f5f9',
        margin=dict(t=20, b=20, l=20, r=20),
        height=400,
        annotations=[
            dict(text=f"{correct_answers}/{total_questions}", x=0.5, y=0.5,
                 font=dict(size=40, color="#f1f5f9", family="Arial, sans-serif"),
                 showarrow=False)
        ]
    )
    return fig


def create_bar_chart(feedback):
    """
    Creates a horizontal bar chart showing the count of correct and incorrect answers.
    """
    correct_answers = sum(1 for fb in feedback if '✅ Correct' in fb)
    incorrect_answers = len(feedback) - correct_answers
    
    # Define labels and values for the chart
    labels = ['Incorrect', 'Correct']
    values = [incorrect_answers, correct_answers]
    colors = ['#F44336', '#8BC34A'] # Red for incorrect, Green for correct

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=labels,
        x=values,
        orientation='h', # Make the bar chart horizontal
        marker=dict(
            color=colors,
            line=dict(color='#1e293b', width=1)
        ),
        text=values,
        textposition='outside', # Show the count outside the bar
        textfont=dict(color='#f1f5f9', size=16)
    ))

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#f1f5f9',
        margin=dict(t=40, b=40, l=20, r=20),
        height=400,
        xaxis=dict(showgrid=False, visible=False), # Hide x-axis labels and grid
        yaxis=dict(showgrid=False, automargin=True), # Hide y-axis grid
        title=dict(text='Question Breakdown', x=0.5) # Add a title to the chart
    )
    
    return fig

