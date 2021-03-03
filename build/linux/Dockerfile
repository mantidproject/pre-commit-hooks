FROM ubuntu:bionic

# Install prerequisites
RUN apt-get update && \
    # Install prerequisite tools
    apt-get install -y \
      clang \
      cmake \
      ninja-build \
      wget && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create build area and copy build script
RUN mkdir -p /build
COPY build-clang-format-linux.sh /build

# Run build script
WORKDIR /build
RUN /build/build-clang-format-linux.sh
