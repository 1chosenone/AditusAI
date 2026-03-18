import pytest
from database.session import SESSION_LOCAL
from models.candidate import Candidate


@pytest.fixture
def db_session():
    session = SESSION_LOCAL()
    yield session
    session.rollback()
    session.close()


def test_candidate_crud(db_session):
    candidate = Candidate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
    )
    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    fetched = db_session.get(Candidate, candidate.candidate_id)
    assert fetched is not None
    assert fetched.first_name == "John"
    assert fetched.last_name == "Doe"
    assert fetched.email == "john.doe@example.com"

    db_session.delete(fetched)
    db_session.commit()

    assert db_session.get(Candidate, candidate.candidate_id) is None
