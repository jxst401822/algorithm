# Jenkins CI/CD + OpenShift Spring Boot 应用部署演示

这个项目演示了完整的 CI/CD 流程：Jenkins 从远程仓库 master 分支构建、运行测试、SonarQube 和 JaCoCo 检测、打 tag 上传到 Nexus、OpenShift 拉取镜像部署。

## 文件结构

```
CICD/
├── dockerfile.yml              # Dockerfile 伪代码 (支持测试和代码质量检测)
├── openshift-deployment.yml    # OpenShift 部署配置 (从 Nexus 拉取镜像)
├── Jenkinsfile                 # Jenkins Pipeline 脚本
├── deploy-to-openshift.sh     # 部署脚本 (备用)
└── README.md                  # 说明文档
```

## CI/CD 流程概览

```
Git Master Branch
       ↓
   Jenkins Pipeline
       ↓
   代码检出 (Checkout)
       ↓
   构建和测试 (Build & Test)
       ↓
   SonarQube 代码质量分析
       ↓
   质量门禁检查 (Quality Gate)
       ↓
   构建 Docker 镜像
       ↓
   推送镜像到 Nexus
       ↓
   部署到 OpenShift
       ↓
   集成测试验证
```

## 主要特性

### Jenkins Pipeline 特性
- **多阶段构建**: 完整的 CI/CD 流水线
- **代码质量检测**: SonarQube 集成
- **测试覆盖率**: JaCoCo 覆盖率报告
- **质量门禁**: 自动质量检查
- **镜像管理**: Nexus 镜像仓库集成
- **自动部署**: OpenShift 自动部署

### Dockerfile 特性
- **多阶段构建**: 优化镜像大小，分离构建和运行环境
- **测试集成**: 包含单元测试、集成测试、JaCoCo 覆盖率
- **代码质量**: SonarQube 分析集成
- **安全配置**: 使用非 root 用户运行应用
- **健康检查**: 集成 Spring Boot Actuator 健康检查
- **资源优化**: JVM 参数优化，适合容器环境

### OpenShift 部署特性
- **镜像拉取**: 从 Nexus 私有仓库拉取镜像
- **认证配置**: Nexus 仓库认证 Secret
- **命名空间隔离**: 独立的命名空间管理
- **服务账户**: 安全权限管理
- **配置管理**: ConfigMap 和 Secret 管理
- **自动扩缩容**: HPA 配置
- **网络策略**: 网络安全控制
- **监控集成**: Prometheus 监控配置
- **路由配置**: 外部访问配置

## 部署步骤

### 1. 前置条件

确保已安装和配置以下工具：
- Jenkins (带必要插件)
- Docker
- OpenShift CLI (oc)
- Nexus 镜像仓库
- SonarQube 服务器

### 2. Jenkins 配置

#### 安装必要插件
```bash
# Jenkins 插件列表
- Pipeline
- Git
- Docker Pipeline
- SonarQube Scanner
- JaCoCo Plugin
- Test Results Aggregator
- Credentials Binding
- Email Extension
```

#### 配置凭据
```bash
# 在 Jenkins 中配置以下凭据
- git-credentials: Git 仓库认证
- nexus-credentials: Nexus 镜像仓库认证
- sonar-credentials: SonarQube 认证
- openshift-credentials: OpenShift 认证
```

### 3. 配置 Jenkins Pipeline

#### 创建 Jenkins Job
1. 创建新的 Pipeline Job
2. 配置 Git 仓库地址
3. 设置 Jenkinsfile 路径
4. 配置构建触发器

#### 环境变量配置
```bash
# 在 Jenkins 系统配置中设置
NEXUS_REGISTRY=nexus.example.com:8082
SONAR_HOST_URL=http://sonarqube.example.com:9000
OPENSHIFT_SERVER=https://openshift.example.com:6443
```

### 4. 运行 CI/CD 流程

#### 方法一：通过 Jenkins Web UI
1. 登录 Jenkins
2. 选择对应的 Pipeline Job
3. 点击 "Build Now"
4. 监控构建进度

#### 方法二：通过 Git Webhook
```bash
# 配置 Git 仓库 Webhook
URL: http://jenkins.example.com/github-webhook/
Events: push, pull_request
```

### 5. 验证部署

```bash
# 检查 OpenShift 部署状态
oc get pods -n spring-boot-demo
oc get deployment spring-boot-app -n spring-boot-demo
oc get route spring-boot-route -n spring-boot-demo

# 测试应用访问
curl https://$(oc get route spring-boot-route -n spring-boot-demo -o jsonpath='{.spec.host}')/actuator/health
```

## 配置说明

### Jenkins Pipeline 配置要点

1. **多阶段构建**
   - Checkout: 代码检出
   - Build & Test: 构建和测试
   - SonarQube Analysis: 代码质量分析
   - Quality Gate: 质量门禁检查
   - Build Docker Image: 构建 Docker 镜像
   - Push to Nexus: 推送镜像到 Nexus
   - Deploy to OpenShift: 部署到 OpenShift
   - Integration Test: 集成测试

