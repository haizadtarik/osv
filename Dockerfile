FROM ubuntu:20.04 

ENV DEBIAN_FRONTEND=noninteractive

# Install OpenJDK 8, wget, unzip, and other essentials
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk wget unzip && \
    rm -rf /var/lib/apt/lists/*

# RUN apt-get update && apt-get install -y xvfb

ENV GRADLE_VERSION=4.10.2
ENV GRADLE_HOME=/opt/gradle/gradle-${GRADLE_VERSION}
ENV PATH=${PATH}:${GRADLE_HOME}/bin

# Download and install Gradle
RUN wget https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip -O /tmp/gradle.zip && \
    unzip /tmp/gradle.zip -d /opt/gradle && \
    rm /tmp/gradle.zip

# Set Gradle user home to a writable location inside /app
ENV GRADLE_USER_HOME=/app/.gradle
RUN mkdir -p /app/.gradle

# (Optional) Set LD_LIBRARY_PATH so that any native libraries Gradle unpacks can be found
ENV LD_LIBRARY_PATH=/app/.gradle/native:$LD_LIBRARY_PATH

WORKDIR /app
# Copy your repository into the container
COPY . /app

# Download the prebuilt Jython standalone jar (version 2.7.2) and place it in /opt/jython.
RUN mkdir -p /opt/jython/bin && \
    wget https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar -O /opt/jython/jython.jar && \
    echo '#!/bin/sh\nexec java -cp /opt/jython/jython.jar "$@"' > /opt/jython/bin/jy && \
    chmod +x /opt/jython/bin/jy

# Add Jython to the PATH.
ENV PATH="/opt/jython/bin:${PATH}"


# Build the project using Gradle.
RUN gradle --no-daemon build --stacktrace -Dorg.gradle.vfs.watch=false -Dorg.gradle.unsafe.watch-fs=false

# Set environment variables expected by the OSV code.
ENV OSV_HOME=/app/
ENV CLASSPATH=/app/libs/*:/app/build/classes:.

WORKDIR /app/src/osv
CMD ["./jy", "demoF3d.py"]

    