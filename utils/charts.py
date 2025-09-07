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
    Creates a visually appealing pie chart showing the breakdown of answers.
    """
    correct = sum(1 for fb in feedback if '✅ Correct' in fb)
    incorrect = sum(1 for fb in feedback if '❌ Incorrect' in fb)
    skipped = sum(1 for fb in feedback if 'Skipped' in fb)

    labels = ['Correct', 'Incorrect', 'Skipped']
    values = [correct, incorrect, skipped]
    colors = ['#8BC34A', '#F44336', '#607D8B'] # Green, Red, Grey

    # Filter out categories with zero values to avoid cluttering the chart
    final_labels = [label for i, label in enumerate(labels) if values[i] > 0]
    final_values = [value for value in values if value > 0]
    final_colors = [color for i, color in enumerate(colors) if values[i] > 0]

    if not final_values: # Handle case where there is no feedback
        return go.Figure()

    fig = go.Figure(data=[go.Pie(
        labels=final_labels,
        values=final_values,
        hole=.6,
        marker=dict(
            colors=final_colors,
            line=dict(color='#1e293b', width=2)
        ),
        hoverinfo='label+percent+value',
        textinfo='percent',
        textfont=dict(size=16, color='white'),
        pull=[0.05 if v > 0 else 0 for v in final_values] # Slightly pull out slices
    )])

    fig.update_layout(
        title=dict(text='Question Breakdown', x=0.5, font=dict(size=20)),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#f1f5f9',
        margin=dict(t=60, b=60, l=20, r=20),
        height=400,
    )
    
    return fig

