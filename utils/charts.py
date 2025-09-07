import plotly.graph_objects as go

def create_donut_chart(score, total_questions):
    """
    Creates a donut chart visualizing the percentage of correct vs incorrect answers.
    """
    correct_answers = score
    incorrect_answers = total_questions - score

    labels = ['Correct', 'Incorrect']
    values = [correct_answers, incorrect_answers]
    
    # Using a theme-appropriate, vibrant color palette
    colors = ['#14b8a6', '#f43f5e'] # Teal for correct, Rose for incorrect
    
    # Logic to handle cases where there are 0 correct or 0 incorrect answers
    if correct_answers == 0:
        plot_values = [incorrect_answers]
        plot_labels = ['Incorrect']
        segment_colors = [colors[1]]
    elif incorrect_answers == 0:
        plot_values = [correct_answers]
        plot_labels = ['Correct']
        segment_colors = [colors[0]]
    else:
        plot_values = values
        plot_labels = labels
        segment_colors = colors

    fig = go.Figure(data=[go.Pie(
        labels=plot_labels,
        values=plot_values,
        hole=.7,
        marker=dict(
            colors=segment_colors,
        ),
        hoverinfo='label+percent',
        textinfo='percent',
        textfont=dict(size=22, color="#f1f5f9", family="Arial, sans-serif"),
        direction='clockwise',
        sort=False,
    )])

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='#1e293b',
        plot_bgcolor='#1e293b',
        font_color='#f1f5f9',
        margin=dict(t=30, b=30, l=30, r=30),
        height=350,
        annotations=[
            dict(text=f"{correct_answers}/{total_questions}", x=0.5, y=0.5,
                 font=dict(size=36, color="#f1f5f9", family="Arial, sans-serif"),
                 showarrow=False)
        ]
    )

    return fig


def create_bar_chart(feedback):
    """
    Creates a bar chart showing the performance for each question.
    """
    correct_answers = sum(1 for fb in feedback if 'Correct' in fb)
    incorrect_answers = len(feedback) - correct_answers

    labels = ['Incorrect', 'Correct']
    values = [incorrect_answers, correct_answers]
    colors = ['#f43f5e', '#14b8a6']

    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=values,
        text=values,
        textposition='inside',
        textfont=dict(size=18, color="#f1f5f9", family="Arial, sans-serif"),
        marker=dict(
            color=colors,
            cornerradius=8
        ),
        width=[0.5, 0.5] # Set custom bar width
    )])

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=True,
            linecolor='rgba(0,0,0,0)',
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            visible=False 
        ),
        paper_bgcolor='#1e293b',
        plot_bgcolor='#1e293b',
        font_color='#f1f5f9',
        margin=dict(t=20, b=20, l=20, r=20),
        height=300,
        bargap=0.4
    )
    return fig
