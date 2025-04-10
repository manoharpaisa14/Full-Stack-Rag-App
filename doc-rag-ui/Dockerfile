# ✅ Use official Node.js image
FROM node:18

# ✅ Set working directory
WORKDIR /app

# ✅ Copy package files first to leverage Docker cache
COPY package.json package-lock.json ./

# ✅ Install dependencies (cached if no change in package files)
RUN npm install

# ✅ Copy app source code
COPY . .

# ✅ Build the app
RUN npm run build

# ✅ Install serve globally just once
RUN npm install -g serve

# ✅ Serve the build folder on port 3000
CMD ["serve", "-s", "build", "-l", "3000"]
