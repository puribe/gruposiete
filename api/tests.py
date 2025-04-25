import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from django.contrib.auth.models import Group
from app.models import (
    OrganismoSectorial, Plan, TipoMedida,
    Medida, Verificacion, MedidaReportada, OrganismoPlan
)

User = get_user_model()

# ------------------------ FIXTURES ------------------------

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser("admin", "admin@example.com", "adminpass")

@pytest.fixture
def user_sectorial(db):
    org = OrganismoSectorial.objects.create(nombre="CONAF")
    user = User.objects.create_user("fiscalizador", password="1234", organismo_sectorial=org)
    group, _ = Group.objects.get_or_create(name='organizacion_sectorial')
    user.groups.add(group)
    return user

@pytest.fixture
def admin_client(client, admin_user):
    client.force_authenticate(user=admin_user)
    return client

@pytest.fixture
def sectorial_client(client, user_sectorial):
    client.force_authenticate(user=user_sectorial)
    return client

# ------------------------ ORGANISMOS ------------------------

@pytest.mark.django_db
def test_organismo_list(admin_client):
    OrganismoSectorial.objects.create(nombre="SAG")
    res = admin_client.get("/api/organismos/")
    assert res.status_code == 200
    assert len(res.data) >= 1

@pytest.mark.django_db
def test_organismo_create(admin_client):
    res = admin_client.post("/api/organismos/", {"nombre": "MMA"})
    assert res.status_code == 201
    assert res.data["nombre"] == "MMA"

@pytest.mark.django_db
def test_organismo_create_no_auth(client):
    res = client.post("/api/organismos/", {"nombre": "MMA"})
    assert res.status_code == 403

@pytest.mark.django_db
def test_organismo_sin_medidas_action(admin_client):
    res = admin_client.get("/api/organismos/sin_medidas_informadas/")
    assert res.status_code == 404

# ------------------------ PLANES ------------------------

@pytest.mark.django_db
def test_plan_crud(admin_client):
    data = {
        "nombre": "Plan Clima",
        "inicio": "2025-01-01T00:00:00Z",
        "termino": "2025-12-31T00:00:00Z",
        "estado_avance": "Inicial"
    }
    res = admin_client.post("/api/planes/", data, format="json")
    assert res.status_code == 201
    plan_id = res.data["id"]

    res = admin_client.get(f"/api/planes/{plan_id}/")
    assert res.status_code == 200
    assert res.data["nombre"] == "Plan Clima"

    res = admin_client.put(f"/api/planes/{plan_id}/", {**data, "nombre": "Plan Modificado"}, format="json")
    assert res.status_code == 200
    assert res.data["nombre"] == "Plan Modificado"

    res = admin_client.delete(f"/api/planes/{plan_id}/")
    assert res.status_code == 204

# ------------------------ TIPO MEDIDA ------------------------

@pytest.mark.django_db
def test_tipo_medida_create_and_list(admin_client):
    res = admin_client.post("/api/tipo_medidas/", {"nombre": "Toneladas"})
    assert res.status_code == 201
    res = admin_client.get("/api/tipo_medidas/")
    assert res.status_code == 200
    assert len(res.data) >= 1

# ------------------------ VERIFICACIONES ------------------------

@pytest.mark.django_db
def test_verificacion_crud(admin_client):
    res = admin_client.post("/api/verificaciones/", {
        "nombre": "Informe",
        "verificacion": "Verificado por firma"
    })
    assert res.status_code == 201
    ver_id = res.data["id"]

    res = admin_client.get(f"/api/verificaciones/{ver_id}/")
    assert res.status_code == 200
    assert res.data["nombre"] == "Informe"

# ------------------------ MEDIDAS ------------------------

@pytest.mark.django_db
def test_create_medida(admin_client):
    plan = Plan.objects.create(nombre="Plan X", inicio="2025-01-01", termino="2025-12-31")
    tipo = TipoMedida.objects.create(nombre="Volumen")
    org = OrganismoSectorial.objects.create(nombre="SAG")
    OrganismoPlan.objects.create(plan=plan, organismo_sectorial=org)
    data = {
        "referencia_pda": "M-001",
        "nombre_corto": "Medida X",
        "indicador": "N° árboles",
        "formula_de_calculo": "sum(x)",
        "frecuencia_reporte": "ANUAL",
        "tipo_de_dato_a_validar": "Decimal",
        "tipo_medida": tipo.id,
        "plan": plan.id,
        "organismo_sectorial": org.id
    }

    res = admin_client.post("/api/medidas/", data, format="json")
    assert res.status_code == 201
    assert res.data["nombre_corto"] == "Medida X"

# ------------------------ MEDIDA REPORTADA ------------------------

@pytest.mark.django_db
def test_reportar_medida(sectorial_client):
    org = OrganismoSectorial.objects.get(nombre="CONAF")
    tipo = TipoMedida.objects.create(nombre="Volumen")
    plan = Plan.objects.create(nombre="Plan Y", inicio="2025-01-01", termino="2025-12-31")
    medida = Medida.objects.create(
        referencia_pda="REP-001",
        nombre_corto="Control X",
        indicador="Volumen total",
        formula_de_calculo="sum(x)",
        frecuencia_reporte="ANUAL",
        tipo_de_dato_a_validar="Decimal",
        tipo_medida=tipo,
        plan=plan,
        organismo_sectorial=org
    )

    data = {
        "organismo_sectorial": org.id,
        "medida": medida.id,
        "valor": "123.45",
        "estado": "VERIFICACION_PENDIENTE"
    }

    res = sectorial_client.post("/api/medida_reportada/", data, format="json")
    assert res.status_code == 201
    assert res.data["valor"] == "123.45"
