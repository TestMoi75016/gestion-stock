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
