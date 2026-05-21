import matplotlib.pyplot as plt
import seaborn as sns


# Global Visualization Theme
sns.set_theme(
    style="whitegrid",
    palette="deep"
)


def create_line_chart(
    df,
    x_column,
    y_column,
    title,
    x_label,
    y_label,
    figure_size=(12, 6)
):

    plt.figure(figsize=figure_size)

    sns.lineplot(
        data=df,
        x=x_column,
        y=y_column,
        marker="o",
        linewidth=2.5
    )

    plt.title(title, fontsize=16, fontweight="bold")
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


def create_bar_chart(
    df,
    x_column,
    y_column,
    title,
    x_label,
    y_label,
    figure_size=(12, 6),
    horizontal=True,
    sort=True
):

    if sort:
        df = df.sort_values(by=y_column, ascending=False)

    plt.figure(figsize=figure_size)

    if horizontal:

        sns.barplot(
            data=df,
            x=y_column,
            y=x_column
        )

        plt.xlabel(y_label, fontsize=12)
        plt.ylabel(x_label, fontsize=12)

    else:

        sns.barplot(
            data=df,
            x=x_column,
            y=y_column
        )

        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)

        plt.xticks(rotation=45)

    plt.title(title, fontsize=16, fontweight="bold")

    plt.tight_layout()

    plt.show()