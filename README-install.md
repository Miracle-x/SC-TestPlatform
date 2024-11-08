# Uos网络问题
由于图形界面使用的是 network-manager，所以需要修改重启

1. sudo service network-manager stop
2. sudo rm /var/lib/NetworkManager/NetworkManager.state
3. sudo vim /etc/NetworkManager/NetworkManager.conf
（把false改成true）
4. sudo touch /etc/NetworkManager/conf.d/10-globally-managed-devices.conf (一定是10-globally-managed-devices.conf这个名字，不能乱改，我就吃亏了！！！)

5. sudo service network-manager restart
然后再看图形界面setting里面就有网卡了。如果没有重启一下机器。





# 安装kubectl
更新 apt 包索引，并安装使用 Kubernetes apt 仓库所需要的包
```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg
```
下载 Kubernetes 软件包仓库的公共签名密钥，如果你想用 v1.30 之外的 Kubernetes 版本， 请将下面命令中的 v1.30 替换为所需的次要版本

如果 `/etc/apt/keyrings` 目录不存在，则应在 curl 命令之前创建它，请阅读下面的注释。
```bash
sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg # allow unprivileged APT programs to read this keyring 
```

添加合适的 Kubernetes apt 仓库
这会覆盖 /etc/apt/sources.list.d/kubernetes.list 中的所有现存配置
```bash
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo chmod 644 /etc/apt/sources.list.d/kubernetes.list   # 有助于让诸如 command-not-found 等工具正常工作
```
更新 apt 包索引，然后安装 kubectl
```bash
sudo apt-get update
sudo apt-get install -y kubectl
```


# 安装docker
参考 https://www.jianshu.com/p/a25f630467f7


# 安装kind
For AMD64 / x86_64
```bash
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
```


# 安装 KubeVirt

可以使用 KubeVirt operator 安装 KubeVirt，该 operator 管理所有 KubeVirt 核心组件的生命周期
用于部署 KubeVirt Operator：kubectl
参考 https://maimai.cn/article/detail?fid=1566004910&efid=cSZOlQ4jiUvi7a6EauxXWQ

其中部分命令被下面命令替换
```bash
export VERSION=v1.3.0
kubectl create -f https://github.com/kubevirt/kubevirt/releases/download/${VERSION}/kubevirt-operator.yaml
kubectl apply -f https://github.com/kubevirt/kubevirt/releases/download/${VERSION}/kubevirt-cr.yaml

export VERSION=v1.59.0
kubectl create -f http://github.com/kubevirt/containerized-data-importer/releases/download/$VERSION/cdi-operator.yaml
kubectl create -f http://github.com/kubevirt/containerized-data-importer/releases/download/$VERSION/cdi-cr.yaml

export VERSION=v1.3.0
curl -L -o /usr/local/bin/virtctl https://github.com/kubevirt/kubevirt/releases/download/$VERSION/virtctl-$VERSION-linux-amd64
chmod +x /usr/local/bin/virtctl
```


# 部署前端
基于开源项目kubevirt-manager https://github.com/kubevirt-manager/kubevirt-manager/
下载并修改kubevirt-cr.yaml
```yaml
spec:
  configuration:
    developerConfiguration:
      featureGates:
      - ExpandDisks
```

端口转发到宿主机
```bash
kubectl port-forward pod/kubevirt-manager-6f754586df-r8xg8 8080:8080 -n kubevirt-manager
```
注意要使用ng build部署运行，不然运行的是他们原来的前端镜像


# kind创建集群
```shell
kind create cluster --name 3n --config kube-ovn-3nodes/config.yaml 
kubectl config use-context kind-3n
kubectl -n kube-system get no -o wide
kubectl -n kube-system get po -o wide
```
进入节点
```shell
docker exec -it 3n-worker bash
```


