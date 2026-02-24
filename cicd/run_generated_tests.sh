#!/bin/bash
# Script to compile and run generated Selenium tests
# Usage: ./run_generated_tests.sh [test-name]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}AI-Generated Test Compilation & Execution${NC}"
echo -e "${GREEN}========================================${NC}"

# Configuration
TEST_NAME=${1:-"GeneratedTest"}
PROJECT_DIR="test-project"
OUTPUT_DIR="outputs"

# Step 1: Check prerequisites
echo -e "\n${YELLOW}[1/6] Checking prerequisites...${NC}"
command -v java >/dev/null 2>&1 || { echo -e "${RED}Java not found!${NC}" >&2; exit 1; }
command -v mvn >/dev/null 2>&1 || { echo -e "${RED}Maven not found!${NC}" >&2; exit 1; }
echo -e "${GREEN}✓ Java and Maven found${NC}"

# Step 2: Create project structure
echo -e "\n${YELLOW}[2/6] Setting up project structure...${NC}"
mkdir -p ${PROJECT_DIR}/src/test/java/com/automation
mkdir -p ${PROJECT_DIR}/src/test/resources
cp cicd/pom.xml ${PROJECT_DIR}/
echo -e "${GREEN}✓ Project structure created${NC}"

# Step 3: Copy generated tests
echo -e "\n${YELLOW}[3/6] Copying generated tests...${NC}"
if [ -f "${OUTPUT_DIR}/tests/${TEST_NAME}Test.java" ]; then
    cp ${OUTPUT_DIR}/tests/${TEST_NAME}Test.java ${PROJECT_DIR}/src/test/java/com/automation/
    echo -e "${GREEN}✓ Test file copied: ${TEST_NAME}Test.java${NC}"
else
    echo -e "${RED}✗ Test file not found: ${OUTPUT_DIR}/tests/${TEST_NAME}Test.java${NC}"
    exit 1
fi

# Step 4: Compile tests
echo -e "\n${YELLOW}[4/6] Compiling tests...${NC}"
cd ${PROJECT_DIR}
if mvn clean compile test-compile; then
    echo -e "${GREEN}✓ Compilation successful!${NC}"
else
    echo -e "${RED}✗ Compilation failed!${NC}"
    exit 1
fi

# Step 5: Run tests
echo -e "\n${YELLOW}[5/6] Running tests...${NC}"
if mvn test -Dtest=${TEST_NAME}Test; then
    echo -e "${GREEN}✓ Tests executed successfully!${NC}"
    TEST_STATUS=0
else
    echo -e "${RED}⚠ Tests completed with failures${NC}"
    TEST_STATUS=1
fi

# Step 6: Generate report
echo -e "\n${YELLOW}[6/6] Generating test report...${NC}"
mvn surefire-report:report
echo -e "${GREEN}✓ Report generated: ${PROJECT_DIR}/target/site/surefire-report.html${NC}"

# Summary
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Execution Summary${NC}"
echo -e "${GREEN}========================================${NC}"
echo "Test Name: ${TEST_NAME}Test"
echo "Source: ${OUTPUT_DIR}/tests/${TEST_NAME}Test.java"
echo "Compiled: ${PROJECT_DIR}/target/test-classes/com/automation/${TEST_NAME}Test.class"
echo "Report: ${PROJECT_DIR}/target/site/surefire-report.html"
echo -e "${GREEN}========================================${NC}"

exit ${TEST_STATUS}
