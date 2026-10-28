# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis?

Static code analysis examines source code without executing the program. It helps identify potential programming errors, security vulnerabilities, and style violations before deployment.

## 2. What is the difference between Pylint, Bandit, and Flake8?

Pylint checks code quality, naming conventions, and potential programming problems. Bandit identifies common security vulnerabilities and unsafe coding patterns. Flake8 checks formatting, whitespace, and compliance with Python style conventions.

## 3. What issues did you identify and fix during this lab?

I addressed multiple issues in the Attendance Tracker, including a hardcoded ERP API key, disabled TLS certificate verification, missing request timeouts, a mutable default argument, and an incorrect attendance eligibility boundary. I also improved empty-record handling, CSV export safety, command handling, naming, and formatting.

## 4. How does static code analysis improve software quality?

Static code analysis helps detect potential defects early in development. It improves security, encourages consistent coding practices, and makes software easier to read and maintain. However, it should be combined with program execution and functional testing because static analysis cannot detect every runtime or logical problem.