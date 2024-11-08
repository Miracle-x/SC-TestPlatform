```shell
cat <<EOF | kind create cluster --name kube-ovn3 --config -
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  kubeProxyMode: ipvs
  disableDefaultCNI: true
  ipFamily: ipv4
  apiServerAddress: 127.0.0.1
  apiServerPort: 0
  podSubnet: "10.16.0.0/16"
  serviceSubnet: "10.96.0.0/12"
nodes:
  - role: control-plane
  - role: worker
  - role: worker
EOF
```