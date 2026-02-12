from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.data_service import DataService
from services.analysis_service import AnalysisService


app = FastAPI()

# Mount the static directory for CSS and generated plots [cite: 184-186]
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 for HTML rendering [cite: 22, 178]
templates = Jinja2Templates(directory="templates")

# Initialize services (Data loaded once on startup) [cite: 18, 162-163]
data_svc = DataService()
analysis_svc = AnalysisService(data_svc)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Main entry point showing the dataset name [cite: 29-31]
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "dataset": "Palmer Penguins Dataset"
    })

@app.get("/questions", response_class=HTMLResponse)
@app.get("/questions/{question_id}", response_class=HTMLResponse)
async def questions_page(request: Request, question_id: int = None):
    # Handles predefined analytical questions [cite: 36-40]
    title, result, plot_img = None, None, None
    if question_id:
        # Run specific analysis through the service [cite: 167]
        title, result, plot_img = analysis_svc.run_question(question_id)
    
    return templates.TemplateResponse("questions.html", {
        "request": request,
        "question_id": question_id,
        "title": title,
        "result": result,
        "plot_url": f"/static/plots/{plot_img}" if plot_img else None
    })

@app.get("/data", response_class=HTMLResponse)
async def get_data(request: Request, 
                   cols: str = None, 
                   filter_col: str = None, 
                   op: str = "==", 
                   value: str = None, 
                   limit: int = 20):
    # Dynamic data querying route [cite: 48-53]
    df = data_svc.get_df()
    error_msg = None
    table_html = None

    try:
        # Handle column selection [cite: 141-146]
        if cols:
            selected_cols = [c.strip() for c in cols.split(",")]
            df = df[selected_cols]
        
        # Handle row filtering logic [cite: 147-157]
        if filter_col and value:
            if op == "==": df = df[df[filter_col].astype(str) == value]
            elif op == "!=": df = df[df[filter_col].astype(str) != value]
            elif op == ">": df = df[df[filter_col] > float(value)]
            elif op == "<": df = df[df[filter_col] < float(value)]
            elif op == "contains": 
                df = df[df[filter_col].astype(str).str.contains(value, case=False, na=False)]
        
        # Convert result to HTML table [cite: 159-160]
        table_html = df.head(limit).to_html(classes="data-table", index=False)
    except Exception as e:
        # Prevent crash and show friendly error [cite: 135-138, 192]
        error_msg = f"Invalid query: {str(e)}"

    return templates.TemplateResponse("data.html", {
        "request": request, 
        "table": table_html, 
        "error": error_msg
    })

# Check if the script is run directly
if __name__ == "__main__":
    import uvicorn
    # Start the Uvicorn server to host the FastAPI app
    # host "127.0.0.1" is your local machine, port 8000 is default
    uvicorn.run(app, host="127.0.0.1", port=8000)