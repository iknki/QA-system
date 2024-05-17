# 使用 Node.js 作为基础镜像
FROM node:21.7.1 as build-stage

# 设置工作目录
WORKDIR /app

# 拷贝前端代码到工作目录
COPY . .

# 安装 pnpm 并构建项目
RUN npm install -g pnpm
RUN pnpm install
RUN pnpm run build

# 直接启动前端服务器
CMD ["pnpm", "serve", "-s", "dist", "-l", "5173"]

