# MyTestFramework
Basic test automation framework 


To run the tests
1. Download all the files under MyTestFramework.
2. Create and activate a virtualenv
3. Install all the packages listed in requirements.txt <code> pip install -r requirements.txt </code> in the virtualenv
4. Start the mock flask server that serves the API calls <code>python mock_server.py & </code> - To restart, kill the pid for the process running mock_server and exectue the command again.
5. Start the mock frontend <code>python -m http.server 8080 --directory frontend & </code> - To restart, kill the pid for the process running the frontend and execute the command again.
6. Verify UI mock is work by `http://localhost:8080/index.html` in your browser
7. To run tests:
8. ----- All tests - <code>pytest  --html=reports/report.html --self-contained-html  -v</code>
9. ----- Specific test - <code>pytest  --html=reports/report.html --self-contained-html  -v -k test_create_user_invalid_account_type</code>
10. Both API test and UI test code are under `/tests/`
11. Test reports after every run can be viewed in browser using - `<path_to_project>/reports/report.html`
12. Screenshots for failing UI tests will be attached to the repor.html, or can be viewed under `screenshots` folder
