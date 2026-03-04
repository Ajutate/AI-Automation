#!/bin/bash
# Maven Installation Helper for Linux/Mac
set -e

echo "========================================"
echo "Maven Installation Helper"
echo "========================================"

# Configuration
MAVEN_VERSION="3.9.6"
INSTALL_DIR="$HOME/maven"
MAVEN_URL="https://dlcdn.apache.org/maven/maven-3/$MAVEN_VERSION/binaries/apache-maven-$MAVEN_VERSION-bin.tar.gz"

# Check if Maven is already installed
if command -v mvn &> /dev/null; then
    echo "✓ Maven is already installed!"
    mvn --version
    exit 0
fi

echo -e "\n[1/4] Downloading Maven $MAVEN_VERSION..."
wget -q --show-progress -O /tmp/maven.tar.gz "$MAVEN_URL"
echo "  ✓ Downloaded to /tmp/maven.tar.gz"

echo -e "\n[2/4] Extracting Maven..."
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
tar -xzf /tmp/maven.tar.gz -C "$INSTALL_DIR" --strip-components=1
echo "  ✓ Extracted to $INSTALL_DIR"

echo -e "\n[3/4] Adding Maven to PATH..."
MAVEN_BIN="$INSTALL_DIR/bin"

# Determine shell config file
if [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
elif [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
else
    SHELL_CONFIG="$HOME/.profile"
fi

# Add to PATH if not already there
if ! grep -q "export PATH=.*maven/bin" "$SHELL_CONFIG" 2>/dev/null; then
    echo "" >> "$SHELL_CONFIG"
    echo "# Maven" >> "$SHELL_CONFIG"
    echo "export PATH=\"$MAVEN_BIN:\$PATH\"" >> "$SHELL_CONFIG"
    echo "  ✓ Added Maven to $SHELL_CONFIG"
else
    echo "  ✓ Maven already in PATH"
fi

echo -e "\n[4/4] Verifying installation..."
export PATH="$MAVEN_BIN:$PATH"
mvn --version

# Clean up
rm -f /tmp/maven.tar.gz

echo -e "\n========================================"
echo "✅ Maven installed successfully!"
echo "========================================"
echo -e "\nIMPORTANT: Run this command to update your PATH:"
echo "  source $SHELL_CONFIG"
echo -e "\nThen verify with: mvn --version"
echo -e "\nMaven Home: $INSTALL_DIR"
echo "========================================"
