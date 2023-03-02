echo "1. Check if server is alive on GET http://0.0.0.0:8000"
echo "RESPONSE: $(curl -s -i http://0.0.0.0:8000/)"

echo "\n2. Try access a protceted route at GET http://0.0.0.0:8000/protected"
echo "RESPONSE: $(curl -s http://0.0.0.0:8000/protected)"

echo "\n3. Try logout without being authenticated at POST http://0.0.0.0:8000/logout"
echo "RESPONSE: $(curl -X POST -s http://0.0.0.0:8000/logout)"

echo "\n4. Login as tony.stark@test.com at POST http://0.0.0.0:8000/login"
TOKEN=$(curl -X POST -s --json '{"email":"tony.stark@test.com", "password":"hello"}' http://0.0.0.0:8000/login | jq .access_token | tr -d '\"')
echo "RESPONSE: Token Retrieved -> $TOKEN"

echo "\n5. Try access a protceted route at GET http://0.0.0.0:8000/protected"
echo "RESPONSE: $(curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/protected)"

echo "\n6. Try access to personal details at GET http://0.0.0.0:8000/me"
echo "RESPONSE: $(curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/me)"

echo "\n7. Logout at POST http://0.0.0.0:8000/logout"
echo "RESPONSE: $(curl -X POST -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/logout)"

echo "\n8. Try access a protceted route at GET http://0.0.0.0:8000/protected"
echo "RESPONSE: $(curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/protected)"

echo "\n9. Check Blacklist at GET http://0.0.0.0:8000/blacklist"
echo "RESPONSE: $(curl -s http://0.0.0.0:8000/blacklist)"
