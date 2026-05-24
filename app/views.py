from flask_appbuilder.views import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .models import Cliente, Servicio, Tecnico, OrdenServicio
from . import appbuilder, db
from flask import render_template
from flask_appbuilder import BaseView, expose
from sqlalchemy import func
from datetime import date
from .ia_service import generar_analisis
from sqlalchemy import desc

class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)

    list_columns = [
        "nombre",
        "telefono",
        "correo",
        "direccion"
    ]
class ServicioView(ModelView):
    datamodel = SQLAInterface(Servicio)

    list_columns = [
        "nombre",
        "descripcion",
        "precio"
    ]
class TecnicoView(ModelView):
    datamodel = SQLAInterface(Tecnico)

    list_columns = [
        "nombre",
        "especialidad",
        "telefono"
    ]
class OrdenServicioView(ModelView):
    datamodel = SQLAInterface(OrdenServicio)


    list_columns = [
        "fecha",
        "estado",
        "costo",
        "cliente",
        "servicio",
        "tecnico"
    ]

    add_columns = [
    "cliente",
    "servicio",
    "tecnico",
    "fecha",
    "estado",
    "costo"
]

    edit_columns = [
    "cliente",
    "servicio",
    "tecnico",
    "fecha",
    "estado",
    "costo"
]

    def pre_add(self, item):

        if item.servicio:
            item.costo = item.servicio.precio

        if item.fecha and item.fecha >= date.today():
            item.estado = "Activo"
        else:
            item.estado = "Inactivo"

    def pre_update(self, item):

        if item.servicio:
            item.costo = item.servicio.precio

        if item.fecha and item.fecha >= date.today():
            item.estado = "Activo"
        else:
            item.estado = "Inactivo"

appbuilder.add_view(
    ClienteView,
    "Clientes",
    icon="fa-user",
    category="Gestión"
)

appbuilder.add_view(
    ServicioView,
    "Servicios",
    icon="fa-tools",
    category="Gestión"
)

appbuilder.add_view(
    TecnicoView,
    "Técnicos",
    icon="fa-wrench",
    category="Gestión"
)
    
appbuilder.add_view(
   OrdenServicioView,
    "Órdenes",
    icon="fa-clipboard",
    category="Gestión"
)

class DashboardView(BaseView):

    default_view = "index"
    route_base = "/dashboard"

    @expose("/")
    def index(self):

        total_clientes = db.session.query(
            func.count(Cliente.id)
        ).scalar()

        total_ordenes = db.session.query(
            func.count(OrdenServicio.id)
        ).scalar()

        ingresos = db.session.query(
            func.sum(OrdenServicio.costo)
        ).scalar()

        servicios = db.session.query(
            Servicio.nombre,
            func.count(OrdenServicio.id)
        ).join(
            OrdenServicio
        ).group_by(
            Servicio.nombre
        ).all()

        labels = [s[0] for s in servicios]
        valores = [s[1] for s in servicios]

        datos_ia = f"""
        Total de clientes: {total_clientes}
        Total de órdenes: {total_ordenes}
        Ingresos totales: {ingresos}

        Servicios:
        {servicios}
        """

        analisis_ia = generar_analisis(datos_ia)

        return self.render_template(
            "dashboard/dashboard.html",
            total_clientes=total_clientes,
            total_ordenes=total_ordenes,
            ingresos=ingresos,
            labels=labels,
            valores=valores,
            analisis_ia=analisis_ia
        )

class TendenciasView(BaseView):

    default_view = "index"

    route_base = "/tendencias"

    @expose("/")

    def index(self):

        clientes = db.session.query(
            Cliente.nombre,
            func.count(OrdenServicio.id)
        ).join(
            OrdenServicio
        ).group_by(
            Cliente.nombre
        ).order_by(
            desc(func.count(OrdenServicio.id))
        ).all()

        servicios = db.session.query(
            Servicio.nombre,
            func.count(OrdenServicio.id)
        ).join(
            OrdenServicio
        ).group_by(
            Servicio.nombre
        ).all()

        clientes_labels = [c[0] for c in clientes]
        clientes_valores = [c[1] for c in clientes]

        servicios_labels = [s[0] for s in servicios]
        servicios_valores = [s[1] for s in servicios]

        datos_ia = f"""
        Clientes frecuentes: {clientes}
        Servicios más utilizados: {servicios}
        """

        analisis_ia = generar_analisis(datos_ia)

        return self.render_template(
            "reportes/tendencias.html",
            clientes_labels=clientes_labels,
            clientes_valores=clientes_valores,
            servicios_labels=servicios_labels,
            servicios_valores=servicios_valores,
            analisis_ia=analisis_ia
        )

class RecomendacionesView(BaseView):

    default_view = "index"

    route_base = "/recomendaciones"

    @expose("/")

    def index(self):

        total_ordenes = db.session.query(
            func.count(OrdenServicio.id)
        ).scalar()

        ingresos = db.session.query(
            func.sum(OrdenServicio.costo)
        ).scalar()

        servicio_top = db.session.query(
            Servicio.nombre,
            func.count(OrdenServicio.id)
        ).join(
            OrdenServicio
        ).group_by(
            Servicio.nombre
        ).order_by(
            desc(func.count(OrdenServicio.id))
        ).first()

        tecnico_top = db.session.query(
            Tecnico.nombre,
            func.count(OrdenServicio.id)
        ).join(
            OrdenServicio
        ).group_by(
            Tecnico.nombre
        ).order_by(
            desc(func.count(OrdenServicio.id))
        ).first()

        datos_ia = f"""
        Total de órdenes: {total_ordenes}
        Ingresos totales: {ingresos}
        Servicio más solicitado: {servicio_top}
        Técnico con más carga: {tecnico_top}

        Genera recomendaciones para mejorar el negocio,
        optimizar servicios y aumentar ingresos.
        """

        analisis_ia = generar_analisis(datos_ia)

        return self.render_template(
            "reportes/recomendaciones.html",
            total_ordenes=total_ordenes,
            ingresos=ingresos,
            servicio_top=servicio_top,
            tecnico_top=tecnico_top,
            analisis_ia=analisis_ia
        )
appbuilder.add_view(
    DashboardView,
    "Dashboard",
    icon="fa-chart-bar",
    category="Reportes"
)

appbuilder.add_view(
    TendenciasView,
    "Tendencias",
    icon="fa-chart-line",
    category="Reportes"
)
appbuilder.add_view(
    RecomendacionesView,
    "Recomendaciones IA",
    icon="fa-robot",
    category="Reportes"
)