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
    Creates a bar chart showing the performance for each question.
    """
    # Calculate score and total from the feedback list to maintain compatibility
    total_questions = len(feedback)
    score = sum(1 for fb in feedback if 'Correct' in fb)

    if total_questions == 0:
        correct_perc = 0
        incorrect_perc = 0
    else:
        correct_perc = round((score / total_questions) * 100)
        incorrect_perc = 100 - correct_perc

    # Create a subplot figure with 2 rows for the two pie charts
    fig = make_subplots(rows=2, cols=1, specs=[[{'type':'domain'}], [{'type':'domain'}]])

    # Chart 1: Correct Answers
    fig.add_trace(go.Pie(
        values=[correct_perc, 100 - correct_perc],
        hole=.8,
        marker=dict(colors=['#8BC34A', '#37474F']),
        textinfo='none',
        hoverinfo='none',
        sort=False
    ), 1, 1)

    # Chart 2: Incorrect Answers
    fig.add_trace(go.Pie(
        values=[incorrect_perc, 100 - incorrect_perc],
        hole=.8,
        marker=dict(colors=['#F44336', '#37474F']),
        textinfo='none',
        hoverinfo='none',
        sort=False
    ), 2, 1)

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(t=40, b=0, l=0, r=0),
        annotations=[
            # Annotations for Chart 1 (top)
            dict(text=f'{correct_perc}%', x=0.5, y=0.88, font=dict(size=30, color='#f1f5f9'), showarrow=False),
            dict(text='Correct', x=0.5, y=0.80, font=dict(size=14, color='#94a3b8'), showarrow=False),
            # Annotations for Chart 2 (bottom)
            dict(text=f'{incorrect_perc}%', x=0.5, y=0.18, font=dict(size=30, color='#f1f5f9'), showarrow=False),
            dict(text='Incorrect', x=0.5, y=0.15, font=dict(size=14, color='#94a3b8'), showarrow=False),
            # Main Title
            dict(text='Question Breakdown', x=0.5, y=1, font_size=20, font_color="#f1f5f9", showarrow=False)
        ]
    )
    return fig
