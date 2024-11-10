kubectl apply -f vlan1.yaml
kubectl apply -f vlan2.yaml
kubectl create ns underlay
kubectl apply -f subnet1.yaml
kubectl create ns underlay2
kubectl apply -f subnet2.yaml
kubectl apply -f deployment1.yaml

kubectl create ns overlay
kubectl apply -f overlay-subnet1.yaml
kubectl apply -f overlay-deployment1.yaml