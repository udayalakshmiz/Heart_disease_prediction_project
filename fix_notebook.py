import json

path = r"c:\Users\bpskm\OneDrive\Desktop\Heart_disease_prediction\Heart_Disease_Predictor.ipynb"

with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb.get("cells", []):
    if cell.get("cell_type") == "code":
        source = cell.get("source", [])
        if any("from google.colab import drive" in line for line in source):
            cell["source"] = ["# Loading the dataset\n", "# from google.colab import drive\n", "# drive.mount('/content/drive')"]
            cell["outputs"] = []
        if any("pd.read_csv('/content/drive/MyDrive/Datasets/heart.csv')" in line for line in source):
            new_source = []
            for line in source:
                if "pd.read_csv('/content/drive/MyDrive/Datasets/heart.csv')" in line:
                    new_source.append(line.replace("pd.read_csv('/content/drive/MyDrive/Datasets/heart.csv')", "pd.read_csv('Dataset/heart.csv')"))
                else:
                    new_source.append(line)
            cell["source"] = new_source
            cell["outputs"] = []

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)
