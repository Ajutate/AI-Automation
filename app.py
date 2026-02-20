"""FastAPI Web Application for BRD to Test Automation"""
import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from docx import Document
import PyPDF2

from ai_automation.workflow import AutomationWorkflow, ValidatedWorkflow
from ai_automation.config import Config


app = FastAPI(title="BRD to Test Automation")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


def read_document(file_path: str) -> str:
    """Read content from different file formats"""
    ext = Path(file_path).suffix.lower()
    
    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    elif ext == '.docx':
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    
    elif ext == '.pdf':
        content = []
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                content.append(page.extract_text())
        return '\n'.join(content)
    
    else:
        raise ValueError(f"Unsupported file format: {ext}")


@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")


@app.post("/generate")
async def generate_tests(
    file: UploadFile = File(...),
    base_name: str = Form(...),
    use_strong_model: bool = Form(False),
    use_parallel: bool = Form(False)
):
    """Generate feature and test files from uploaded BRD"""
    try:
        # Create temp directory for uploads
        os.makedirs("temp", exist_ok=True)
        
        # Save uploaded file
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Read BRD content
        brd_content = read_document(file_path)
        
        # Initialize workflow
        if use_parallel:
            workflow = ValidatedWorkflow(use_strong_model=use_strong_model)
        else:
            workflow = AutomationWorkflow(use_strong_model=use_strong_model)
        
        # Run workflow
        result = workflow.execute(brd_content)
        
        # Save outputs
        from ai_automation.generator import save_outputs
        feature_path, test_path = save_outputs(
            result["feature_file"],
            result["selenium_test"],
            base_name
        )
        
        # Clean up temp file
        os.remove(file_path)
        
        return JSONResponse({
            "status": "success",
            "message": "Files generated successfully",
            "files": {
                "feature": feature_path,
                "test": test_path
            },
            "feature_content": result["feature_file"],
            "test_content": result["selenium_test"]
        })
        
    except Exception as e:
        # Clean up on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{file_type}/{filename}")
async def download_file(file_type: str, filename: str):
    """Download generated files"""
    if file_type == "feature":
        file_path = f"outputs/features/{filename}"
    elif file_type == "test":
        file_path = f"outputs/tests/{filename}"
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, filename=filename)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "BRD to Test Automation"}


if __name__ == "__main__":
    # Create required directories
    os.makedirs("outputs/features", exist_ok=True)
    os.makedirs("outputs/tests", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("temp", exist_ok=True)
    
    print("Starting FastAPI server...")
    print("Open http://localhost:8000 in your browser")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
