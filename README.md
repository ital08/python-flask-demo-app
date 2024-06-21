# Flask App Deployment to Azure Kubernetes Service (AKS)

Este proyecto muestra cómo desplegar una aplicación Flask en AKS, utilizando secretos almacenados en Kubernetes. Aquí están las instrucciones para construir la imagen Docker y subirla a Azure Container Registry (ACR).

## Prerrequisitos

- Azure CLI instalado
- Docker instalado
- Una cuenta de Azure
- Python y pip instalados

## Pasos

### 1. Clonar el repositorio

```bash
git clone https://github.com/ital08/python-flask-demo-app.git
cd <NOMBRE_DEL_DIRECTORIO>
```

### 2. Construir la imagen Docker

```bash
docker build -t flask-app .
```

### 3. Crear un Resource Group en Azure

```bash
az login
az group create --name <myResourceGroup> --location eastus
```

### 4. Crear un Azure Container Registry (ACR)

```bash
az acr create --resource-group <myResourceGroup> --name <myContainerRegistry> --sku Basic
```

### 5. Iniciar sesión en ACR

```bash
az acr login --name <myContainerRegistry>
```

### 6. Etiquetar y subir la imagen a ACR

```bash
docker tag flask-app:latest <mycontainerregistry>.azurecr.io/flask-app:latest
docker push <mycontainerregistry>.azurecr.io/flask-app:latest
```

### 7. Crear un clúster de AKS

```bash
az aks create --resource-group <myResourceGroup> --name <myAKSCluster> --node-count 1 --enable-addons monitoring --generate-ssh-keys
```

- resource-group <myResourceGroup>: Especifica el grupo de recursos de Azure donde se creará el clúster.

- name <myAKSCluster>: Define el nombre del clúster de AKS.

- node-count 1: Establece el número de nodos del clúster. En este caso, se crea un clúster con 1 nodo.

- enable-addons monitoring: Habilita el complemento de monitoreo (Azure Monitor) para el clúster, lo que permite recopilar métricas y registros.

- generate-ssh-keys: Genera automáticamente las claves SSH necesarias para acceder a los nodos del clúster.

### 8. Obtener credenciales para el clúster de AKS

```bash
az aks get-credentials --resource-group <myResourceGroup> --name <myAKSCluster></myAKSCluster>
```

### 9. Crear un secreto en Kubernetes

```bash
kubectl create secret generic <mysecret> --from-literal=username=myuser --from-literal=password=mypassword
```

### 10. Desplegar la aplicación en AKS

# Explicación del archivo `deployment.yaml`

El archivo `deployment.yaml` define los recursos necesarios para desplegar la aplicación Flask en Kubernetes. Aquí se incluye tanto un Deployment como un Service.

### Deployment

A. **apiVersion: apps/v1**: Especifica la versión de la API de Kubernetes que se está utilizando para definir el recurso de Deployment.

B. **kind: Deployment**: Define el tipo de recurso que se está creando. En este caso, es un Deployment.

C. **metadata**: Contiene datos que identifican el Deployment, como su nombre.

```bash
 metadata:
 name: flask-app-deployment
```

D. **spec**: Especifica los detalles del Deployment.

- replicas: Define el número de réplicas (pods) que se deben ejecutar para esta aplicación. Aquí está configurado para 2 réplicas.

```bash
 replicas: 2
```

- selector: Define cómo seleccionar los pods que son administrados por este Deployment mediante etiquetas.

```bash
 selector:
  matchLabels:
    app: flask-app
```

- template: Describe el contenido de los pods que se crearán.

```bash
 template:
  metadata:
    labels:
      app: flask-app
  spec:
    containers:
    - name: flask-app
      image: <mycontainerregistry>.azurecr.io/flask-app:latest
      ports:
      - containerPort: 80
      env:
      - name: USERNAME
        valueFrom:
          secretKeyRef:
            name: <mysecret>
            key: username
      - name: PASSWORD
        valueFrom:
          secretKeyRef:
            name: <mysecret>
            key: password
```

- metadata: Contiene las etiquetas para los pods que se crean.

```bash
metadata:
  labels:
    app: flask-app
```

- spec: Contiene los detalles específicos del contenedor dentro del pod.

      -  containers: Define una lista de contenedores que se ejecutarán en los pods. En este caso, solo hay un contenedor.

      -  name: Nombre del contenedor.
      -  image: Especifica la imagen del contenedor que se utilizará.
      -  ports: Expone los puertos del contenedor. Aquí se expone el puerto 80.
      -  env: Define las variables de entorno que se pasan al contenedor. Aquí se obtienen valores de secretos de Kubernetes.

Crea un archivo deployment.yaml con el siguiente contenido:

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
name: flask-app-deployment
spec:
replicas: 2
selector:
matchLabels:
app: flask-app
template:
metadata:
labels:
  app: flask-app
spec:
containers:
- name: flask-app
  image: <mycontainerregistry>.azurecr.io/flask-app:latest
  ports:
  - containerPort: 80
  env:
  - name: USERNAME
    valueFrom:
      secretKeyRef:
        name: <mysecret>
        key: username
  - name: PASSWORD
    valueFrom:
      secretKeyRef:
        name: <mysecret>
        key: password
---
apiVersion: v1
kind: Service
metadata:
name: flask-app-service
spec:
type: LoadBalancer
ports:
- port: 80
selector:
app: flask-app
```

Aplica el deployment:

```bash
kubectl apply -f deployment.yaml
```

### 11. Obtener la dirección IP externa del servicio

```bash
kubectl get services
```
