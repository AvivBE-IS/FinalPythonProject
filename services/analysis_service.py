import matplotlib.pyplot as plt
import seaborn as sns
import os
from services.data_service import DataService

class AnalysisService:
    def __init__(self, data_service: DataService):
        self.data_service = data_service
        # Ensure the directory for plot images exists [cite: 57, 186]
        os.makedirs("static/plots", exist_ok=True)

    def run_question(self, question_id: int):
        # Dispatcher to run one of exactly 5 internal methods [cite: 167, 168]
        questions = {
            1: self._avg_mass_by_species,
            2: self._flipper_vs_bill,
            3: self._island_counts,
            4: self._bill_depth_dist,
            5: self._mass_by_sex
        }
        
        if question_id in questions:
            return questions[question_id]()
        return None, None, None

    # --- 5 Pinned Questions for Penguins Dataset [cite: 55] ---

    def _avg_mass_by_species(self):
        df = self.data_service.get_df()
        # Compute mean body mass per species [cite: 56, 170]
        result = df.groupby('species', observed=True)['body_mass_g'].mean().reset_index()
        
        plt.figure(figsize=(8, 4))
        sns.barplot(data=result, x='species', y='body_mass_g', palette='coolwarm')
        plt.title("Average Body Mass by Species (grams)")
        
        plot_name = "q1.png"
        plt.savefig(f"static/plots/{plot_name}") # [cite: 57, 172]
        plt.close()
        return "Average Body Mass per Species", result.to_html(index=False), plot_name

    def _flipper_vs_bill(self):
        df = self.data_service.get_df()
        # Visualizing correlation between flipper length and bill length
        plt.figure(figsize=(8, 4))
        sns.scatterplot(data=df, x='flipper_length_mm', y='bill_length_mm', hue='species')
        plt.title("Flipper Length vs. Bill Length")
        
        plot_name = "q2.png"
        plt.savefig(f"static/plots/{plot_name}")
        plt.close()
        return "Correlation Analysis", "Scatter plot showing the relationship between flipper and bill size.", plot_name

    def _island_counts(self):
        df = self.data_service.get_df()
        # Count number of penguins observed per island
        result = df['island'].value_counts().reset_index()
        
        plt.figure(figsize=(8, 4))
        sns.countplot(data=df, x='island', palette='Set2')
        plt.title("Penguin Count per Island")
        
        plot_name = "q3.png"
        plt.savefig(f"static/plots/{plot_name}")
        plt.close()
        return "Island Observations", result.to_html(index=False), plot_name

    def _bill_depth_dist(self):
        df = self.data_service.get_df()
        # Distribution of bill depth (cleaned of missing values)
        plt.figure(figsize=(8, 4))
        sns.histplot(df['bill_depth_mm'].dropna(), kde=True, color='orange')
        plt.title("Distribution of Bill Depth (mm)")
        
        plot_name = "q4.png"
        plt.savefig(f"static/plots/{plot_name}")
        plt.close()
        return "Bill Depth Distribution", f"Average Bill Depth: {df['bill_depth_mm'].mean():.2f}mm", plot_name

    def _mass_by_sex(self):
        df = self.data_service.get_df()
        # Comparing body mass between males and females across species
        result = df.groupby(['species', 'sex'], observed=True)['body_mass_g'].mean().reset_index()
        
        plt.figure(figsize=(8, 4))
        sns.boxplot(data=df, x='species', y='body_mass_g', hue='sex')
        plt.title("Body Mass Distribution by Species and Sex")
        
        plot_name = "q5.png"
        plt.savefig(f"static/plots/{plot_name}")
        plt.close()
        return "Mass Comparison by Sex", result.to_html(index=False), plot_name
    
#     Key implementation highlights:
# Handling Missing Values: Where necessary, I used .dropna() to ensure the plotting functions don't crash if the dataset contains null values.

# observed=True: This was added to groupby calls to prevent future warnings when handling categorical columns in Pandas.


# FastAPI Integration: Each function returns three values: the title, the result (either plain text or an HTML table), and the plot's filename.