2. **质量保证**
   - 单元测试覆盖率要求
   - SonarQube 质量门禁
   - 代码规范检查
   - 安全漏洞扫描

3. **镜像管理**
   - 版本化镜像标签
   - Nexus 私有仓库
   - 镜像安全扫描
   - 镜像生命周期管理

### Dockerfile 配置要点

1. **多阶段构建**
   - 第一阶段：使用 JDK 构建应用
   - 第二阶段：使用 JRE 运行应用

2. **测试集成**
   - 单元测试执行
   - JaCoCo 覆盖率生成
   - SonarQube 分析集成

3. **安全配置**
   - 使用非 root 用户 (UID 1001)
   - 设置适当的文件权限

4. **性能优化**
   - JVM 参数优化
   - 使用 G1GC 垃圾收集器
   - 内存限制配置

### OpenShift 配置要点

1. **镜像拉取**
   - Nexus 仓库认证
   - 私有镜像拉取
   - 镜像拉取策略

2. **资源管理**
   - CPU 和内存限制
   - 自动扩缩容配置

3. **安全配置**
   - 服务账户配置
   - 网络策略
   - Secret 管理

4. **监控和日志**
   - Prometheus 监控
   - 日志聚合
   - 健康检查端点

## 常用命令

### Jenkins 相关
```bash
# 查看构建日志
curl -u user:token http://jenkins.example.com/job/spring-boot-app/lastBuild/consoleText

# 触发构建
curl -X POST http://jenkins.example.com/job/spring-boot-app/build

# 查看构建状态
curl -u user:token http://jenkins.example.com/job/spring-boot-app/lastBuild/api/json
```

### OpenShift 相关
```bash
# 查看部署状态
oc get pods -n spring-boot-demo
oc rollout status deployment/spring-boot-app -n spring-boot-demo

# 查看日志
oc logs -f deployment/spring-boot-app -n spring-boot-demo

# 手动扩缩容
oc scale deployment spring-boot-app --replicas=5 -n spring-boot-demo
```

### Nexus 相关
```bash
# 查看镜像列表
curl -u admin:password http://nexus.example.com:8081/service/rest/v1/search?repository=docker-hosted

# 删除旧镜像
curl -X DELETE -u admin:password http://nexus.example.com:8081/service/rest/v1/components/component-id
```

## 故障排除

### 常见问题

1. **Jenkins 构建失败**
   - 检查 Git 仓库访问权限
   - 验证 Maven 依赖下载
   - 确认测试用例通过

2. **SonarQube 分析失败**
   - 检查 SonarQube 服务器连接
   - 验证认证凭据
   - 确认项目配置正确

3. **镜像推送失败**
   - 检查 Nexus 仓库连接
   - 验证 Docker 登录状态
   - 确认镜像标签格式

4. **OpenShift 部署失败**
   - 检查镜像拉取权限
   - 验证资源限制配置
   - 确认服务账户权限

### 调试命令

```bash
# Jenkins 调试
ssh jenkins@jenkins-server
docker exec -it jenkins-container bash

# OpenShift 调试
oc describe pod <pod-name> -n spring-boot-demo
oc exec -it <pod-name> -n spring-boot-demo -- /bin/bash
oc get events -n spring-boot-demo --sort-by='.lastTimestamp'

# Nexus 调试
docker exec -it nexus-container bash
tail -f /opt/sonatype/nexus/log/nexus.log
```

## 最佳实践

1. **CI/CD 流程**
   - 自动化所有构建和测试步骤
   - 实施质量门禁
   - 版本化所有制品
   - 回滚机制

2. **镜像管理**
   - 使用语义化版本标签
   - 定期清理旧镜像
   - 镜像安全扫描
   - 镜像签名验证

3. **安全配置**
   - 最小权限原则
   - 定期更新基础镜像
   - 网络安全策略
   - 密钥管理

4. **监控和日志**
   - 集成健康检查
   - 配置结构化日志
   - 设置监控告警
   - 性能指标收集

## 扩展功能

### 多环境部署
```yaml
# 在 Jenkinsfile 中添加环境判断
stage('Deploy to Environment') {
    steps {
        script {
            if (env.BRANCH_NAME == 'master') {
                // 部署到生产环境
                sh "oc project production"
            } else if (env.BRANCH_NAME == 'develop') {
                // 部署到开发环境
                sh "oc project development"
            }
        }
    }
}
```

### 蓝绿部署
```yaml
# OpenShift 蓝绿部署配置
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: spring-boot-route-blue
spec:
  to:
    name: spring-boot-service-blue
---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: spring-boot-route-green
spec:
  to:
    name: spring-boot-service-green
```

### 金丝雀发布
```yaml
# 金丝雀发布配置
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: spring-boot-route-canary
spec:
  to:
    name: spring-boot-service
    weight: 90
  alternateBackends:
  - name: spring-boot-service-new
    weight: 10
```

这个演示项目提供了一个完整的 Jenkins CI/CD + OpenShift 部署解决方案，包含了生产环境所需的各种配置和最佳实践。 