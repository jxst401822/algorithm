#!/bin/bash

# OpenShift Spring Boot 应用部署脚本
# 演示如何使用 Dockerfile 和 OpenShift 配置文件部署应用

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查必要的工具
check_prerequisites() {
    log_info "检查部署前置条件..."
    
    # 检查 Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装或不在 PATH 中"
        exit 1
    fi
    
    # 检查 OpenShift CLI
    if ! command -v oc &> /dev/null; then
        log_error "OpenShift CLI (oc) 未安装或不在 PATH 中"
        exit 1
    fi
    
    # 检查是否已登录 OpenShift
    if ! oc whoami &> /dev/null; then
        log_error "未登录 OpenShift，请先运行: oc login"
        exit 1
    fi
    
    log_success "前置条件检查通过"
}

# 构建 Docker 镜像
build_image() {
    log_info "开始构建 Docker 镜像..."
    
    # 设置镜像标签
    IMAGE_NAME="spring-boot-app"
    IMAGE_TAG="latest"
    FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"
    
    # 构建镜像
    docker build -f CICD/dockerfile.yml -t ${FULL_IMAGE_NAME} .
    
    if [ $? -eq 0 ]; then
        log_success "Docker 镜像构建成功: ${FULL_IMAGE_NAME}"
    else
        log_error "Docker 镜像构建失败"
        exit 1
    fi
}

# 推送镜像到 OpenShift 内部镜像仓库
push_image() {
    log_info "推送镜像到 OpenShift 内部镜像仓库..."
    
    # 获取 OpenShift 内部镜像仓库地址
    REGISTRY_URL=$(oc get route default-route -n openshift-image-registry -o jsonpath='{.spec.host}')
    
    if [ -z "$REGISTRY_URL" ]; then
        log_error "无法获取 OpenShift 镜像仓库地址"
        exit 1
    fi
    
    # 获取当前项目名称
    PROJECT_NAME=$(oc project -q)
    
    # 标记镜像
    INTERNAL_IMAGE_NAME="${REGISTRY_URL}/${PROJECT_NAME}/spring-boot-app:latest"
    docker tag spring-boot-app:latest ${INTERNAL_IMAGE_NAME}
    
    # 推送镜像
    docker push ${INTERNAL_IMAGE_NAME}
    
    if [ $? -eq 0 ]; then
        log_success "镜像推送成功: ${INTERNAL_IMAGE_NAME}"
    else
        log_error "镜像推送失败"
        exit 1
    fi
}

# 创建 OpenShift 资源
create_openshift_resources() {
    log_info "创建 OpenShift 资源..."
    
    # 应用配置文件
    oc apply -f CICD/openshift-deployment.yml
    
    if [ $? -eq 0 ]; then
        log_success "OpenShift 资源创建成功"
    else
        log_error "OpenShift 资源创建失败"
        exit 1
    fi
}

# 等待应用部署完成
wait_for_deployment() {
    log_info "等待应用部署完成..."
    
    # 等待 Deployment 就绪
    oc rollout status deployment/spring-boot-app -n spring-boot-demo --timeout=300s
    
    if [ $? -eq 0 ]; then
        log_success "应用部署完成"
    else
        log_error "应用部署超时或失败"
        exit 1
    fi
}

# 验证部署
verify_deployment() {
    log_info "验证部署状态..."
    
    # 检查 Pod 状态
    POD_STATUS=$(oc get pods -n spring-boot-demo -l app=spring-boot-app -o jsonpath='{.items[*].status.phase}')
    
    if [[ $POD_STATUS == *"Running"* ]]; then
        log_success "所有 Pod 正在运行"
    else
        log_warning "部分 Pod 可能未正常运行"
    fi
    
    # 检查服务状态
    SERVICE_STATUS=$(oc get service spring-boot-service -n spring-boot-demo -o jsonpath='{.spec.clusterIP}')
    
    if [ ! -z "$SERVICE_STATUS" ]; then
        log_success "服务创建成功"
    else
        log_error "服务创建失败"
    fi
    
    # 检查路由状态
    ROUTE_STATUS=$(oc get route spring-boot-route -n spring-boot-demo -o jsonpath='{.spec.host}')
    
    if [ ! -z "$ROUTE_STATUS" ]; then
        log_success "路由创建成功: https://${ROUTE_STATUS}"
    else
        log_error "路由创建失败"
    fi
}

# 显示部署信息
show_deployment_info() {
    log_info "部署信息汇总:"
    echo "=========================================="
    echo "应用名称: Spring Boot Demo"
    echo "命名空间: spring-boot-demo"
    echo "服务地址: $(oc get service spring-boot-service -n spring-boot-demo -o jsonpath='{.spec.clusterIP}')"
    echo "外部访问: https://$(oc get route spring-boot-route -n spring-boot-demo -o jsonpath='{.spec.host}')"
    echo "健康检查: https://$(oc get route spring-boot-route -n spring-boot-demo -o jsonpath='{.spec.host}')/actuator/health"
    echo "监控端点: https://$(oc get route spring-boot-route -n spring-boot-demo -o jsonpath='{.spec.host}')/actuator/prometheus"
    echo "=========================================="
}

# 清理函数
cleanup() {
    log_info "清理临时资源..."
    
    # 删除本地构建的镜像
    docker rmi spring-boot-app:latest 2>/dev/null || true
    docker rmi spring-boot-app:latest 2>/dev/null || true
    
    log_success "清理完成"
}

# 主函数
main() {
    log_info "开始 Spring Boot 应用部署到 OpenShift..."
    
    # 检查前置条件
    check_prerequisites
    
    # 构建镜像
    build_image
    
    # 推送镜像
    push_image
    
    # 创建 OpenShift 资源
    create_openshift_resources
    
    # 等待部署完成
    wait_for_deployment
    
    # 验证部署
    verify_deployment
    
    # 显示部署信息
    show_deployment_info
    
    # 清理
    cleanup
    
    log_success "部署完成！"
}

# 错误处理
trap 'log_error "部署过程中发生错误，正在清理..."; cleanup; exit 1' ERR

# 执行主函数
main "$@" 