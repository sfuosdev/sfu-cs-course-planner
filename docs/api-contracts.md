# API Contracts

The REST API between the React frontend and the FastAPI backend. Each request and
response shape below is defined as a Pydantic schema in `backend/app/schemas/`. The
schema name is listed with every endpoint.

> Status: designed in #9. The auth endpoints and the plan endpoints
> (`/api/plans` and `/api/plans/{plan_id}`) are implemented (#38). The rest are not
> implemented yet.

## Conventions

- **All paths start with `/api`**, e.g. `/api/courses`. `/health` is the only
  exception.
- **JSON keys are camelCase** (`courseCode`, `planCourses`). The Python code uses
  snake_case (`course_code`). The schemas convert between the two with
  `alias_generator=to_camel`.
- **IDs are integers.** The frontend's `Course.id` in `frontend/src/types/course.ts`
  is currently a `string` and should change to `number`.
- **Plan slots.** A course in a plan is placed by `year` (`1`, `2`, `3`, ...) and
  `season` (`"fall"`, `"spring"` or `"summer"`, lowercase), the same grid the
  frontend shows. Within a year the order is fall, spring, summer. Plans don't
  need real term codes.
- **Term codes** are SFU's 4-digit codes: `1` + 2-digit year + starting month.
  `1251` = Spring 2025, `1254` = Summer 2025, `1257` = Fall 2025. A plan's optional
  `startTermCode` uses this format so slots can be turned into real terms later.
- **Timestamps** are ISO 8601 strings, e.g. `"2026-01-15T18:30:00Z"`.
- **`null`** means a value is missing or doesn't apply, e.g. a course with no
  designation.
- **`credits` is never `null`.** It is `0` when SFU lists no units for a course.
  The backend stores missing units as `0` (see `Course` in
  `backend/app/models/courses.py`).
- **Users:** `/api/plans` endpoints act on the signed-in user's plans, identified by
  the `session` cookie (see [Auth](#auth)). No endpoint takes a user ID. Browsers
  send the cookie automatically; other clients must send it back too.

## Endpoints

| Method | Path | Request body | Success response |
|---|---|---|---|
| POST | `/api/auth/register` | `RegisterRequest` | `201` `UserResponse`, signs in |
| POST | `/api/auth/login` | `LoginRequest` | `200` `UserResponse`, signs in |
| POST | `/api/auth/logout` | none | `204` no body |
| GET | `/api/auth/me` | none | `200` `UserResponse` |
| GET | `/api/courses` | none | `200` list of `CourseSummary` |
| GET | `/api/courses/{courseCode}` | none | `200` `CourseResponse` |
| GET | `/api/terms` | none | `200` list of `TermRead` |
| GET | `/api/plans` | none | `200` list of `PlanResponse` |
| POST | `/api/plans` | `PlanCreate` | `201` `PlanDetailResponse` |
| GET | `/api/plans/{plan_id}` | none | `200` `PlanDetailResponse` |
| PATCH | `/api/plans/{plan_id}` | `PlanUpdate` | `200` `PlanResponse` |
| DELETE | `/api/plans/{plan_id}` | none | `204` no body |
| POST | `/api/plans/{plan_id}/courses` | `PlanCourseCreate` | `201` `PlanCourseRead` |
| PATCH | `/api/plans/{plan_id}/courses/{plan_course_id}` | `PlanCourseUpdate` | `200` `PlanCourseRead` |
| DELETE | `/api/plans/{plan_id}/courses/{plan_course_id}` | none | `204` no body |
| GET | `/api/programs/{program_code}/requirements` | none | `200` list of `ProgramRequirementResponse` |

---

### Auth

Signing in sets a `session` cookie (`HttpOnly`, `SameSite=Lax`, `Secure` outside
development) that lasts 7 days by default. Send it back on later requests. JavaScript
can't read it, so `fetch` calls from another origin need `credentials: "include"`.
Routes that need a signed-in user return `401` without a valid cookie.

#### `POST /api/auth/register`

Creates an account and signs in.

Request, a `RegisterRequest`. `email` must be a valid email address, and `password`
must be 8–128 characters. Emails aren't case-sensitive. `username` is a display name:
it is trimmed, must be 1–50 characters, and doesn't have to be unique. Sign-in still
uses the email:

```json
{ "email": "student@sfu.ca", "password": "correct horse battery", "username": "Test user" }
```

Response `201`, a `UserResponse`, with the `session` cookie set. The password is
never returned:

```json
{ "id": 1, "email": "student@sfu.ca", "username": "Test user", "createdAt": "2026-01-15T18:30:00Z" }
```

Errors: `409` if the email already has an account; `422` for an invalid email, a
password that is too short or too long, or a username that is missing, blank or
longer than 50 characters.

#### `POST /api/auth/login`

Signs in with an existing account. Request, a `LoginRequest`, with the `email` and
`password` used to register:

```json
{ "email": "student@sfu.ca", "password": "correct horse battery" }
```

Response `200`, a `UserResponse`, with a new `session` cookie. Errors: `401` with
`"Invalid email or password"`, the same for a wrong password and an unknown email;
`422` for a malformed body.

#### `POST /api/auth/logout`

Ends the current session on the server and clears the cookie. Response `204` with no
body. It also returns `204` when nobody is signed in.

#### `GET /api/auth/me`

Returns the signed-in user, so the frontend can check whether someone is signed in.
Response `200`, a `UserResponse`. Errors: `401` if not signed in.

---

### Courses

#### `GET /api/courses`

Lists courses, with optional search and paging.

Query parameters, all optional:

| Parameter | Example | Meaning |
|---|---|---|
| `q` | `data struct` | Case-insensitive text search on course code and title |
| `subject` | `CMPT` | Only courses in this department, case-insensitive |
| `limit` | `20` | Return at most this many courses, 1–500. No limit if left out |
| `offset` | `40` | Skip this many courses first. Default `0` |

Example: `GET /api/courses?subject=CMPT&q=data&limit=20&offset=0`

With no parameters, every course is returned, so the frontend can keep loading the
full list once and filtering it in the browser. Results are always sorted by
department, then course number, so paging with `limit` and `offset` is stable.

Errors: `422` if `limit` is below 1 or above 500, or `offset` is negative.

The response is a plain list, not an envelope like `{ "items": [...], "total": 152 }`.
With only CMPT courses the frontend can load everything at once, so it doesn't need
a total count. Switching to an envelope later is a breaking change the frontend has
to be updated for.

Response `200`, a list of `CourseSummary`:

```json
[
  { "id": 1, "courseCode": "CMPT 120", "title": "Introduction to Computing Science and Programming I", "credits": 3 },
  { "id": 12, "courseCode": "CMPT 225", "title": "Data Structures and Programming", "credits": 3 }
]
```

`credits` is `0` when SFU lists no units for the course. The frontend should show
this as "units not listed", not "0 credits".

#### `GET /api/courses/{courseCode}`

Returns one course's full details.

`courseCode` is written with a hyphen instead of a space, e.g.
`/api/courses/CMPT-225` or `/api/courses/CMPT-105W`. It is case-insensitive, so
`cmpt-225` also works. The backend splits it on the first hyphen into the
department and the course number.

Errors: `404` if no course has that code.

Response `200`, a `CourseResponse` (`CourseSummary` plus these fields):

```json
{
  "id": 12,
  "courseCode": "CMPT 225",
  "title": "Data Structures and Programming",
  "credits": 3,
  "description": "Introduction to a variety of practical and important data structures...",
  "degreeLevel": "UGRD",
  "designation": "Quantitative",
  "prerequisitesText": "(MACM 101 and (CMPT 125, CMPT 129 or CMPT 135)) or (ENSC 251 and ENSC 252), all with a minimum grade of C-.",
  "corequisitesText": null,
  "outlineUrl": "https://www.sfu.ca/students/calendar/2026/fall/courses/cmpt/225.html",
  "prerequisites": [
    {
      "groupNumber": 1,
      "requiredCourse": { "id": 3, "courseCode": "CMPT 125", "title": "Introduction to Computing Science and Programming II", "credits": 3 }
    }
  ]
}
```

`prerequisitesText` is SFU's original wording and should always be shown to the
user. `prerequisites` is the structured version the app checks. It can't yet
express every rule, such as "(A and B) or (C and D)" or minimum grades.

`outlineUrl` links to the course's official SFU page. It is `null` if there isn't one.

---

### Terms

#### `GET /api/terms`

Lists SFU terms. Plans don't use this endpoint. It's kept for checking course
offerings and for choosing a plan's `startTermCode`.

Response `200`, a list of `TermRead`:

```json
[
  { "code": 1257, "year": 2025, "season": "Fall" },
  { "code": 1261, "year": 2026, "season": "Spring" }
]
```

---

### Plans

#### `GET /api/plans`

Lists the signed-in user's plans, without their courses. Errors: `401`.

Response `200`, a list of `PlanResponse`:

```json
[
  {
    "id": 7,
    "name": "Graduate in 4 years",
    "version": 3,
    "startTermCode": 1257,
    "createdAt": "2026-01-15T18:30:00Z",
    "updatedAt": "2026-02-02T09:12:44Z"
  }
]
```

#### `POST /api/plans`

Creates a plan.

Request, a `PlanCreate`. `name` is required, 1–255 characters. `startTermCode`
is optional and can be `null` or left out if the student hasn't picked a start term:

```json
{ "name": "Graduate in 4 years", "startTermCode": 1257 }
```

Response `201`, a `PlanDetailResponse`. A new plan has an empty `planCourses` list.
Errors: `401`; `422` if `name` is missing, empty, or too long.

#### `GET /api/plans/{plan_id}`

Returns one plan with all its courses. Errors: `401`; `404` if the plan doesn't
exist or belongs to another user.

Response `200`, a `PlanDetailResponse` (`PlanResponse` plus `planCourses`):

```json
{
  "id": 7,
  "name": "Graduate in 4 years",
  "version": 3,
  "startTermCode": 1257,
  "createdAt": "2026-01-15T18:30:00Z",
  "updatedAt": "2026-02-02T09:12:44Z",
  "planCourses": [
    {
      "id": 41,
      "year": 1,
      "season": "fall",
      "course": { "id": 12, "courseCode": "CMPT 225", "title": "Data Structures and Programming", "credits": 3 }
    }
  ]
}
```

#### `PATCH /api/plans/{plan_id}`

Renames a plan or changes its start term.

Request, a `PlanUpdate`. `name` is required, 1–255 characters. `version` is
required and must match the plan's current `version`. `startTermCode` is optional.
Changing it doesn't move any courses, because they're stored by year and season:

```json
{ "name": "Graduate in 5 years", "version": 3, "startTermCode": 1267 }
```

Response `200`, a `PlanResponse` with `version` increased by 1. Errors: `401`; `404`
if the plan doesn't exist or belongs to another user; `409` if `version` isn't the
plan's current version, because it was changed since the client loaded it; `422` for
an invalid name.

#### `DELETE /api/plans/{plan_id}`

Deletes a plan and all its courses. Response `204` with no body. Errors: `401`;
`404` if the plan doesn't exist or belongs to another user.

---

### Courses in a plan

#### `POST /api/plans/{plan_id}/courses`

Adds a course to a plan in a given year and season.

Request, a `PlanCourseCreate`. `year` must be `1` or more, and `season` must be
`"fall"`, `"spring"` or `"summer"`:

```json
{ "courseId": 12, "year": 1, "season": "fall" }
```

Response `201`, a `PlanCourseRead`:

```json
{
  "id": 41,
  "year": 1,
  "season": "fall",
  "course": { "id": 12, "courseCode": "CMPT 225", "title": "Data Structures and Programming", "credits": 3 }
}
```

Errors: `404` if the plan or course doesn't exist; `409` if the course is already
in the plan; `422` if a field is missing, the wrong type, `year` is below `1`, or
`season` isn't one of the three values.

#### `PATCH /api/plans/{plan_id}/courses/{plan_course_id}`

Moves a course in a plan to a different year and season.

Request, a `PlanCourseUpdate`:

```json
{ "year": 1, "season": "spring" }
```

Response `200`, a `PlanCourseRead`. Errors: `404`, `422`.

#### `DELETE /api/plans/{plan_id}/courses/{plan_course_id}`

Removes a course from a plan. Response `204` with no body. Errors: `404`.

---

### Program requirements

#### `GET /api/programs/{program_code}/requirements`

Lists the requirements for a program, e.g. `CMPT-MAJOR`. Errors: `404` if the
program doesn't exist.

Response `200`, a list of `ProgramRequirementResponse`:

```json
[
  {
    "id": 1,
    "programCode": "CMPT-MAJOR",
    "name": "Calculus",
    "minCredits": null,
    "minCourses": 2,
    "courses": [
      { "course": { "id": 20, "courseCode": "MATH 150", "title": "Calculus I with Review", "credits": 4 } },
      { "course": { "id": 21, "courseCode": "MATH 152", "title": "Calculus II", "credits": 3 } }
    ]
  }
]
```

A requirement is met when the student has at least `minCourses` of the listed
courses and/or at least `minCredits` credits from them, whichever are set.

## Errors

Errors return an `ErrorResponse`:

```json
{ "detail": "Plan not found" }
```

| Status | Meaning |
|---|---|
| `404` | The resource doesn't exist, or belongs to another user. The API doesn't say which |
| `409` | The request conflicts with existing data, e.g. adding a course that's already in the plan, registering a taken email, or updating a plan with an out-of-date `version` |
| `422` | The request body or path failed validation. FastAPI returns `detail` as a list of `{ "loc", "msg", "type" }` objects |
| `401` | Not signed in, or the session expired. Also returned for a wrong email or password at login |
