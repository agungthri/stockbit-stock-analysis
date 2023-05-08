import pandas as pd

def get_codes(file_path: str = "./Daftar Saham.xlsx") -> list[str]:
    # Read only the 'Kode' column using the openpyxl engine
    codes = pd.read_excel(file_path, engine='openpyxl', usecols=['Kode'])['Kode'].tolist()

    return codes
