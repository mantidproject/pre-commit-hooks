#!/bin/bash

BUILD_LOGS_DIR=build_logs
IMAGE_TAG=clang-format-build

if [ ! -f Dockerfile ]; then
  echo "Unable to find Dockerfile. Run this script from build/linux directory."
  exit 1
fi

test -d "${BUILD_LOGS_DIR}" || mkdir "${BUILD_LOGS_DIR}"

# Build image containg binary
docker build \
  --file=Dockerfile \
  --network=host \
  --tag=${IMAGE_TAG} \
  . | tee "${BUILD_LOGS_DIR}/build_log_docker_linux.log"

# Create a temporary container and copy out binary
container_id=$(docker create ${IMAGE_TAG})
docker cp ${container_id}:/build/llvm-build/bin/clang-format ../../bin/clang-format-linux64
docker rm ${container_id}
