import pytest
from .conftest import Note
from datetime import datetime

"""
Test af notes endpoints
- Igen lange og lidt rodede tests, men det for at få det igang asap og så lige en beskrivelse nedenunder fra onkel GPT
"""
"""
Oversigt over test af note endpoints:

1. Brugerlogind:
   - Logger en testbruger ind for at kunne gennemføre de efterfølgende tests.

2. Opret Note:
   - GET-anmodning til oprettelsessiden for at sikre, at den indlæses korrekt for den indloggede bruger.
   - POST-anmodning for faktisk at oprette en note og bekræfte, at det lykkes, herunder en kontrol af, at noten er tilføjet til databasen.
   - Forsøger at oprette en note uden at være logget ind, for at bekræfte, at uautoriserede handlinger forhindres.
3. Rediger Note:
   - Forbereder ved at oprette en note, der skal redigeres.
   - GET-anmodning til redigeringssiden for at sikre, at den indlæses korrekt, med specifikke notedetaljer forudindlæst for den indloggede bruger.
   - POST-anmodning for at opdatere en notes titel og indhold, og bekræfte at ændringerne gemmes og vises korrekt.

4. Slet Note:
   - Forbereder ved at oprette en note, der skal slettes.
   - Tester succesfuld sletning af en note via en GET-anmodning, og sikrer at noten fjernes fra databasen.
   - Forsøger at slette en note som en anden bruger end den, der oprettede den, for at bekræfte, at uautoriserede handlinger forhindres.
   - Sletter succesfuldt en note som en admin-bruger, hvilket bekræfter, at højere privilegier tillader sletning.

5. Søg i Noter:
   - Tilføjer en note, der skal søges efter.
   - Udfører en succesfuld søgning, der finder noten.
   - Tester mislykkede søgninger med forespørgsler, der ikke matcher nogen note, og bekræfter passende feedback, når der ikke findes resultater.
"""



@pytest.fixture
def log_in_test_user(client):
    # This is a simplified version. You should implement your actual login logic here
    with client.session_transaction() as session:
        session['user'] = 'testuserNotes'
        session['userID'] = 9999
        session['userEmail'] = 'testusernotes@test.com'
        session['roleID'] = 1 #standard bruger

#test create note uden at være logget ind:
def test_create_note_get_not_logged_in(client):
    response = client.get('/notes/create/', follow_redirects=True)
    print(response.data)
    assert 'You need to be logged in to view this page.' in response.data.decode('utf-8')
    assert 'Login' in response.data.decode('utf-8')
    assert response.status_code == 200

# Test creating a note
def test_create_note_get(client, log_in_test_user):
    response = client.get('/notes/create/')
    assert 'Logged in as: ' in response.data.decode('utf-8')
    assert 'Create Note' in response.data.decode('utf-8')
    assert 'Opret Note' in response.data.decode('utf-8')
    assert response.status_code == 200

