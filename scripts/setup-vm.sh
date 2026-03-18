#!/usr/bin/env bash
# scripts/setup-vm.sh
#
# Provisions an Ubuntu 24.04 VM with:
#   - Python 3.12 + pip + virtualenv
#   - Docker (containerd) — used to build the app image
#   - k3s (lightweight Kubernetes)
#   - Project Python dependencies (diffusers, transformers, torch CPU)
#
# This script is idempotent: running it multiple times is safe.
set -euo pipefail

APP_DIR=/home/vagrant/app
VENV_DIR=/home/vagrant/app/.venv
HF_CACHE=/home/vagrant/hf_cache

echo "=== [1/7] Update apt packages ==="
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get upgrade -y -qq

echo "=== [2/7] Install system packages ==="
apt-get install -y -qq \
    curl wget git \
    python3 python3-pip python3-venv python3-dev \
    build-essential libssl-dev \
    ca-certificates gnupg lsb-release \
    jq unzip

# -------------------------------------------------------------------
# Docker (needed to build the container image)
# -------------------------------------------------------------------
echo "=== [3/7] Install Docker ==="
if ! command -v docker &>/dev/null; then
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
        | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
        > /etc/apt/sources.list.d/docker.list
    apt-get update -qq
    apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin
    systemctl enable --now docker
fi
# Allow vagrant user to use docker without sudo
usermod -aG docker vagrant || true

# -------------------------------------------------------------------
# k3s — lightweight single-node Kubernetes
# -------------------------------------------------------------------
echo "=== [4/7] Install k3s ==="
if ! command -v k3s &>/dev/null; then
    # Install k3s in offline-friendly mode (no traefik to save memory)
    curl -sfL https://get.k3s.io | \
        INSTALL_K3S_EXEC="server --disable traefik --write-kubeconfig-mode 644" \
        sh -
fi
systemctl enable --now k3s

# Copy kubeconfig for vagrant user
mkdir -p /home/vagrant/.kube
cp /etc/rancher/k3s/k3s.yaml /home/vagrant/.kube/config
chown vagrant:vagrant /home/vagrant/.kube/config
chmod 600 /home/vagrant/.kube/config
# Also export for root
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# kubectl alias for vagrant user
if ! grep -q 'alias kubectl' /home/vagrant/.bashrc; then
    echo 'export KUBECONFIG=$HOME/.kube/config' >> /home/vagrant/.bashrc
    echo 'alias kubectl="k3s kubectl"'          >> /home/vagrant/.bashrc
fi

# -------------------------------------------------------------------
# Python virtual environment + project dependencies
# -------------------------------------------------------------------
echo "=== [5/7] Set up Python venv + install dependencies ==="
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

pip install --upgrade pip --quiet

# Install CPU-only PyTorch first (smaller download, works on all VMs)
pip install --quiet \
    torch==2.3.1 torchvision==0.18.1 --index-url https://download.pytorch.org/whl/cpu

# Project deps
pip install --quiet -r "$APP_DIR/backend/requirements.txt"

# Add diffusers, transformers, accelerate for real AI generation
pip install --quiet \
    diffusers==0.29.2 \
    transformers==4.42.4 \
    accelerate==0.31.0 \
    Pillow

deactivate

# Activate venv automatically when vagrant logs in
if ! grep -q 'source.*venv.*activate' /home/vagrant/.bashrc; then
    echo "source $VENV_DIR/bin/activate" >> /home/vagrant/.bashrc
fi

# -------------------------------------------------------------------
# Pre-load HuggingFace models (offline/air-gap support)
# -------------------------------------------------------------------
echo "=== [6/7] Pre-load HuggingFace models for offline use ==="
mkdir -p "$HF_CACHE"
chown vagrant:vagrant "$HF_CACHE"

# Run model download as vagrant user so cache ownership is correct
sudo -u vagrant bash -c "
    source $VENV_DIR/bin/activate
    HF_HOME=$HF_CACHE \
    python3 $APP_DIR/scripts/preload-models.py
"

# -------------------------------------------------------------------
# Build Docker image + deploy to k3s
# -------------------------------------------------------------------
echo "=== [7/7] Build & deploy to k3s ==="
bash "$APP_DIR/scripts/deploy.sh"

echo ""
echo "======================================================"
echo " Setup complete!"
echo " Browse: http://192.168.56.20:30800"
echo " Test:   python3 $APP_DIR/moon_test.py"
echo "======================================================"