# kube-ovn
## 安装
```shell
wget -O install-1.12.2.sh https://raw.githubusercontent.com/kubeovn/kube-ovn/v1.12.2/dist/images/install.sh
```
```shell
kubectl label node 3n-control-plane 3n-worker 3n-worker2 kube-ovn/role=master
kind load docker-image kubeovn/kube-ovn:v1.12.2 -n 3n
bash NETWORK/install-1.12.2.sh
kubectl -n kube-system get po -o wide
```

## 操作
查看静态路由
```shell
# 进入docker
kubectl exec -it -n kube-system ovn-central-68cfdb5b76-9cljn -- /bin/bash
# 查看
ovn-nbctl lr-route-list ovn-cluster
```

# 网络拓扑可视化
caretta
```shell
helm repo add groundcover https://helm.groundcover.com/
helm repo update
helm install caretta --namespace caretta --create-namespace groundcover/caretta
kubectl port-forward --namespace caretta caretta-grafana-7bdc98d88c-m8nhc 3000:3000
#删除
# helm delete caretta --namespace caretta
# kubectl delete namespace caretta
```
DeepFlow
```shell
helm repo add deepflow https://deepflowio.github.io/deepflow
helm repo update deepflow # use `helm repo update` when helm < 3.7.0
helm install deepflow -n deepflow deepflow/deepflow --version 6.5.012 --create-namespace
kubectl get po -o wide -n deepflow
```
```shell
# 查看地址
NODE_PORT=$(kubectl get --namespace deepflow -o jsonpath="{.spec.ports[0].nodePort}" services deepflow-grafana)
NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")
echo -e "Grafana URL: http://$NODE_IP:$NODE_PORT  \nGrafana auth: admin:deepflow"
```
# k8s dashboard

https://github.com/kubernetes/dashboard/releases/tag/kubernetes-dashboard-7.7.0
```shell
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
kubectl get po -o wide -n kubernetes-dashboard
```
To access Dashboard run:
  kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443

NOTE: In case port-forward command does not work, make sure that kong service name is correct.
      Check the services in Kubernetes Dashboard namespace using:
        kubectl -n kubernetes-dashboard get svc

Dashboard will be available at:
  https://loca
23
lhost:8443

```shell
kubectl create serviceaccount my-admin-sa -n kubernetes-dashboard
kubectl create clusterrolebinding my-admin-binding --clusterrole=cluster-admin --serviceaccount=kubernetes-dashboard:my-admin-sa
kubectl -n kubernetes-dashboard create token my-admin-sa
```


# 部署靶场题目
（以environment/ctf_challenges/web/qiandao1为例）
编写Dockerfile
构建镜像，并载入集群
```shell
docker build -t qiandao1 .
kind load docker-image qiandao1:latest -n 3n
```
编写pod.yaml（或者deployment.yaml）
部署pod
```shell
kubectl apply -f pod.yml
kubectl port-forward pod/qiandao1 8080:80 -n web-test # 转发
```




https://zhuanlan.zhihu.com/p/550841894

# 测试验证模块

基于我们之前的项目Autogen-CTF，进入该目录查看详细使用说明

## Nessus

```shell
docker pull tenable/nessus:latest-oracle
docker run -itd --name my-nessus --restart=always -p 8834:8834 tenable/nessus:latest-oracle
docker ps
```
```shell
docker exec -it ba70ce1fb0a3 /bin/bash
/opt/nessus/sbin/nessuscli fetch --challenge

docker cp /home/bhys/Downloads/nessus.license ba70ce1fb0a3:/
docker exec -it ba70ce1fb0a3 /bin/bash
/opt/nessus/sbin/nessuscli fetch --register-offline nessus.license

docker cp /home/bhys/Downloads/all-2.0.tar.gz ba70ce1fb0a3:/
docker exec -it ba70ce1fb0a3 /bin/bash
/opt/nessus/sbin/nessuscli update ./all-2.0.tar.gz 

/opt/nessus/sbin/nessusd stop
/opt/nessus/sbin/nessusd start
```