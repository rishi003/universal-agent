# Use an official Node.js runtime as a parent image
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy prisma directory
COPY prisma ./prisma

# Command to run migrations
CMD ["npx", "prisma", "migrate", "deploy"]