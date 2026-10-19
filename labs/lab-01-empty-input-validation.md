# Lab 01 — Empty Input Validation

**Project:** URL Shortener  
**Topic:** Server-side input validation  
**Status:** Implementation and initial tests passed

## 1. Objective

Reject empty or whitespace-only URL submissions before they reach
the database lookup and insertion logic.

## 2. Problem

The original Flask route read the submitted value and continued
processing without explicitly checking whether it was empty.

This could allow an empty string to be stored as an original URL.

HTML validation improves user experience, but it cannot replace
server-side validation because clients can send HTTP requests
without using the browser form.

## 3. Implementation

Added this guard inside the `home()` route, immediately after
reading the submitted form value:

```python
url_received = request.form['nm']
url_received = url_received.strip()

if url_received == '':
    return "URL cannot be empty", 400
```

### How it works

- `request.form['nm']` retrieves the submitted form value.
- `.strip()` removes leading and trailing whitespace.
- `url_received == ''` checks whether the normalized value is empty.
- HTTP 400 indicates that the submitted request is invalid.
- Returning immediately prevents this request from reaching the
  subsequent database lookup and insertion logic.

## 4. Tests

### Test A — Empty input

```bash
curl -i -X POST \
  --data-urlencode 'nm=' \
  http://127.0.0.1:5000/
```

Expected and observed: `400 BAD REQUEST`.

### Test B — Whitespace-only input

```bash
curl -i -X POST \
  --data-urlencode 'nm=   ' \
  http://127.0.0.1:5000/
```

Expected and observed: `400 BAD REQUEST`.

### Test C — Valid URL

```bash
curl -i -X POST \
  --data-urlencode 'nm=https://example.com' \
  http://127.0.0.1:5000/
```

Expected and observed: `302 FOUND`, redirecting to the
short-URL display route.

### Database inspection

Observed database state after testing:

- Total URL records: 4
- Empty or whitespace-only original URLs: 0

This confirms there are no such invalid records in the inspected
database. A before-and-after record count was not captured.

## 5. Key Learnings

1. Validate user input on the server, not only in HTML.
2. Normalize input before validating it.
3. An empty string (`''`) differs from a whitespace-only string
   (`'   '`).
4. An early return prevents invalid input from reaching later
   operations in the request handler.
5. HTTP status codes communicate the outcome of a request.
6. Test server behavior directly with tools such as `curl`.

## 6. Current Limitations

- Missing form fields are not handled explicitly.
- URL structure and permitted schemes are not validated on the
  server by this change.
- User-facing validation errors have not been implemented.
- No automated regression tests have been added.

These concerns are intentionally outside this lab's scope.

## 7. Next Lab

**Topic:** Handle a missing form field safely.

Investigate how Flask behaves when a POST request omits the `nm`
field, then implement and test a controlled response.

## 8. Git Checklist

- [ ] Review the implementation diff.
- [ ] Review this lab file.
- [ ] Run all relevant tests.
- [ ] Commit only after the changes are satisfactory.
