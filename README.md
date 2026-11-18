fp050-miapp
FP.050 · DevOps y Cloud Computing — Producto 2: despliegue continuo con Jenkins (en AWS EC2) y alta disponibilidad con Kubernetes (Minikube).
Cada `git push` a la rama `main` dispara el pipeline de Jenkins, que construye la imagen Docker y la despliega en Kubernetes con 2 réplicas balanceadas por un Service.
Estructura
```
fp050-miapp/
├── app.py               # aplicación Flask: responde con el nombre del pod
├── requirements.txt     # dependencias de Python
├── Dockerfile           # imagen de la aplicación
├── Jenkinsfile          # pipeline: Build → Deploy → Verificar
├── .gitignore           # evita subir claves (.pem) y ficheros temporales
└── k8s/
    ├── deployment.yaml  # 2 réplicas con readinessProbe
    └── service.yaml     # LoadBalancer: reparte el tráfico entre réplicas
```
Probar en local-v1
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py            # http://localhost:8080  y  http://localhost:8080/health
```
Con Docker:
```bash
docker build -t miapp:test .
docker run --rm -p 8080:8080 miapp:test
```
Desplegar a mano en Minikube
```bash
eval $(minikube docker-env)
docker build -t miapp:latest .
kubectl apply -f k8s/
kubectl get pods -l app=miapp          # 2 pods en Running
URL=$(minikube service miapp --url)
for i in {1..6}; do curl -s $URL; done  # las respuestas alternan entre los dos pods
```
Prueba de resiliencia
```bash
kubectl delete pod <nombre-de-un-pod>
kubectl get pods -l app=miapp          # Kubernetes crea otro automáticamente

