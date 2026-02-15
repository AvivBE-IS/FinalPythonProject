from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.data_service import DataService
from services.analysis_service import AnalysisService
import pandas as pd
import json

app = FastAPI()

# 1. Mount static files (CSS, Images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Setup Jinja2 for HTML rendering
templates = Jinja2Templates(directory="templates")

# 3. Initialize Services
data_svc = DataService()
analysis_svc = AnalysisService(data_svc)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """ Renders the homepage """
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "dataset": "Palmer Penguins Dataset"
    })

@app.get("/questions", response_class=HTMLResponse)
@app.get("/questions/{question_id}", response_class=HTMLResponse)
async def questions_page(request: Request, question_id: int = None):
    """ Handles the predefined questions page """
    
    questions_list = {
        1: "Species Distribution",
        2: "Body Mass vs Flipper",
        3: "Island Count",
        4: "Culmen Length Stats",
        5: "Sex Distribution"
    }

    title, result, plot_img = None, None, None
    
    if question_id:
        title, result, plot_img = analysis_svc.run_question(question_id)
    
    return templates.TemplateResponse("questions.html", {
        "request": request,
        "questions_list": questions_list,
        "question_id": question_id,
        "title": title,
        "result": result,
        "plot_url": f"/static/plots/{plot_img}" if plot_img else None
    })

@app.get("/data", response_class=HTMLResponse)
async def get_data(request: Request, 
                   cols: list[str] = Query(None), 
                   filter_col: str = None, 
                   op: str = "==", 
                   value: str = None, 
                   limit: int = 20):
    """ 
    Handles the Data Explorer page.
    Generates metadata for frontend dropdowns and filters the dataframe.
    """
    
    # Load original data and create a copy for filtering
    original_df = data_svc.get_df()
    df = original_df.copy()
    
    error_msg = None

    # --- Prepare Metadata for Frontend (Dropdowns & Logic) ---
    columns_metadata = {}
    
    # Iterate over all columns to check if they are numeric and get unique values
    for col in original_df.columns:
        # Check if column is numeric (int or float)
        is_numeric = pd.api.types.is_numeric_dtype(original_df[col])
        
        # Get unique values: drop NaNs, convert to string, and sort
        unique_vals = sorted(original_df[col].dropna().astype(str).unique().tolist())
        
        columns_metadata[col] = {
            "is_numeric": is_numeric,
            "unique_values": unique_vals
        }

    # --- Filtering Logic ---
    # We use a try-except block to ensure the table renders even if filtering fails
    try:
        # 1. Filter Columns (Select specific columns to display)
        if cols:
            valid_cols = [c for c in cols if c in df.columns]
            if valid_cols:
                df = df[valid_cols]
        
        # 2. Filter Rows (Apply condition)
        if filter_col and value:
            # Check if the chosen column is numeric in the original dataframe
            is_numeric_col = pd.api.types.is_numeric_dtype(original_df[filter_col])
            
            if is_numeric_col:
                # Numeric Comparison
                val_num = float(value)
                if op == "==": df = df[df[filter_col] == val_num]
                elif op == "!=": df = df[df[filter_col] != val_num]
                elif op == ">": df = df[df[filter_col] > val_num]
                elif op == "<": df = df[df[filter_col] < val_num]
                elif op == ">=": df = df[df[filter_col] >= val_num]
                elif op == "<=": df = df[df[filter_col] <= val_num]
            else:
                # String Comparison
                if op == "contains": 
                    # Case-insensitive contains
                    df = df[df[filter_col].astype(str).str.contains(value, case=False, na=False)]
                elif op == "==": 
                    # Exact match (as string)
                    df = df[df[filter_col].astype(str) == value]
    
    except Exception as e:
        error_msg = f"Filter Error: {str(e)}"
        # In case of error, 'df' might be partially filtered or remain as original copy.
        # We continue to render whatever we have.

    # --- Generate HTML Table ---
    # This block is outside the 'try' to ensure table is always generated
    table_html = df.head(limit).to_html(classes="data-table", index=False)

    return templates.TemplateResponse("data.html", {
        "request": request, 
        "table": table_html, 
        "error": error_msg,
        "columns_metadata": columns_metadata,
        "current_filter": filter_col,
        "current_op": op,
        "current_val": value
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)