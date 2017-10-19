# Apache Spark Helm Chart

Apache Spark is a fast and general-purpose cluster computing system including Apache Zeppelin.

* http://spark.apache.org/
* https://zeppelin.apache.org/

Inspired from Helm Classic chart https://github.com/helm/charts

## Chart Details
This chart will do the following:

* 1 x Spark master with port 8080 exposed on an external LoadBalancer
* 3 x Spark workers with HorizontalPodAutoscaler to scale to max 10 pods when CPU hits 50% of 100m
* 1 x Zeppelin with port 8080 exposed on an external LoadBalancer
* All using Kubernetes Deployments

## Prerequisites

* Assumes that serviceAccount tokens are available under hostname metadata. (Works on GKE by default) URL -- http://metadata/computeMetadata/v1/instance/service-accounts/default/token

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm install --name my-release stable/spark
```

## Configuration

The following tables lists the configurable parameters of the Spark chart and their default values.

### Spark master

| Parameter               | Description                        | Default                                                    |
| ----------------------- | ---------------------------------- | ---------------------------------------------------------- |
| `master.name`           | Spark master name                  | `spark-master`                                             |
| `master.image`          | Container image name               | `gcr.io/google_containers/spark`                           |
| `master.imageTag`       | Container image tag                | `1.5.1_v3`                                                 |
| `master.replicas`       | k8s deployment replicas            | `1`                                                        |
| `master.component`      | k8s selector key                   | `spark-master`                                             |
| `master.cpu`            | container requested cpu            | `100m`                                                     |
| `master.cemory`         | container requested memory         | `512Mi`                                                    |
| `master.servicePort`    | k8s service port                   | `7077`                                                     |
| `master.containerPort`  | Container listening port           | `7077`                                                     |
| `master.daemonMemory`   | master JVM Xms and Xmx option      | `1g`                                                       |

### Spark webUi

|       Parameter       |           Description            |                         Default                          |
|-----------------------|----------------------------------|----------------------------------------------------------|
| `webUi.name`          | Spark webui name                 | `spark-webui`                                            |
| `webUi.servicePort`   | k8s service port                 | `8080`                                                   |
| `webUi.containerPort` | Container listening port         | `8080`                                                   |

### Spark worker

| Parameter                    | Description                        | Default                                                    |
| -----------------------      | ---------------------------------- | ---------------------------------------------------------- |
| `worker.name`                | Spark worker name                  | `spark-worker`                                             |
| `worker.image`               | Container image name               | `gcr.io/google_containers/spark`                           |
| `worker.imageTag`            | Container image tag                | `1.5.1_v3`                                                 |
| `worker.replicas`            | k8s hpa and deployment replicas    | `3`                                                        |
| `worker.replicasMax`         | k8s hpa max replicas               | `10`                                                       |
| `worker.component`           | k8s selector key                   | `spark-worker`                                             |
| `worker.cpu`                 | container requested cpu            | `100m`                                                     |
| `worker.memory`              | container requested memory         | `512Mi`                                                    |
| `worker.containerPort`       | Container listening port           | `7077`                                                     |
| `worker.cpuTargetPercentage` | k8s hpa cpu targetPercentage       | `50`                                                       |
| `worker.daemonMemory`        | worker JVM Xms and Xmx setting     | `1g`                                                       |
| `worker.executorMemory`      | worker memory available for executor | `1g`                                                       |


Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. For example,

```bash
$ helm install --name my-release -f values.yaml stable/spark
```

> **Tip**: You can use the default [values.yaml](values.yaml)


### Notes

Get the Spark URL to visit by running these commands in the same shell:
  
  NOTE: It may take a few minutes for the LoadBalancer IP to be available.
  You can watch the status of by running 'kubectl get svc --namespace {{ .Release.Namespace }} -w {{ template "webui-fullname" . }}'
  
  export SPARK_SERVICE_IP=$(kubectl get svc --namespace {{ .Release.Namespace }} {{ template "webui-fullname" . }} -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  echo http://$SPARK_SERVICE_IP:{{ .Values.webUi.servicePort }}
