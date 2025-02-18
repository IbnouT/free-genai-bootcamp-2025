from app.models import Language

def test_seed_database(client, db_session):
    """Test the admin seed endpoint."""
    # Call the seed endpoint
    response = client.post("/admin/seed")
    assert response.status_code == 200
    assert response.json() == {"message": "Database seeded successfully"}
    
    # Verify that the database was seeded
    languages = db_session.query(Language).all()
    assert len(languages) > 0 