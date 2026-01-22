#!/bin/bash
set -e

# Usage: ./build.sh [arch] [el_version]
# Examples:
#   ./build.sh              # Build for current arch, el9
#   ./build.sh aarch64      # Build for aarch64, el9
#   ./build.sh x86_64 8     # Build for x86_64, el8
#   ./build.sh aarch64 10   # Build for aarch64, el10

ARCH=${1:-$(uname -m)}
EL_VERSION=${2:-9}

if [ "$ARCH" = "arm64" ]; then
  ARCH="aarch64"
  PLATFORM="linux/arm64"
elif [ "$ARCH" = "x86_64" ]; then
  PLATFORM="linux/amd64"
elif [ "$ARCH" = "aarch64" ]; then
  PLATFORM="linux/arm64"
else
  echo "Unsupported architecture: $ARCH"
  exit 1
fi

# Set container image
if [ "$EL_VERSION" = "10" ]; then
  IMAGE="quay.io/rockylinux/rockylinux:10"
else
  IMAGE="rockylinux:$EL_VERSION"
fi

echo "Building for $ARCH, EL$EL_VERSION ($PLATFORM, $IMAGE)..."

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

mkdir -p dist

docker run --rm --platform "$PLATFORM" \
  -v "$SCRIPT_DIR:/workspace" \
  -w /workspace \
  "$IMAGE" bash -c '
    dnf install -y rpm-build rpmdevtools golang git systemd-rpm-macros
    mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
    cp SPECS/GoBGP.spec ~/rpmbuild/SPECS/
    cp SOURCES/* ~/rpmbuild/SOURCES/
    cd ~/rpmbuild
    spectool -g -R SPECS/GoBGP.spec
    rpmbuild -ba SPECS/GoBGP.spec
    cp RPMS/*/*.rpm /workspace/dist/
  '

echo "Build complete! RPM files are in dist/"
ls -la dist/*.rpm
