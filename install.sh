#!/bin/bash
# MBG Installer Script
# Installs MBG to /usr/local/bin so it can be run from anywhere

set -e

echo "╔════════════════════════════════════════╗"
echo "║     MBG Installer                      ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 tidak ditemukan!"
    echo "   Install dengan: sudo apt install python3"
    exit 1
fi

echo "✅ Python 3 ditemukan"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create MBG directory in /opt
MBG_DIR="/opt/mbg"
echo "📁 Membuat direktori $MBG_DIR..."

if [ -d "$MBG_DIR" ]; then
    echo "   Direktori sudah ada, menghapus versi lama..."
    sudo rm -rf "$MBG_DIR"
fi

sudo mkdir -p "$MBG_DIR"
sudo cp "$SCRIPT_DIR"/*.py "$MBG_DIR/"
sudo mkdir -p "$MBG_DIR/dapur"
sudo chmod -R 755 "$MBG_DIR"
sudo chmod 777 "$MBG_DIR/dapur"

echo "✅ File disalin ke $MBG_DIR"

# Create launcher script
LAUNCHER="/usr/local/bin/mbg"
echo "📝 Membuat launcher di $LAUNCHER..."

sudo tee "$LAUNCHER" > /dev/null << 'EOF'
#!/bin/bash
# MBG Launcher
cd /opt/mbg
python3 mbg.py "$@"
EOF

sudo chmod +x "$LAUNCHER"

echo "✅ Launcher dibuat"
echo ""
echo "╔════════════════════════════════════════╗"
echo "║  ✅ Instalasi berhasil!                ║"
echo "║                                        ║"
echo "║  Jalankan dengan mengetik:   mbg      ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "Database akan disimpan di: $MBG_DIR/dapur/"
