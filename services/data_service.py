import seaborn as sns
import pandas as pd

class DataService:
    def __init__(self):
        # Load the 'penguins' dataset from seaborn on startup [cite: 163]
        # This dataset contains measurements for penguin species in Antarctica
        self._df = sns.load_dataset('penguins')

    def get_df(self) -> pd.DataFrame:
        # Expose the DataFrame for the AnalysisService [cite: 165]
        return self._df