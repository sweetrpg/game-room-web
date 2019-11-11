FROM node:10 as build
LABEL maintainer="Paul Schifferer <paul@schifferers.net>"

ENV NODE_ENV=development
RUN yarn global add npm

COPY . /build
WORKDIR /build
RUN npm set progress false && npm install --loglevel warn
# RUN node build/build.js
RUN npm run build
RUN ls -l /build


FROM nginx:1

# RUN apt-get update -qq && apt-get install -y -qq \
#   libpangocairo-1.0-0 libx11-xcb1 libxcomposite1 libxcursor1 \
#   libxdamage1 libxi6 libxtst6 libnss3 libcups2 libxss1 libxrandr2 \
#   libgconf2-4 libasound2 libatk1.0-0 libgtk-3-0

# RUN mkdir -p /app
COPY --from=build /build/dist /usr/share/nginx/html
RUN ls -l /usr/share/nginx/html

EXPOSE 80
# WORKDIR /app
# ENTRYPOINT [ "npm", "run", "build" ]
