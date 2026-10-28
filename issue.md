# Issue Documentation Table

| Issue | Type | Original Location | Description | Fix Approach |
|---|---|---|---|---|
| Hardcoded ERP API key | Security | Global configuration | API key was stored directly in source code. | Read the key from the `ERP_API_KEY` environment variable. |
| Disabled TLS verification | Security | `sync_to_erp()` | Disabling certificate verification can expose HTTPS requests to interception. | Use the default certificate verification and remove `verify=False`. |
| Missing request timeout | Reliability | `sync_to_erp()` | A request could wait indefinitely. | Add a timeout to the HTTP request. |
| Mutable default argument | Bug | `mark_attendance()` | A shared mutable default could retain data between calls. | Use `None` and initialize a new dictionary. |
| Incorrect eligibility boundary | Logic bug | `is_eligible()` | Exactly 75% attendance was rejected. | Use `>=` to include the minimum threshold. |
| Division by zero | Reliability | `attendance_percentage()` | Empty attendance records could cause division by zero. | Return 0 when no records exist. |
| Unsafe CSV handling | Reliability | `export_csv()` | File handling lacked a context manager and explicit encoding. | Use `with open(...)`, UTF-8 encoding, and newline handling. |
| Spreadsheet formula injection | Security | `export_csv()` | User-provided values could be interpreted as spreadsheet formulas. | Prefix potentially dangerous text values with an apostrophe. |
| Unsafe shell execution | Security | `run_job()` | Shell execution can expose commands to injection risks. | Represent commands as argument lists and avoid shell execution. |
| Deprecated TLS protocol | Security | `legacyChannel()` | The original code used an obsolete TLS protocol. | Remove the deprecated protocol function. |
| Poor naming and formatting | Code quality | Multiple functions | CamelCase names, unused imports, and formatting issues reduced readability. | Use snake_case, remove unused imports, and correct formatting. |
| Empty attendance history | Reliability | `latest_date()` | Finding the maximum date could fail when there were no records. | Return `None` for empty histories. |

## Summary

Pylint, Bandit, and Flake8 were used to analyze the Attendance Tracker program. The code was updated to improve security, reliability, logic, and formatting. The final reports should be retained as evidence of the results after the fixes.