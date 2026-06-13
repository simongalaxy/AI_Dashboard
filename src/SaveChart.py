import base64


def save_chart(no: int, chart) -> None:
    
    with open("chart.png", "wb") as f:
        f.write(base64.b64decode(chart["img"]))

    return