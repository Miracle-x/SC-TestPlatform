# 创建节点
kind delete cluster -n 3n
kind create cluster --name 3n --config kube-ovn-3nodes/config.yaml
kubectl config use-context kind-3n
kubectl -n kube-system get no -o wide
kubectl -n kube-system get po -o wide

# 安装kube-ovn
kubectl label node 3n-control-plane 3n-worker 3n-worker2 kube-ovn/role=master
kind load docker-image kubeovn/kube-ovn:v1.12.2 -n 3n
bash NETWORK/install-1.12.2.sh
kubectl -n kube-system get po -o wide

## 集成cilium
#kubectl apply -f NETWORK/chaining.yaml
#helm repo add cilium https://helm.cilium.io/
#helm install cilium cilium/cilium --version 1.11.6 \
#    --namespace kube-system \
#    --set cni.chainingMode=generic-veth \
#    --set cni.customConf=true \
#    --set cni.configMap=cni-configuration \
#    --set tunnel=disabled \
#    --set enableIPv4Masquerade=false \
#    --set devices="eth+ ovn0 genev_sys_6081 vxlan_sys_4789" \
#    --set enableIdentityMark=false
#
## 安装流量观测UI
#helm upgrade cilium cilium/cilium --version 1.11.6 \
#   --namespace kube-system \
#   --reuse-values \
#   --set hubble.relay.enabled=true \
#   --set hubble.ui.enabled=true
#curl -L --fail --remote-name-all https://github.com/cilium/hubble/releases/download/v0.10.0/hubble-linux-amd64.tar.gz
#sudo tar xzvfC hubble-linux-amd64.tar.gz /usr/local/bin

# 安装k8s dashboard
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
kubectl get po -o wide -n kubernetes-dashboard

# 部署underlay网络
kubectl apply -f kube-ovn-3nodes/test-underlay/net1.yaml
NETWORK_NAME="net1"
INTERVAL=3

# 循环监视 ProviderNetwork 状态
while true; do
    # 获取当前状态
    STATUS=$(kubectl get provider-network $NETWORK_NAME -o jsonpath='{.status.ready}')
    # 打印当前状态
    echo "Current status of $NETWORK_NAME: $STATUS"
    # 检查状态是否为 true
    if [[ "$STATUS" == "true" ]]; then
        echo "$NETWORK_NAME is ready."
        break
    fi
    # 等待指定的时间间隔
    sleep $INTERVAL
done
