import plotly.graph_objects as go

def create_donut_chart(score, total_questions):
    """
    Creates a donut chart visualizing the percentage of correct vs incorrect answers.
    """
    correct_answers = score
    incorrect_answers = total_questions - score

    labels = ['Correct', 'Incorrect']
    values = [correct_answers, incorrect_answers]
    # Softer neutral green + red instead of harsh blue
    colors = ['#22c55e', '#ef4444']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.55,  # cleaner ring look
        marker=dict(colors=colors, line=dict(color='#0f172a', width=2)),  # dark border for slices
        hoverinfo='label+percent',
        textinfo='percent',  # cleaner than raw values
        textfont=dict(size=18, color="#f1f5f9", family="Segoe UI, sans-serif"),
    )])

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,  # slightly more spacing
            xanchor="center",
            x=0.5,
            font=dict(color="#f1f5f9", size=12)
        ),
        paper_bgcolor='#1e293b',
        plot_bgcolor='#1e293b',
        font_color='#f1f5f9',
        margin=dict(t=30, b=20, l=20, r=20),
        height=320
    )

    # Add score annotation in center
    fig.add_annotation(
        text=f"{correct_answers}/{total_questions}",
        x=0.5, y=0.5,
        font=dict(size=20, color="#f1f5f9", family="Segoe UI, sans-serif"),
        showarrow=False
    )

    return fig


def create_bar_chart(feedback):
    """
    Creates a bar chart showing the performance for each question.
    """
    scores = [1 if 'Correct' in fb else 0 for fb in feedback]
    question_labels = [f"Q{i+1}" for i in range(len(scores))]
    colors = ['#3b82f6' if s == 1 else '#ef4444' for s in scores]

    fig = go.Figure(data=[go.Bar(
        x=question_labels,
        y=scores,
        marker_color=colors,
        text=['Correct' if s == 1 else 'Incorrect' for s in scores],
        textposition='auto',
    )])

    fig.update_layout(
        xaxis_title="Questions",
        yaxis=dict(
            showticklabels=False,
            range=[0, 1.2]
        ),
        paper_bgcolor='#1e293b',
        plot_bgcolor='#1e293b',
        font_color='#f1f5f9',
        margin=dict(t=20, b=20, l=20, r=20),
        height=300
    )
    return fig
