Install CPPCheck at :https://cppcheck.sourceforge.io/
Check CPPCheck added on Path? if not, check here : https://chatgpt.com/share/67cb206e-3c60-8013-812e-c013e3aac97a 

Call function check_cpp_code(code_snip)

TesAPI:

URL: localhost - port 8000.
Endpoint: The endpoint is /analyze-code.
Method: POST.
Request Body: JSON with the code key.
Example curl command:
curl -X POST -H "Content-Type: application/json" -d '{"code": "int main() { int x; return 0; }"}' http://127.0.0.1:8000/analyze-code
or
curl -X POST -H "Content-Type: application/json" -d '{"code": "int x = 10; int y; st
