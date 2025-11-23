import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def get_theme_colors(theme: str):
    #theme = theme.lower()
    if theme == "dark":
        return ("#0e1117", "white")      # ciemne tło 
    else:
        return ("white", "black")        # jasne tło 


def plot_col_hist(series, theme: str):
    bg_color, text_color = get_theme_colors(theme)

    fig, ax = plt.subplots(figsize=(4, max(len(series)/2, 1))) # wysokość wykresu w zależności od liczby kategorii
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    sns.barplot(
        y=series.index, 
        x=series.values, 
        orient='h', 
        color='skyblue', 
        ax=ax
    )
    ax.set_ylabel('')
    ax.xaxis.set_visible(False)

    for i, v in enumerate(series.values):
        ax.text(v / 2, i, str(v), color=text_color, va='center', ha='center', fontweight='bold', fontsize=12)

    for s in ax.spines:
        ax.spines[s].set_visible(False)

    st.pyplot(fig)


def plot_line(series1, series2, label1, label2, xlabel, ylabel, title=''):
    plt.figure(figsize=(8, 4))
    plt.plot(series1, label=label1)
    plt.plot(series2, label=label2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()


def pair_multiselect_radio(label_ms, options_ms, options_radio, key_ms, key_radio):
    col1, col2 = st.columns([7, 2])  # dostosuj proporcje kolumn
    with col1:
        selected = st.multiselect(label_ms, options_ms, key=key_ms)
    with col2:
        choice = st.radio('', options_radio, key=key_radio, horizontal=True)
    return selected, choice


def plot_heatmap(corr_matrix):
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=0, vmax=1, linewidths=0.5, linecolor='gray', ax=ax)
    ax.set_title('Macierz istotnych korelacji')
    st.pyplot(fig)