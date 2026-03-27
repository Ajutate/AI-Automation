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

from ai_automation.workflow import AutomationWorkflow
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
    auto_setup_maven: bool = Form(False)
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
        
        # Initialize workflow with tool validation
        workflow = AutomationWorkflow(
            use_strong_model=use_strong_model,
            auto_setup_maven=False  # Maven handled after save_outputs below
        )
        
        # Run workflow
        result = workflow.execute(brd_content)
        
        # Save outputs
        from ai_automation.generator import save_outputs
        feature_path, step_def_path, runner_path = save_outputs(
            result["feature_file"],
            result.get("step_definitions", result.get("selenium_test", "")),
            base_name,
            result.get("runner_class", None)
        )
        
        # Clean up temp file
        os.remove(file_path)

        # Create a brand-new project folder for this submission (never touch older ones)
        import re as _re
        safe_name = _re.sub(r'[^\w\-]', '-', base_name).strip('-') or 'test'
        project_name = f"test-project-{safe_name}"
        from ai_automation.maven_setup import MavenProjectSetup
        setup = MavenProjectSetup(project_name=project_name)
        setup.setup_project_structure()
        setup.copy_specific_files(feature_path, step_def_path, runner_path if runner_path else None)

        maven_setup_complete = False
        if auto_setup_maven:
            deps_resolved = setup.resolve_dependencies()
            if deps_resolved:
                setup.compile_tests()
            setup.configure_vscode_classpath()
            maven_setup_complete = True

        response_files = {
            "feature": feature_path,
            "step_definitions": step_def_path
        }
        if runner_path:
            response_files["runner"] = runner_path

        response_data = {
            "status": "success",
            "message": "Files generated successfully",
            "files": response_files,
            "project_dir": project_name,
            "feature_content": result["feature_file"],
            "test_content": result.get("step_definitions", result.get("selenium_test", "")),
            "runner_content": result.get("runner_class", "")
        }

        if auto_setup_maven:
            response_data["maven_setup"] = maven_setup_complete
            response_data["message"] += " + Maven project configured" if maven_setup_complete else " (Maven setup failed)"

        return JSONResponse(response_data)
        
    except Exception as e:
        # Clean up on error
        if os.path.exists(file_path):
            os.remove(file_path)
        # Detect LiteLLM / LLM backend connection failures
        error_str = str(e)
        if "Connection error" in error_str or "ConnectionRefused" in error_str or "10061" in error_str or "APIConnectionError" in error_str:
            raise HTTPException(
                status_code=503,
                detail="LiteLLM server is not reachable at http://localhost:4000. "
                       "Please start it with: litellm --model ollama/qwen3 --port 4000"
            )
        raise HTTPException(status_code=500, detail=error_str)


@app.post("/setup-maven")
async def setup_maven_project():
    """Setup Maven project structure and resolve dependencies"""
    try:
        from ai_automation.maven_setup import MavenProjectSetup
        
        setup = MavenProjectSetup()
        success = setup.run_full_setup()
        
        if success:
            return JSONResponse({
                "status": "success",
                "message": "Maven project setup completed successfully",
                "project_dir": str(setup.project_dir),
                "instructions": [
                    "Reload VS Code window (Ctrl+Shift+P → 'Reload Window')",
                    "Run: cd test-project && mvn test"
                ]
            })
        else:
            return JSONResponse({
                "status": "partial",
                "message": "Maven project setup completed with warnings",
                "note": "Check console output for details"
            })
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Maven setup failed: {str(e)}")


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
