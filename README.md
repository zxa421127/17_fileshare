# PM Knowledge Portal V1

企业知识门户 / 文件管理系统的第一阶段实现。

当前能力：
- FastAPI 后端
- 用户名/密码登录
- JWT 认证
- `/api/auth/me` 当前用户
- PostgreSQL 数据库
- Alembic 数据库迁移
- MinIO 对象存储
- 文件上传、列表、详情、临时下载 URL
- 文件所有者隔离
- pytest 自动化质量门禁

## 本地自动测试

```powershell
cd E:\01-stock\17_fileshare\backend
python -m pip install --upgrade -r requirements.txt
Set-ExecutionPolicy -Scope Process Bypass -Force
.\run_all_tests.ps1
```

测试使用内存 SQLite 和 Fake Storage，不要求启动 PostgreSQL 或 MinIO。

## Docker 开发环境

在项目根目录执行：

```powershell
cd E:\01-stock\17_fileshare
docker compose up -d
```

服务：
- Backend: http://localhost:8000
- Swagger: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- MinIO API: http://localhost:9000
- MinIO Console: http://localhost:9001

Backend 容器启动时会自动执行：

```text
alembic upgrade head
```

## 创建管理员

Docker 服务启动后：

```powershell
docker compose exec backend python create_admin.py --username admin --password "CHANGE_THIS_PASSWORD"
```

生产环境不要使用示例密码，并应替换 JWT、数据库和 MinIO 凭据。

## 当前主要 API

```text
GET  /
GET  /api/auth/status
POST /api/auth/login
GET  /api/auth/me

POST /api/files/upload
GET  /api/files
GET  /api/files/{file_id}
GET  /api/files/{file_id}/download
```

当前文件权限规则：只有文件所有者可以查看和获取下载 URL。共享、角色和文件级权限将在下一阶段加入。
