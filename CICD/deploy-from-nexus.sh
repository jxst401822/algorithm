#!/bin/bash

# 从 Nexus 拉取镜像并部署到 OpenShift 的脚本
# 演示 Jenkins CI/CD 流程中的部署阶段

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

# 配置参数
PROJECT_NAME="spring-boot-app"
NEXUS_REGISTRY="nexus.example.com:8082"
OPENSHIFT_PROJECT="spring-boot-demo"
IMAGE_TAG="${1:-latest}"
FULL_IMAGE_NAME="${NEXUS_REGISTRY}/${PROJECT_NAME}:${IMAGE_TAG}"

# 检查参数
if [ -z "$IMAGE_TAG" ]; then
    log_error "请提供镜像标签"
    echo "用法: $0 <image-tag>"
    echo "示例: $0 123-abc123"
    exit 1
fi

# 检查必要的工具
check_prerequisites() {
    log_info "检查部署前置条件..."
    
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
    
    # 检查 Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装或不在 PATH 中"
        exit 1
    fi
    
    log_success "前置条件检查通过"
}

# 验证镜像存在
verify_image_exists() {
    log_info "验证镜像是否存在: ${FULL_IMAGE_NAME}"
    
    # 尝试拉取镜像
    if docker pull ${FULL_IMAGE_NAME} &> /dev/null; then
        log_success "镜像验证成功"
    else
        log_error "镜像不存在或无法访问: ${FULL_IMAGE_NAME}"
        exit 1
    fi
}

# 登录 OpenShift
login_openshift() {
    log_info "登录 OpenShift..."
    
    # 检查是否已登录
    if oc whoami &> /dev/null; then
        log_info "已登录 OpenShift: $(oc whoami)"
    else
        log_error "OpenShift 登录失败"
        exit 1
    fi
}

# 切换到目标项目
switch_project() {
    log_info "切换到项目: ${OPENSHIFT_PROJECT}"
    
    # 检查项目是否存在
    if oc get project ${OPENSHIFT_PROJECT} &> /dev/null; then
        oc project ${OPENSHIFT_PROJECT}
        log_success "已切换到项目: ${OPENSHIFT_PROJECT}"
    else
        log_error "项目不存在: ${OPENSHIFT_PROJECT}"
        exit 1
    fi
}

# 更新部署配置
update_deployment() {
    log_info "更新部署配置..."
    
    # 检查部署是否存在
    if oc get deployment spring-boot-app -n ${OPENSHIFT_PROJECT} &> /dev/null; then
        # 更新镜像
        oc patch deployment spring-boot-app \
            -p "{\"spec\":{\"template\":{\"spec\":{\"containers\":[{\"name\":\"spring-boot-container\",\"image\":\"${FULL_IMAGE_NAME}\"}]}}}}"
        
        log_success "部署配置已更新"
    else
        log_error "部署不存在: spring-boot-app"
        exit 1
    fi
}

# 等待部署完成
wait_for_deployment() {
    log_info "等待部署完成..."
    
    # 等待部署就绪
    if oc rollout status deployment/spring-boot-app -n ${OPENSHIFT_PROJECT} --timeout=300s; then
        log_success "部署完成"
    else
        log_error "部署超时或失败"
        exit 1
    fi
}

# 验证部署
verify_deployment() {
    log_info "验证部署状态..."
    
    # 检查 Pod 状态
    POD_STATUS=$(oc get pods -n ${OPENSHIFT_PROJECT} -l app=spring-boot-app -o jsonpath='{.items[*].status.phase}')
    
    if [[ $POD_STATUS == *"Running"* ]]; then
        log_success "所有 Pod 正在运行"
    else
        log_warning "部分 Pod 可能未正常运行"
    fi
    
    # 检查服务状态
    SERVICE_STATUS=$(oc get service spring-boot-service -n ${OPENSHIFT_PROJECT} -o jsonpath='{.spec.clusterIP}')
    
    if [ ! -z "$SERVICE_STATUS" ]; then
        log_success "服务创建成功"
    else
        log_error "服务创建失败"
    fi
    
    # 检查路由状态
    ROUTE_STATUS=$(oc get route spring-boot-route -n ${OPENSHIFT_PROJECT} -o jsonpath='{.spec.host}')
    
    if [ ! -z "$ROUTE_STATUS" ]; then
        log_success "路由创建成功: https://${ROUTE_STATUS}"
    else
        log_error "路由创建失败"
    fi
}

# 健康检查
health_check() {
    log_info "执行健康检查..."
    
    # 获取应用 URL
    APP_URL=$(oc get route spring-boot-route -n ${OPENSHIFT_PROJECT} -o jsonpath='{.spec.host}')
    
    if [ ! -z "$APP_URL" ]; then
        # 等待应用启动
        sleep 30
        
        # 执行健康检查
        if curl -f https://${APP_URL}/actuator/health &> /dev/null; then
            log_success "健康检查通过"
        else
            log_error "健康检查失败"
            exit 1
        fi
    else
        log_error "无法获取应用 URL"
        exit 1
    fi
}

# 显示部署信息
show_deployment_info() {
    log_info "部署信息汇总:"
    echo "=========================================="
    echo "应用名称: Spring Boot Demo"
    echo "命名空间: ${OPENSHIFT_PROJECT}"
    echo "镜像: ${FULL_IMAGE_NAME}"
    echo "服务地址: $(oc get service spring-boot-service -n ${OPENSHIFT_PROJECT} -o jsonpath='{.spec.clusterIP}')"
    echo "外部访问: https://$(oc get route spring-boot-route -n ${OPENSHIFT_PROJECT} -o jsonpath='{.spec.host}')"
    echo "健康检查: https://$(oc get route spring-boot-route -n ${OPENSHIFT_PROJECT} -o jsonpath='{.spec.host}')/actuator/health"
    echo "监控端点: https://$(oc get route spring-boot-route -n ${OPENSHIFT_PROJECT} -o jsonpath='{.spec.host}')/actuator/prometheus"
    echo "=========================================="
}

# 清理函数
cleanup() {
    log_info "清理临时资源..."
    
    # 删除本地拉取的镜像
    docker rmi ${FULL_IMAGE_NAME} 2>/dev/null || true
    
    log_success "清理完成"
}

# 主函数
main() {
    log_info "开始从 Nexus 部署应用到 OpenShift..."
    log_info "镜像: ${FULL_IMAGE_NAME}"
    
    # 检查前置条件
    check_prerequisites
    
    # 验证镜像存在
    verify_image_exists
    
    # 登录 OpenShift
    login_openshift
    
    # 切换到目标项目
    switch_project
    
    # 更新部署配置
    update_deployment
    
    # 等待部署完成
    wait_for_deployment
    
    # 验证部署
    verify_deployment
    
    # 健康检查
    health_check
    
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