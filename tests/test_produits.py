def test_lire_produits_vide(client):
    response = client.get("/produits")
    assert response.status_code == 200
    assert response.json() == []
