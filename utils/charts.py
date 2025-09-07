import plotly.graph_objects as go

def create_donut_chart(score, total_questions):
    """
    Creates a donut chart visualizing the percentage of correct vs incorrect answers.
    """
    correct_answers = score
    incorrect_answers = total_questions - score

    labels = ['Correct', 'Incorrect']
    values = [correct_answers, incorrect_answers]
    colors = ['#14b8a6', '#f43f5e']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.6,  # cleaner ring look
        marker=dict(
            colors=colors,
        ),
        hoverinfo='label+percent',
        textinfo='percent',
        textfont=dict(size=18, color="#f1f5f9", family="Segoe UI, sans-serif"),
        pull=[0.03, 0.03]
    )])

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='#1e293b',
        plot_bgcolor='#1e293b',
        font_color='#f1f5f9',
        margin=dict(t=30, b=20, l=20, r=20),
        height=320,
        annotations=[
            dict(text='Score', x=0.5, y=0.55, font_size=16, showarrow=False, font=dict(color="#94a3b8")),
            dict(text=f"{correct_answers}/{total_questions}", x=0.5, y=0.45, font_size=24, showarrow=False, font=dict(family="Segoe UI, sans-serif"))
        ]
    )

    return fig


def create_bar_chart(feedback):
    """
    Creates a bar chart showing the performance for each question.
    """
    scores = [1 if 'Correct' in fb else 0 for fb in feedback]
    question_labels = [f"Q{i+1}" for i in range(len(scores))]
    colors = ['#14b8a6' if s == 1 else '#f43f5e' for s in scores]

    fig = go.Figure(data=[go.Bar(
        x=question_labels,
        y=[1] * len(scores),
        marker=dict(
            color=colors,
            cornerradius=5
        ),
        text=['Correct' if s == 1 else 'Incorrect' for s in scores],
        textposition='inside',
        textfont=dict(size=14, color="#f1f5f9", family="Segoe UI, sans-serif"),
        hoverinfo='text'
    )])

    fig.update_layout(
        xaxis_title="Questions",
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
        bargap=0.3
    )
    return fig
