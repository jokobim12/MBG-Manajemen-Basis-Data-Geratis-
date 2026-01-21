#!/bin/bash
# MBG Remote Installer
# Jalankan dengan: curl -sSL https://raw.githubusercontent.com/jokobim12/MBG-Manajemen-Basis-data-geratis-/main/remote-install.sh | bash

set -e

echo ""
echo "╔════════════════════════════════════════╗"
echo "║     MBG - Remote Installer             ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 tidak ditemukan!"
    echo "   Install dulu: sudo apt install python3"
    exit 1
fi

echo "✅ Python 3 ditemukan"

# Create temp directory
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

echo "📥 Mengunduh MBG..."

# Download files from GitHub
BASE_URL="https://raw.githubusercontent.com/jokobim12/MBG-Manajemen-Basis-data-geratis-/main"

curl -sSL "$BASE_URL/mbg.py" -o mbg.py
curl -sSL "$BASE_URL/translator.py" -o translator.py
curl -sSL "$BASE_URL/db.py" -o db.py
curl -sSL "$BASE_URL/bantuan.py" -o bantuan.py

echo "✅ File berhasil diunduh"

# Install to /opt/mbg
MBG_DIR="/opt/mbg"
echo "📁 Menginstall ke $MBG_DIR..."

sudo mkdir -p "$MBG_DIR"
sudo cp *.py "$MBG_DIR/"
sudo mkdir -p "$MBG_DIR/dapur"
sudo chmod -R 755 "$MBG_DIR"
sudo chmod 777 "$MBG_DIR/dapur"

# Create launcher
LAUNCHER="/usr/local/bin/mbg"
echo "📝 Membuat launcher..."

sudo tee "$LAUNCHER" > /dev/null << 'EOF'
#!/bin/bash
cd /opt/mbg
python3 mbg.py "$@"
EOF

sudo chmod +x "$LAUNCHER"

# Cleanup
cd /
rm -rf "$TMP_DIR"

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  ✅ Instalasi berhasil!                ║"
echo "║                                        ║"
echo "║  Jalankan dengan:  mbg                 ║"
echo "╚════════════════════════════════════════╝"
echo ""
