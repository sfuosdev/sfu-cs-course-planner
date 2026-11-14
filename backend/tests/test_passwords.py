from app.services.passwords import hash_password, verify_password #peep that verity reference

def test_passhash():
    password = "helloWorldANDPRINT123!"
    daHashPass = hash_password(password)

    assert password != daHashPass
    assert verify_password(password, daHashPass)

def test_wrongpassword():
    password = "xxSFUluvr2006!xx"
    daHashPass = hash_password(password)

    assert not verify_password("EvilSfuHater67?", daHashPass)

def test_diffhashes():
    password = "ummmmPASSWORD123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2