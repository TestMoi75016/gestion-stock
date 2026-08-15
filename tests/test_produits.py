def test_lire_produits_vide(client):
    response = client.get("/produits")
    assert response.status_code == 200
    assert response.json() == []


def test_calcul_stock_produit(client):
    categorie = client.post("/categories", json={"nom": "Boissons"}).json()
    fournisseur = client.post("/fournisseurs", json={"nom": "ACME"}).json()
    produit = client.post(
        "/produits",
        json={
            "nom": "Café",
            "sku": "CAFE-001",
            "categorie_id": categorie["id"],
            "fournisseur_id": fournisseur["id"],
        },
    ).json()

    client.post(
        f"/produits/{produit['id']}/mouvements",
        json={"type": "entree", "quantite": 10},
    )
    client.post(
        f"/produits/{produit['id']}/mouvements",
        json={"type": "sortie", "quantite": 3},
    )

    response = client.get(f"/produits/{produit['id']}/stock")
    assert response.status_code == 200
    assert response.json() == {"produit_id": produit["id"], "stock": 7}


def test_stock_negatif_interdit(client):
    categorie = client.post("/categories", json={"nom": "Boissons"}).json()
    fournisseur = client.post("/fournisseurs", json={"nom": "ACME"}).json()
    produit = client.post(
        "/produits",
        json={
            "nom": "Café",
            "sku": "CAFE-001",
            "categorie_id": categorie["id"],
            "fournisseur_id": fournisseur["id"],
        },
    ).json()

    client.post(
        f"/produits/{produit['id']}/mouvements",
        json={"type": "entree", "quantite": 5},
    )

    response = client.post(
        f"/produits/{produit['id']}/mouvements",
        json={"type": "sortie", "quantite": 10},
    )
    assert response.status_code == 400

    response = client.get(f"/produits/{produit['id']}/stock")
    assert response.status_code == 200
    assert response.json() == {"produit_id": produit["id"], "stock": 5}


def test_alertes_seuil(client):
    categorie = client.post("/categories", json={"nom": "Boissons"}).json()
    fournisseur = client.post("/fournisseurs", json={"nom": "ACME"}).json()

    produit_a = client.post(
        "/produits",
        json={
            "nom": "Produit A",
            "sku": "A-001",
            "seuil_alerte": 5,
            "categorie_id": categorie["id"],
            "fournisseur_id": fournisseur["id"],
        },
    ).json()
    client.post(
        f"/produits/{produit_a['id']}/mouvements",
        json={"type": "entree", "quantite": 3},
    )

    produit_b = client.post(
        "/produits",
        json={
            "nom": "Produit B",
            "sku": "B-001",
            "seuil_alerte": 2,
            "categorie_id": categorie["id"],
            "fournisseur_id": fournisseur["id"],
        },
    ).json()
    client.post(
        f"/produits/{produit_b['id']}/mouvements",
        json={"type": "entree", "quantite": 10},
    )

    response = client.get("/produits/alertes")
    assert response.status_code == 200

    produit_ids = [alerte["produit_id"] for alerte in response.json()]
    assert produit_a["id"] in produit_ids
    assert produit_b["id"] not in produit_ids
