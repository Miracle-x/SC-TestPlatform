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

可以使用 KubeVirt operator 安装 KubeVirt，该 operator 管理所有 KubeVirt 核心组件的生命周期。

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



# 测试验证模块

基于我们之前的项目Autogen-CTF，进入该目录查看详细使用说明