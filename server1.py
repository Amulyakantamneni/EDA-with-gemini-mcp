import random
from fastmcp import FastMCP
from typing import Any, List
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import base64
from io import BytesIO

mcp = FastMCP(name="Dice Roller")

@mcp.tool
def roll_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` 6-sided dice and return the results."""
    print("here in the loop hello hello hello hello hello hello")
    return [random.randint(1, 6) for _ in range(n_dice)]

# -----------------------
# 📊 Data Visualization Tool
# -----------------------
def _plot_to_base64():
    """Convert current matplotlib figure to base64 string."""
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


@mcp.tool
def generate_visualization(csv_data: str, chart_type: str, x: str, y: str | None = None) -> dict:
    """
    Generate a visualization from a CSV dataset.

    Args:
        csv_data (str): CSV string data.
        chart_type (str): "hist", "scatter", "bar", or "heatmap".
        x (str): Column for x-axis.
        y (str): Column for y-axis (optional).
    Returns:
        dict: { "image_base64": <base64-encoded-png> }
    """
    # Load dataframe
    df = pd.read_csv(io.StringIO(csv_data))

    plt.figure(figsize=(8, 5))
    if chart_type == "hist":
        sns.histplot(df[x], kde=True)
    elif chart_type == "scatter" and y:
        sns.scatterplot(data=df, x=x, y=y)
    elif chart_type == "bar" and y:
        sns.barplot(data=df, x=x, y=y)
    elif chart_type == "heatmap":
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
    else:
        raise ValueError("Unsupported chart type or missing arguments")

    return {"image_base64": _plot_to_base64()}


if __name__ == "__main__":
    mcp.run()