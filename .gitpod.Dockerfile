FROM gitpod/workspace-full:commit-8c0f68d1f8410fdf6ff00fd76f54ab61125a12ea

# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/

RUN npm install -g aws-cdk@1.51.0 && \
    pip install awscli && \
    brew install kubectl