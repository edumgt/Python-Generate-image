#!/usr/bin/env bash
# scripts/deploy.sh
#
# Builds the Docker image locally, imports it into k3s containerd,
# then applies all Kubernetes manifests.
#
# Run from the repo root inside the VM (or via setup-vm.sh):
#   bash scripts/deploy.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE_NAME="python-generate-image:latest"
K8S_DIR="$REPO_ROOT/k8s"
HF_CACHE="${HF_CACHE:-/home/vagrant/hf_cache}"

echo "=== Building Docker image: $IMAGE_NAME ==="
docker build -t "$IMAGE_NAME" "$REPO_ROOT"

echo "=== Importing image into k3s containerd ==="
# k3s uses its own containerd; images must be imported manually.
docker save "$IMAGE_NAME" | k3s ctr images import -

echo "=== Applying Kubernetes manifests ==="
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

kubectl apply -f "$K8S_DIR/namespace.yaml"
kubectl apply -f "$K8S_DIR/configmap.yaml"
kubectl apply -f "$K8S_DIR/pvc.yaml"
kubectl apply -f "$K8S_DIR/deployment.yaml"
kubectl apply -f "$K8S_DIR/service.yaml"

echo ""
echo "=== Waiting for pod to be ready (up to 3 min) ==="
kubectl rollout status deployment/imggen -n imggen --timeout=180s

echo ""
echo "=== Deployment complete! ==="
echo "   Studio: http://$(hostname -I | awk '{print $1}'):30800"
echo "   Health: curl http://localhost:30800/api/health"
