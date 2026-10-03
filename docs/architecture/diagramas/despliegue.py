"""Vista de despliegue de BiblioUNSA con Python Diagrams.
Requisitos: pip install diagrams  +  Graphviz instalado en el sistema.
Ejecución:  python despliegue.py   (genera img/despliegue.png)
"""
import os
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.generic.device import Mobile
from diagrams.onprem.network import Nginx, Internet
from diagrams.programming.framework import Django
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Celery
from diagrams.onprem.monitoring import Grafana, Prometheus

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "img"), exist_ok=True)

graph_attr = {"fontsize": "20", "bgcolor": "white", "pad": "0.3"}
with Diagram("BiblioUNSA - Vista de despliegue",
             filename=os.path.join(HERE, "img", "despliegue"),
             show=False, direction="LR", graph_attr=graph_attr, outformat="png"):
    usuarios = Users("Estudiantes y\nbibliotecarios")
    navegador = Mobile("Navegador\n(celular o PC)")

    idp = Internet("Proveedor de identidad\n(correo institucional)")
    academico = Internet("API Sistema Académico\n(servicio externo)")
    correo = Internet("Servicio de correo\n(SMTP externo)")

    with Cluster("Servidor en la nube (VPS)"):
        proxy = Nginx("Nginx\n(HTTPS)")
        with Cluster("Monolito modular"):
            app = Django("Django API\n(6 módulos)")
            worker = Celery("Tareas asíncronas\n(reintentos y correos)")
        cache = Redis("Redis\n(caché + cola)")
        db = PostgreSQL("PostgreSQL\n(esquema por módulo)")
        with Cluster("Monitoreo"):
            prom = Prometheus("Prometheus")
            graf = Grafana("Grafana")

    usuarios >> navegador >> Edge(label="HTTPS") >> proxy >> Edge(label="proxy") >> app
    app >> Edge(label="SQL") >> db
    app >> Edge(label="encola / caché") >> cache >> Edge(label="consume") >> worker
    app >> Edge(label="OIDC (login)", style="dashed") >> idp
    worker >> Edge(label="valida matrícula (API)", style="dashed") >> academico
    worker >> Edge(label="notificación", style="dashed") >> correo
    app >> Edge(label="métricas", style="dotted") >> prom >> graf
