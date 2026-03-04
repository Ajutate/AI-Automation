"""Automatic Maven project setup and dependency resolution.

This module handles:
1. Creating Maven project structure
2. Copying generated tests to Maven src directory
3. Auto-resolving dependencies
4. Configuring VS Code Java classpath
"""

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple


def clean_java_file(content: str) -> str:
    """Remove markdown formatting from Java files.
    
    Args:
        content: Java file content that may contain markdown
    
    Returns:
        Clean Java code without markdown
    """
    # Extract from markdown code blocks
    code_block_pattern = r'```+(?:\w+)?\s*\n(.*?)\n```+'
    match = re.search(code_block_pattern, content, re.DOTALL)
    
    if match:
        content = match.group(1).strip()
        
        # Check for nested blocks
        if '```' in content:
            nested_match = re.search(code_block_pattern, content, re.DOTALL)
            if nested_match:
                content = nested_match.group(1).strip()
    else:
        # No code blocks, just remove stray backticks
        content = content.replace('```java', '').replace('```', '').strip()
    
    # Remove explanatory sections
    explanatory_patterns = [
        r'\n\s*#{1,6}\s+.*$',  # Headers like ### Explanation:
        r'\n\s*(?:Note|Explanation|This code|This setup):.*$',
    ]
    
    for pattern in explanatory_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    return content.strip()