def test_create_note_post(client, log_in_test_user, dbsession):
    response = client.post('/notes/create/', data=dict(
        title='Test Note',
        note='This is a test note'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Hjem' in response.data
    assert 'Failed to create note' not in response.data.decode('utf-8')
    assert 'Note created successfully' in response.data.decode('utf-8')
    # Fordi Test Note er titlen og vi redirecter til home, så tjekker vi om Test Note er i home
    assert 'Test Note' in response.data.decode('utf-8')
    # for god ordens skyld tjekker vi også om noten er i databasen på den direkte måde
    note = dbsession.query(Note).filter_by(title='Test Note').first()
    assert note is not None
    assert note.title == 'Test Note'
    assert note.text == 'This is a test note'

def test_edit_note_get_not_logged_in(client):
    response = client.get('/notes/edit/1', follow_redirects=True)
    assert 'You need to be logged in to view this page.' in response.data.decode('utf-8')
    assert 'Login' in response.data.decode('utf-8')
    assert response.status_code == 200

def test_edit_note_get(client, log_in_test_user, dbsession):
    # Create a note to edit
    note = Note(
        title='Test Edit Note', 
        text='This is a test edit note, for testing edit endpoint in pytest', 
        created = datetime.now(),
        lastedited = datetime.now(),
        imagelink = None,
        author=9999)
    dbsession.add(note)
    dbsession.commit()
    response = client.get(f'/notes/edit/{note.noteID}')
    assert 'Logged in as: ' in response.data.decode('utf-8')
    assert 'Edit Note' in response.data.decode('utf-8')
    assert 'Rediger Note' in response.data.decode('utf-8')
    assert 'This is a test edit note' in response.data.decode('utf-8')
    assert 'Test Edit Note' in response.data.decode('utf-8')
    assert response.status_code == 200
    
def test_edit_note_post(client, log_in_test_user, dbsession):
    # Create a note to edit
    note = Note(
        title='Test Edit Note Post', 
        text='This is a test edit note post, for testing edit post endpoint in pytest', 
        created = datetime.now(),
        lastedited = datetime.now(),
        imagelink = None,
        author=9999)
    dbsession.add(note)
    dbsession.commit()
    response = client.post(f'/notes/edit/{note.noteID}', data=dict(
        title='EDITED Test Post',
        note='This is a test edit note, for testing edit endpoint in pytest, and this is the edited text'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Hjem' in response.data
    assert 'Failed to edit note' not in response.data.decode('utf-8')
    assert 'Note created successfully' in response.data.decode('utf-8')
    assert 'EDITED Test Post' in response.data.decode('utf-8')
    
def test_delete_note_get_not_logged_in(client):
    response = client.get('/notes/delete/1', follow_redirects=True)
    assert 'You need to be logged in to view this page.' in response.data.decode('utf-8')
    assert 'Login' in response.data.decode('utf-8')
    assert response.status_code == 200
    
def test_delete_note_post_success(client, log_in_test_user, dbsession):
    # Create a note to delete
    note = Note(
        title='Test Delete Note', 
        text='This is a test delete note, for testing delete endpoint in pytest', 
        created = datetime.now(),
        lastedited = datetime.now(),
        imagelink = None,
        author=9999)
    dbsession.add(note)
    dbsession.commit()
    response = client.get(f'/notes/delete/{note.noteID}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Hjem' in response.data
    assert 'Failed to delete note' not in response.data.decode('utf-8')
    assert 'Note deleted successfully' in response.data.decode('utf-8')
    assert 'Test Delete Note' not in response.data.decode('utf-8')
    # for god ordens skyld tjekker vi også om noten er i databasen på den direkte måde
    note = dbsession.query(Note).filter_by(title='Test Delete Note').first()
    assert note is None

def test_delete_note_post_fail(client, log_in_test_user, dbsession):
    # Create a note to delete
    note = Note(
        title='Test Delete Note Fail', 
        text='This is a test delete note, for testing delete endpoint in pytest', 
        created = datetime.now(),
        lastedited = datetime.now(),
        imagelink = None,
        author=9999)
    dbsession.add(note)
    dbsession.commit()
    # prøver at slette med en anden bruger
    with client.session_transaction() as session:
        session['user'] = 'testuserNotes2'
        session['userID'] = 9998
        session['userEmail'] = 'testusernotes2@test.com'
        session['roleID'] = 1
    response = client.get(f'/notes/delete/{note.noteID}', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Hjem' in response.data
    assert 'You are not authorized to delete this note' in response.data.decode('utf-8')
    assert 'Note deleted successfully' not in response.data.decode('utf-8')
    assert 'Test Delete Note Fail' in response.data.decode('utf-8')
    # for god ordens skyld tjekker vi også om noten er i databasen på den direkte måde
    note = dbsession.query(Note).filter_by(title='Test Delete Note Fail').first()
    assert note is not None
    assert note.title == 'Test Delete Note Fail'

def test_delete_note_admin(client, log_in_test_user, dbsession):
    # Create a note to delete
    note = Note(
        title='Test Delete Note Admin', 
        text='This is a test delete note, for testing delete endpoint in pytest', 
        created = datetime.now(),
        lastedited = datetime.now(),
        imagelink = None,
        author=9999)
    dbsession.add(note)
    dbsession.commit()
    # prøver at slette med en admin (roleID = 2)   
    with client.session_transaction() as session:
        session['user'] = 'testuserNotesAdmin'
        session['userID'] = 9997
        session['userEmail'] = 'admin@test.com'
        session['roleID'] = 2
    response = client.get(f'/notes/delete/{note.noteID}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Hjem' in response.data
    assert 'Note deleted successfully' in response.data.decode('utf-8')
    assert 'Test Delete Note Admin' not in response.data.decode('utf-8')
    # for god ordens skyld tjekker vi også om noten er i databasen på den direkte måde
    note = dbsession.query(Note).filter_by(title='Test Delete Note Admin').first()
    assert note is None
    
def test_search_result_success(client, log_in_test_user, dbsession):

    note = Note(
        title='Test Search Note', 
        text='This is a test search note, for testing search endpoint in pytest', 
        created = datetime.now(),
        lastedited = datetime.now(),
        imagelink = None,
        author=9999)
    dbsession.add(note)
    dbsession.commit()
    response = client.get('/notes/search?query=Test Search Note')
    assert response.status_code == 200
    assert 'Test Search Note' in response.data.decode('utf-8')
    assert 'This is a test search note' in response.data.decode('utf-8')
    assert 'Ryd søgning' in response.data.decode('utf-8')

def test_search_result_fail(client, log_in_test_user, dbsession):

    note = Note(
        title='Test Search Note Fail', 
        text='This is a test search note, for testing search endpoint in pytest', 
        created = datetime.now(),
        lastedited = datetime.now(),
        imagelink = None,
        author=9999)
    dbsession.add(note)
    dbsession.commit()
    response = client.get('/notes/search?query=Test Search Note XFail')
    assert response.status_code == 200
    assert 'Test Search Note Fail' not in response.data.decode('utf-8')
    assert 'This is a test search note' not in response.data.decode('utf-8')
    assert 'Ryd søgning' not in response.data.decode('utf-8')
    assert 'Søgningen gav ingen resultater!' in response.data.decode('utf-8')
    response = client.get('/notes/search?query=TestSearch')
    assert response.status_code == 200
    assert 'Test Search Note Fail' not in response.data.decode('utf-8')
    assert 'This is a test search note' not in response.data.decode('utf-8')
    assert 'Ryd søgning' not in response.data.decode('utf-8')
    assert 'Søgningen gav ingen resultater!' in response.data.decode('utf-8')