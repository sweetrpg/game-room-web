#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

FROM node:18-alpine AS build

# This Dockerfile adds a non-root 'vscode' user with sudo access. However, for Linux,
# this user's GID/UID must match your local user UID/GID to avoid permission issues
# with bind mounts. Update USER_UID / USER_GID if yours is not 1000. See
# https://aka.ms/vscode-remote/containers/non-root-user for details.
# ARG USERNAME=sweetrpg
# ARG USER_UID=1001
# ARG USER_GID=$USER_UID
ENV NODE_ENV=development

WORKDIR /app
COPY package*.json /app
RUN npm install
COPY . /app
# RUN npm run test:unit

ENV NODE_ENV=production
RUN npm run build


FROM nginx:stable-alpine

ARG BUILD_NUMBER=unset
ARG BUILD_JOB=unset
ARG BUILD_SHA=unset
ARG BUILD_DATE=unset
ARG BUILD_VERSION=unset

COPY --from=build /app/dist /usr/share/nginx/html
# RUN chown -R ${USER_UID}:${USER_GID} /app
RUN echo "{\"number\":\"${BUILD_NUMBER}\",\"job\":\"${BUILD_JOB}\",\"sha\":\"${BUILD_SHA}\",\"date\":\"${BUILD_DATE}\",\"version\":\"${BUILD_VERSION}\"}" > /usr/share/nginx/html/build-info.json

EXPOSE 80

# USER ${USERNAME}

CMD [ "nginx", "-g", "daemon off;"]