class MavenProjectSetup:
    """Handles automatic Maven project setup and dependency resolution."""
    
    def __init__(self, base_dir: str = None, project_name: str = "test-project"):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.project_dir = self.base_dir / project_name
        self.cicd_dir = self.base_dir / "cicd"
        self.outputs_dir = self.base_dir / "outputs"
        
    def setup_project_structure(self) -> bool:
        """Create Maven project structure with pom.xml."""
        try:
            print("📁 Setting up Maven project structure...")
            
            # Create standard Maven directory structure
            src_test_java = self.project_dir / "src" / "test" / "java" / "com" / "automation"
            src_test_resources = self.project_dir / "src" / "test" / "resources" / "features"
            src_main_java = self.project_dir / "src" / "main" / "java" / "com" / "automation"
            
            for directory in [src_test_java, src_test_resources, src_main_java]:
                directory.mkdir(parents=True, exist_ok=True)
            
            # Copy pom.xml
            pom_source = self.cicd_dir / "pom.xml"
            pom_dest = self.project_dir / "pom.xml"
            
            if pom_source.exists():
                shutil.copy2(pom_source, pom_dest)
                print(f"  ✓ Copied pom.xml to {pom_dest}")
            else:
                print(f"  ⚠ pom.xml not found at {pom_source}")
                return False
            
            print("  ✓ Maven project structure created")
            return True
            
        except Exception as e:
            print(f"  ✗ Error setting up project: {e}")
            return False
    
    def clean_project_sources(self) -> bool:
        """Remove all Java source and feature files from the test project."""
        try:
            java_dir = self.project_dir / "src" / "test" / "java" / "com" / "automation"
            features_dir = self.project_dir / "src" / "test" / "resources" / "features"
            for directory in [java_dir, features_dir]:
                if directory.exists():
                    shutil.rmtree(directory)
                directory.mkdir(parents=True, exist_ok=True)
            print("  ✓ Cleaned existing project sources")
            return True
        except Exception as e:
            print(f"  ✗ Error cleaning project sources: {e}")
            return False

    def copy_specific_files(self, feature_path: str, step_def_path: str, runner_path: str = None) -> Tuple[List[str], List[str]]:
        """Copy only the specified newly-generated files into the Maven project.

        Args:
            feature_path: Absolute path to the .feature file.
            step_def_path: Absolute path to the step-definitions .java file.
            runner_path: Optional absolute path to the runner .java file.

        Returns:
            Tuple of (copied_tests, copied_features) filename lists.
        """
        copied_tests: List[str] = []
        copied_features: List[str] = []

        java_dest = self.project_dir / "src" / "test" / "java" / "com" / "automation"
        feat_dest = self.project_dir / "src" / "test" / "resources" / "features"

        print("\n📋 Copying new files to test project...")

        try:
            # Feature file
            if feature_path and Path(feature_path).exists():
                src = Path(feature_path)
                content = clean_java_file(src.read_text(encoding='utf-8'))
                dest = feat_dest / src.name
                dest.write_text(content, encoding='utf-8')
                copied_features.append(src.name)
                print(f"  ✓ {src.name}")

            # Step definitions
            if step_def_path and Path(step_def_path).exists():
                src = Path(step_def_path)
                content = clean_java_file(src.read_text(encoding='utf-8'))
                dest = java_dest / src.name
                dest.write_text(content, encoding='utf-8')
                copied_tests.append(src.name)
                print(f"  ✓ {src.name}")

            # Runner
            if runner_path and Path(runner_path).exists():
                src = Path(runner_path)
                content = clean_java_file(src.read_text(encoding='utf-8'))
                dest = java_dest / src.name
                dest.write_text(content, encoding='utf-8')
                copied_tests.append(src.name)
                print(f"  ✓ {src.name}")

            print(f"  ✓ Copied {len(copied_tests)} test file(s), {len(copied_features)} feature file(s)")
        except Exception as e:
            print(f"  ✗ Error copying specific files: {e}")

        return copied_tests, copied_features

    def copy_generated_files(self) -> Tuple[List[str], List[str]]:
        """Copy generated tests and features to Maven project."""
        copied_tests = []
        copied_features = []
        
        try:
            print("\n📋 Copying generated files...")
            
            # Copy test files
            tests_dir = self.outputs_dir / "tests"
            if tests_dir.exists():
                dest_dir = self.project_dir / "src" / "test" / "java" / "com" / "automation"
                for test_file in tests_dir.glob("*.java"):
                    # Read and clean the file
                    content = test_file.read_text(encoding='utf-8')
                    cleaned_content = clean_java_file(content)
                    
                    # Write cleaned content
                    dest_file = dest_dir / test_file.name
                    dest_file.write_text(cleaned_content, encoding='utf-8')
                    copied_tests.append(test_file.name)
                    print(f"  ✓ {test_file.name}")
            
            # Copy feature files
            features_dir = self.outputs_dir / "features"
            if features_dir.exists():
                dest_dir = self.project_dir / "src" / "test" / "resources" / "features"
                for feature_file in features_dir.glob("*.feature"):
                    # Read and clean the file  
                    content = feature_file.read_text(encoding='utf-8')
                    cleaned_content = clean_java_file(content)  # Works for Gherkin too
                    
                    dest_file = dest_dir / feature_file.name
                    dest_file.write_text(cleaned_content, encoding='utf-8')
                    copied_features.append(feature_file.name)
                    print(f"  ✓ {feature_file.name}")
            
            print(f"  ✓ Copied {len(copied_tests)} test files, {len(copied_features)} feature files")
            return copied_tests, copied_features
            
        except Exception as e:
            print(f"  ✗ Error copying files: {e}")
            return copied_tests, copied_features

    def setup_with_specific_files(self, feature_path: str, step_def_path: str, runner_path: str = None) -> bool:
        """Fresh Maven project setup with only the specified files (clears old sources first)."""
        print("\n" + "="*60)
        print("🚀 FRESH MAVEN PROJECT SETUP (new submission)")
        print("="*60)

        if not self.setup_project_structure():
            print("\n❌ Setup failed at project structure creation")
            return False

        self.clean_project_sources()
        tests, features = self.copy_specific_files(feature_path, step_def_path, runner_path)

        deps_resolved = self.resolve_dependencies()
        if deps_resolved:
            self.compile_tests()

        self.configure_vscode_classpath()

        print("\n" + "="*60)
        print("✅ SETUP COMPLETE")
        print("="*60)
        print(f"\nMaven Project: {self.project_dir}")
        print(f"Tests: {len(tests)} file(s)")
        print(f"Features: {len(features)} file(s)")
        print("\nNext steps:")
        print("  1. Reload VS Code window (Ctrl+Shift+P → 'Reload Window')")
        print("  2. Run: cd test-project && mvn test")
        print("="*60 + "\n")

        return True
    
    def resolve_dependencies(self) -> bool:
        """Run Maven to download and resolve all dependencies."""
        try:
            print("\n📦 Resolving Maven dependencies...")
            
            if not self.project_dir.exists():
                print("  ✗ Project directory not found")
                return False
            
            # Check if Maven is available
            try:
                subprocess.run(["mvn", "--version"], 
                             check=True, 
                             capture_output=True,
                             timeout=10)
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                print("  ⚠ Maven not found. Please install Maven to resolve dependencies.")
                return False
            
            # Run Maven dependency:resolve
            print("  → Running: mvn dependency:resolve")
            result = subprocess.run(
                ["mvn", "dependency:resolve", "-q"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=180  # 3 minutes
            )
            
            if result.returncode == 0:
                print("  ✓ All dependencies resolved successfully")
                return True
            else:
                print(f"  ⚠ Maven exited with code {result.returncode}")
                if result.stderr:
                    print(f"  Error: {result.stderr[:200]}")
                return False
                
        except subprocess.TimeoutExpired:
            print("  ✗ Maven command timed out")
            return False
        except Exception as e:
            print(f"  ✗ Error resolving dependencies: {e}")
            return False
    
    def compile_tests(self) -> bool:
        """Compile the generated tests."""
        try:
            print("\n🔨 Compiling tests...")
            
            result = subprocess.run(
                ["mvn", "clean", "test-compile", "-q"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            if result.returncode == 0:
                print("  ✓ Compilation successful")
                return True
            else:
                print(f"  ✗ Compilation failed with code {result.returncode}")
                if result.stderr:
                    print(f"  Error: {result.stderr[:500]}")
                return False
                
        except subprocess.TimeoutExpired:
            print("  ✗ Compilation timed out")
            return False
        except Exception as e:
            print(f"  ✗ Error compiling: {e}")
            return False
    
    def configure_vscode_classpath(self) -> bool:
        """Configure VS Code Java language server with Maven classpath."""
        try:
            print("\n⚙️  Configuring VS Code Java classpath...")
            
            vscode_dir = self.base_dir / ".vscode"
            vscode_dir.mkdir(exist_ok=True)
            
            # Create/update settings.json
            settings_file = vscode_dir / "settings.json"
            
            proj = self.project_dir.name
            settings = {
                "java.project.referencedLibraries": [
                    f"{proj}/target/**/*.jar",
                    ".m2/repository/**/*.jar"
                ],
                "java.project.sourcePaths": [
                    f"{proj}/src/main/java",
                    f"{proj}/src/test/java"
                ],
                "java.project.outputPath": f"{proj}/target/classes",
                "java.configuration.updateBuildConfiguration": "automatic"
            }
            
            import json
            
            # Merge with existing settings if file exists
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    try:
                        existing = json.load(f)
                        existing.update(settings)
                        settings = existing
                    except json.JSONDecodeError:
                        pass  # Use new settings if existing file is invalid
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
            
            print(f"  ✓ VS Code settings updated: {settings_file}")
            return True
            
        except Exception as e:
            print(f"  ✗ Error configuring VS Code: {e}")
            return False
    
    def run_full_setup(self) -> bool:
        """Run complete automated setup."""
        print("\n" + "="*60)
        print("🚀 AUTOMATED MAVEN PROJECT SETUP")
        print("="*60)
        
        # Step 1: Setup project structure
        if not self.setup_project_structure():
            print("\n❌ Setup failed at project structure creation")
            return False
        
        # Step 2: Copy generated files
        tests, features = self.copy_generated_files()
        if not tests and not features:
            print("\n⚠️  No generated files found to copy")
        
        # Step 3: Resolve dependencies
        deps_resolved = self.resolve_dependencies()
        
        # Step 4: Compile tests (only if dependencies resolved)
        if deps_resolved:
            self.compile_tests()
        
        # Step 5: Configure VS Code
        self.configure_vscode_classpath()
        
        print("\n" + "="*60)
        print("✅ SETUP COMPLETE")
        print("="*60)
        print(f"\nMaven Project: {self.project_dir}")
        print(f"Tests: {len(tests)} files")
        print(f"Features: {len(features)} files")
        print("\nNext steps:")
        print("  1. Reload VS Code window (Ctrl+Shift+P → 'Reload Window')")
        print("  2. Run: cd test-project && mvn test")
        print("="*60 + "\n")
        
        return True


def setup_maven_project():
    """Entry point for automated setup."""
    setup = MavenProjectSetup()
    return setup.run_full_setup()


if __name__ == "__main__":
    setup_maven_project()
